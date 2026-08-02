#!/usr/bin/env python3
"""Valida e identifica o barramento NEXUS Cosmos sem publicar nada.

O script é deliberadamente local e fail-closed. A sincronização externa é
executada pelos conectores registrados; main e GitHub Pages só podem ser
liberados com ``PUBLICAR {TAF###-EXATO}`` na sessão corrente.
"""

from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import json
import mimetypes
import os
import re
import secrets
import stat
import sys
import unicodedata
import zipfile
import zlib
from datetime import date, datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COSMOS = ROOT / "23_Cosmos_NEXUS"
DATA = COSMOS / "data"
HEX64 = re.compile(r"^[a-f0-9]{64}$")
AGX = re.compile(
    r"^####AGX-(U1|U2|U3|MUX)-"
    r"(EVO|PLAN|VIS|STUDY|TEMI|REFINE|TUTOR|MICRO|IMGT|PROD|REFS|AUDIT|EXT)-"
    r"[0-9]{8}-[0-9]{4}-[A-F0-9]{8}$"
)
TAF = re.compile(
    r"^TAF###-(U1|U2|U3|MUX)-"
    r"(EVO|PLAN|VIS|STUDY|TEMI|REFINE|TUTOR|MICRO|IMGT|PROD|REFS|AUDIT|EXT)-"
    r"[0-9]{8}-[0-9]{4}-[A-F0-9]{8}$"
)
IMG = re.compile(r"^####IMG-[0-9]{8}-[0-9]{4}-[A-F0-9]{8}$")
UNIVERSES = {"U1", "U2", "U3", "MUX"}
BLOCKS = {
    "EVO", "PLAN", "VIS", "STUDY", "TEMI", "REFINE", "TUTOR",
    "MICRO", "IMGT", "PROD", "REFS", "AUDIT", "EXT",
}
BLOCK_ALIASES = {
    "evolucao": "EVO",
    "plano-terapeutico": "PLAN",
    "motor-visual": "VIS",
    "organizador-estudos": "STUDY",
    "turbo-temi": "TEMI",
    "refinaria-temi": "REFINE",
    "tutor": "TUTOR",
    "estudo-microparticulado": "MICRO",
    "imagens-turbo-temi": "IMGT",
    "produtos-turbo-temi": "PROD",
    "referencias-evidencias": "REFS",
    "auditoria-publicacao": "AUDIT",
    "extensao": "EXT",
}
DOMAINS = {
    "clinical-educational": {"code": "MED", "private": False},
    "personal": {"code": "PER", "private": True},
    "legal": {"code": "JUR", "private": True},
    "financial": {"code": "FIN", "private": True},
    "administrative": {"code": "ADM", "private": True},
    "technology-ecosystem": {"code": "TEC", "private": True},
}
SOURCE_PROJECTS = {
    "@TURBOTEMI",
    "#EVOLUCOES",
    "#PLANOTERAPEUTICO",
    "@ORGANIZACAODEESTUDO",
    "@BIBLIOTECAVISUAL",
    "@TEMI360XINFINIT",
}
ORGANIZATION_STUDY_PROJECT = "@ORGANIZACAODEESTUDO"
AUTO_KIND_BY_SUFFIX = {
    ".docx": "gpt-word",
    ".pdf": "gpt-pdf",
    ".png": "gpt-image",
    ".jpg": "gpt-image",
    ".jpeg": "gpt-image",
    ".webp": "gpt-image",
}
ENTITY_PREFIX_BY_KIND = {
    "gpt-word": "DOC",
    "gpt-pdf": "PDF",
    "gpt-image": "IMG",
}
PRIVATE_QUEUE = ROOT / ".nexus-sync-private" / "queue"
MAX_FILE_BYTES = 256 * 1024 * 1024
MAX_DOCX_UNCOMPRESSED_BYTES = 512 * 1024 * 1024
MAX_DOCX_MEMBERS = 5000
MAX_DOCX_COMPRESSION_RATIO = 200
SAFE_INTAKE_KINDS = {"auto", "gpt-word", "gpt-pdf", "gpt-image"}
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
ZERO_HASH = "0" * 64
HOM = re.compile(r"^HOM###[A-Z0-9-]+$")
TOM = re.compile(r"^TOM###[A-Z0-9-]+$")
PRC = re.compile(r"^PRC###[A-Z0-9-]+$")
AUD = re.compile(r"^AUD###[A-Z0-9-]+$")
RELEASE_CONFIRMATIONS = {
    "safariMacOS",
    "safariIPhone",
    "clinicalReview",
    "rightsReview",
}
UMBRELLA_RELEASE_SCHEMA = "antigravity-umbrella-release-manifest-v1"
UMBRELLA_INVENTORY_POLICY = "explicit-closed-list-v1"
UMBRELLA_ROOT_ALGORITHM = "sha256:path-tab-sha256-tab-bytes-lf:sort-path:v1"
UMBRELLA_FILE_SUFFIXES = {
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".pdf",
    ".txt",
    ".xml",
}
UMBRELLA_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
MAX_RELEASE_MEMBERS = 5000
SOURCE_BOUND = "SOURCE_BOUND"
POST_BUILD_POST_SANITIZE = "POST_BUILD_POST_SANITIZE"
RELEASE_ARTIFACT_PROFILES = {SOURCE_BOUND, POST_BUILD_POST_SANITIZE}
SUPERSESSION_REASON = "VOID_PREPUBLICATION_SOURCE_SCOPE"
SUPERSEDED_RELEASE_FIELDS = {
    "procedureCode",
    "auditCode",
    "homologationCode",
    "tombstoneCode",
    "tafCode",
    "artifactProfile",
    "artifactRootSha256",
    "memberCount",
    "supersededAt",
    "supersededByTafCode",
    "supersessionProcedureCode",
    "reason",
    "publication",
}


class ContractError(ValueError):
    """Erro contratual legível para CI e operador."""


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"JSON ausente ou inválido: {path.relative_to(ROOT)}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"Objeto JSON esperado: {path.relative_to(ROOT)}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def digest8(*parts: str) -> str:
    canonical = "|".join(unicodedata.normalize("NFC", part.strip()) for part in parts)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:8].upper()


def token(value: str, field: str) -> str:
    cleaned = re.sub(r"[^A-Z0-9]+", "-", unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().upper()).strip("-")
    if not cleaned:
        raise ContractError(f"{field} vazio após normalização")
    return cleaned[:20]


def jpeg_dimensions(path: Path) -> tuple[int, int]:
    sof_markers = {
        0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
    }
    with path.open("rb") as source:
        if source.read(2) != b"\xff\xd8":
            raise ContractError(f"JPEG inválido: {path.name}")
        while True:
            prefix = source.read(1)
            if not prefix:
                break
            if prefix != b"\xff":
                continue
            marker_raw = source.read(1)
            while marker_raw == b"\xff":
                marker_raw = source.read(1)
            if not marker_raw:
                break
            marker = marker_raw[0]
            if marker == 0x00:
                continue
            if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
                continue
            size_raw = source.read(2)
            if len(size_raw) != 2:
                break
            segment_size = int.from_bytes(size_raw, "big")
            if segment_size < 2:
                break
            if marker in sof_markers:
                payload = source.read(segment_size - 2)
                if len(payload) < 5:
                    break
                return (
                    int.from_bytes(payload[3:5], "big"),
                    int.from_bytes(payload[1:3], "big"),
                )
            source.seek(segment_size - 2, os.SEEK_CUR)
    raise ContractError(f"Dimensões JPEG ausentes: {path.name}")


def _safe_text(value: str, field: str, limit: int) -> str:
    normalized = unicodedata.normalize("NFC", value.strip())
    if not normalized:
        raise ContractError(f"{field} vazio")
    if len(normalized) > limit:
        raise ContractError(f"{field} excede {limit} caracteres")
    if CONTROL_CHARS.search(normalized):
        raise ContractError(f"{field} contém caracteres de controle")
    return normalized


def _parse_calendar_date(value: str) -> str:
    if re.fullmatch(r"\d{8}", value):
        normalized = f"{value[:4]}-{value[4:6]}-{value[6:8]}"
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        normalized = value
    else:
        raise ContractError("data deve ser um calendário válido em YYYY-MM-DD ou YYYYMMDD")
    try:
        parsed = date.fromisoformat(normalized)
    except ValueError as exc:
        raise ContractError("data deve ser um calendário válido em YYYY-MM-DD ou YYYYMMDD") from exc
    return parsed.strftime("%Y%m%d")


def _secure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path, 0o700)


def _snapshot_source(source: Path, suffix: str, private_root: Path) -> tuple[Path, str, int, bool]:
    """Copia por descritor sem seguir symlink e congela bytes em blob privado."""

    _secure_directory(private_root)
    blob_root = private_root / "blobs"
    _secure_directory(blob_root)
    temporary = blob_root / f".snapshot-{os.getpid()}-{secrets.token_hex(8)}.tmp"
    source_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    source_fd = -1
    target_fd = -1
    digest = hashlib.sha256()
    total = 0
    try:
        source_fd = os.open(str(source), source_flags)
        before = os.fstat(source_fd)
        if not stat.S_ISREG(before.st_mode):
            raise ContractError("fonte precisa ser arquivo regular")
        if before.st_size <= 0 or before.st_size > MAX_FILE_BYTES:
            raise ContractError(f"fonte precisa ter entre 1 byte e {MAX_FILE_BYTES} bytes")
        target_fd = os.open(str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        while True:
            chunk = os.read(source_fd, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise ContractError(f"fonte excede {MAX_FILE_BYTES} bytes")
            digest.update(chunk)
            view = memoryview(chunk)
            while view:
                written = os.write(target_fd, view)
                view = view[written:]
        os.fsync(target_fd)
        after = os.fstat(source_fd)
        if (
            before.st_dev != after.st_dev
            or before.st_ino != after.st_ino
            or before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
            or total != before.st_size
        ):
            raise ContractError("fonte mudou durante o snapshot; tente novamente")
    except ContractError:
        temporary.unlink(missing_ok=True)
        raise
    except OSError as exc:
        temporary.unlink(missing_ok=True)
        raise ContractError(f"não foi possível congelar a fonte com segurança: {exc}") from exc
    finally:
        if target_fd >= 0:
            os.close(target_fd)
        if source_fd >= 0:
            os.close(source_fd)

    artifact_hash = digest.hexdigest()
    bucket = blob_root / artifact_hash[:2]
    _secure_directory(bucket)
    destination = bucket / f"{artifact_hash}{suffix}"
    created_new = False
    try:
        if destination.exists():
            if not destination.is_file() or sha256_file(destination) != artifact_hash:
                raise ContractError("colisão ou corrupção no blob privado")
            temporary.unlink(missing_ok=True)
        else:
            os.replace(temporary, destination)
            created_new = True
        os.chmod(destination, 0o600)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return destination, artifact_hash, total, created_new


def _validate_png(path: Path) -> None:
    with path.open("rb") as source:
        if source.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ContractError("PNG sem assinatura válida")
        seen_ihdr = seen_idat = seen_iend = False
        while True:
            length_raw = source.read(4)
            if not length_raw:
                break
            if len(length_raw) != 4:
                raise ContractError("PNG truncado no tamanho do chunk")
            length = int.from_bytes(length_raw, "big")
            if length > MAX_FILE_BYTES:
                raise ContractError("PNG contém chunk excessivo")
            chunk_type = source.read(4)
            payload = source.read(length)
            crc_raw = source.read(4)
            if len(chunk_type) != 4 or len(payload) != length or len(crc_raw) != 4:
                raise ContractError("PNG truncado")
            expected_crc = zlib.crc32(chunk_type + payload) & 0xFFFFFFFF
            if int.from_bytes(crc_raw, "big") != expected_crc:
                raise ContractError("PNG com CRC divergente")
            if chunk_type == b"IHDR":
                if seen_ihdr or length != 13 or int.from_bytes(payload[:4], "big") < 1 or int.from_bytes(payload[4:8], "big") < 1:
                    raise ContractError("PNG com IHDR inválido")
                seen_ihdr = True
            elif chunk_type == b"IDAT":
                seen_idat = True
            elif chunk_type == b"IEND":
                if length != 0 or source.read(1):
                    raise ContractError("PNG com IEND inválido ou bytes residuais")
                seen_iend = True
                break
        if not (seen_ihdr and seen_idat and seen_iend):
            raise ContractError("PNG sem IHDR, IDAT ou IEND completo")


def validate_materialized_file(path: Path, kind: str, original_suffix: str | None = None) -> None:
    """Valida estrutura mínima, assinatura e riscos óbvios do arquivo congelado."""

    suffix = (original_suffix or path.suffix).casefold()
    if kind not in SAFE_INTAKE_KINDS - {"auto"}:
        raise ContractError(f"tipo não permitido no intake seguro: {kind}")
    if kind == "gpt-word":
        if suffix != ".docx" or not zipfile.is_zipfile(path):
            raise ContractError("arquivo Word precisa ser um DOCX/ZIP válido")
        with zipfile.ZipFile(path) as package:
            infos = package.infolist()
            if len(infos) > MAX_DOCX_MEMBERS:
                raise ContractError("DOCX excede o limite de membros")
            total_uncompressed = 0
            members: set[str] = set()
            for info in infos:
                name = info.filename
                folded = name.casefold()
                if name.startswith("/") or "\\" in name or ".." in name.split("/"):
                    raise ContractError("DOCX contém caminho interno inseguro")
                if info.flag_bits & 0x1:
                    raise ContractError("DOCX contém membro criptografado")
                total_uncompressed += info.file_size
                if total_uncompressed > MAX_DOCX_UNCOMPRESSED_BYTES:
                    raise ContractError("DOCX excede o limite descompactado")
                if info.file_size and (
                    info.compress_size == 0
                    or info.file_size / info.compress_size > MAX_DOCX_COMPRESSION_RATIO
                ):
                    raise ContractError("DOCX excede a razão segura de compressão")
                if folded.endswith("vbaproject.bin"):
                    raise ContractError("DOCX contém macro VBA")
                members.add(name)
                if folded.endswith(".rels") and info.file_size:
                    if info.file_size > 2 * 1024 * 1024:
                        raise ContractError("relacionamentos DOCX excessivos")
                    relationships = package.read(info).lower()
                    if re.search(rb"targetmode\s*=\s*['\"]external['\"]", relationships):
                        raise ContractError("DOCX contém relacionamento externo")
        if "[Content_Types].xml" not in members or "word/document.xml" not in members:
            raise ContractError("DOCX sem estrutura Word obrigatória")
    elif kind == "gpt-pdf":
        size = path.stat().st_size
        with path.open("rb") as source:
            head = source.read(16)
            source.seek(max(0, size - 4096))
            tail = source.read()
        if suffix != ".pdf" or not re.match(rb"^%PDF-[12]\.\d", head) or b"%%EOF" not in tail:
            raise ContractError("PDF sem cabeçalho e EOF válidos")
    elif kind == "gpt-image":
        if suffix == ".png":
            _validate_png(path)
        elif suffix in {".jpg", ".jpeg"}:
            with path.open("rb") as source:
                source.seek(-2, os.SEEK_END)
                if source.read(2) != b"\xff\xd9":
                    raise ContractError("JPEG truncado ou sem EOI")
            width, height = jpeg_dimensions(path)
            if width < 1 or height < 1:
                raise ContractError("JPEG sem dimensões válidas")
        elif suffix == ".webp":
            size = path.stat().st_size
            with path.open("rb") as source:
                head = source.read(16)
            if (
                size < 20
                or head[:4] != b"RIFF"
                or head[8:12] != b"WEBP"
                or int.from_bytes(head[4:8], "little") + 8 != size
                or head[12:16] not in {b"VP8 ", b"VP8L", b"VP8X"}
            ):
                raise ContractError("WebP truncado ou estruturalmente inválido")
        else:
            raise ContractError("imagem deve ser PNG, JPEG ou WebP")


def _load_queue(queue_dir: Path) -> list[dict]:
    if not queue_dir.exists():
        return []
    entries: list[dict] = []
    for path in sorted(queue_dir.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ContractError(f"fila privada contém JSON inválido: {path.name}") from exc
        if not isinstance(value, dict):
            raise ContractError(f"fila privada contém registro inválido: {path.name}")
        entries.append(value)
    return entries


def _surface_state(status_value: str, gate: str) -> dict:
    return {
        "status": status_value,
        "gate": gate,
        "attempts": 0,
        "remoteId": None,
        "remoteRevision": None,
        "confirmedSha256": None,
        "lastErrorCode": None,
        "updatedAt": None,
    }


def _write_private_json(path: Path, value: dict) -> None:
    temporary = path.parent / f".{path.name}.{os.getpid()}.{secrets.token_hex(6)}.tmp"
    payload = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    descriptor = -1
    try:
        descriptor = os.open(str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fsync(descriptor)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    os.replace(temporary, path)
    os.chmod(path, 0o600)


def enqueue_intake(args: argparse.Namespace, queue_dir: Path = PRIVATE_QUEUE) -> dict:
    """Congela bytes e registra intenção privada; não chama conectores nem publica."""

    source_input = Path(args.source).expanduser()
    try:
        source_status = source_input.lstat()
    except OSError as exc:
        raise ContractError("fonte materializada ausente ou inacessível") from exc
    if stat.S_ISLNK(source_status.st_mode) or not stat.S_ISREG(source_status.st_mode):
        raise ContractError("fonte precisa ser arquivo regular e não pode ser symlink")
    source = source_input.resolve(strict=True)
    suffix = source.suffix.casefold()
    if args.kind not in SAFE_INTAKE_KINDS:
        raise ContractError(f"tipo não permitido no intake seguro: {args.kind}")
    kind = AUTO_KIND_BY_SUFFIX.get(suffix) if args.kind == "auto" else args.kind
    if kind is None:
        raise ContractError("auto reconhece somente DOCX, PDF, PNG, JPEG e WebP")
    routes = load_json(DATA / "content-routing.json").get("routes", [])
    route_matches = [item for item in routes if item.get("kind") == kind]
    if len(route_matches) != 1:
        raise ContractError(f"tipo de conteúdo não resolvido de forma única: {kind}")

    universe = args.universe.upper()
    if universe not in UNIVERSES:
        raise ContractError("universe deve ser U1, U2, U3 ou MUX")
    block_key = args.block.casefold().lstrip("#")
    block = BLOCK_ALIASES.get(block_key)
    if not block:
        raise ContractError(f"bloco desconhecido: {args.block}")
    privacy = args.privacy.upper()
    if privacy not in {"P0", "P1", "P2", "P3"}:
        raise ContractError("privacy deve ser P0, P1, P2 ou P3")
    source_project = getattr(args, "source_project", None)
    owner_completed_module = bool(getattr(args, "owner_completed_module", False))
    if source_project is not None and source_project not in SOURCE_PROJECTS:
        raise ContractError("source-project não pertence ao escopo editorial autorizado")
    if owner_completed_module and source_project != ORGANIZATION_STUDY_PROJECT:
        raise ContractError(
            "owner-completed-module só se aplica ao projeto @ORGANIZACAODEESTUDO"
        )
    if source_project == ORGANIZATION_STUDY_PROJECT:
        if block not in {"MICRO", "IMGT"}:
            raise ContractError(
                "@ORGANIZACAODEESTUDO só pode gerar projeção pública em estudo-microparticulado ou imagens-turbo-temi"
            )
        if block == "MICRO" and privacy == "P0" and not owner_completed_module:
            raise ContractError(
                "P0 bloqueado: o proprietário ainda não confirmou a conclusão integral do módulo"
            )
    independent_organization_study_image = (
        source_project == ORGANIZATION_STUDY_PROJECT and block == "IMGT"
    )
    domain = getattr(args, "domain", "clinical-educational")
    domain_contract = DOMAINS.get(domain)
    if not domain_contract:
        raise ContractError(f"domínio desconhecido: {domain}")
    domain_code = domain_contract["code"]
    private_domain = bool(domain_contract["private"])

    title = _safe_text(args.title or source.stem, "título", 160)
    objective = _safe_text(args.objective, "objetivo", 240)
    intake_date = _parse_calendar_date(args.date)
    private_root = queue_dir.parent
    blob_path, artifact_hash, artifact_size, blob_created = _snapshot_source(
        source,
        suffix,
        private_root,
    )
    try:
        validate_materialized_file(blob_path, kind, suffix)
    except Exception:
        if blob_created:
            blob_path.unlink(missing_ok=True)
        raise

    semantic_key = re.sub(
        r"[^a-z0-9]+",
        "-",
        unicodedata.normalize("NFKD", title)
        .encode("ascii", "ignore")
        .decode()
        .casefold(),
    ).strip("-")
    if not semantic_key:
        raise ContractError("título não produz chave semântica válida")
    intent_uid = hashlib.sha256(
        f"Antigravity_Consultas|{domain}|{source_project or 'sem-projeto'}|{kind}|{universe}|{block_key}|{semantic_key}".encode("utf-8")
    ).hexdigest()
    idempotency_key = hashlib.sha256(f"{artifact_hash}|{intent_uid}".encode("utf-8")).hexdigest()

    _secure_directory(private_root)
    _secure_directory(queue_dir)
    lock_path = private_root / "queue.lock"
    lock_fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o600)
    os.chmod(lock_path, 0o600)
    fcntl.flock(lock_fd, fcntl.LOCK_EX)
    try:
        existing = _load_queue(queue_dir)
        for entry in existing:
            if entry.get("idempotencyKey") == idempotency_key:
                duplicate = dict(entry)
                if entry.get("privacy") != privacy:
                    duplicate["queueResult"] = "REVIEW_REQUIRED_PRIVACY_CHANGE"
                    duplicate["requestedPrivacy"] = privacy
                elif (
                    entry.get("moduleCompletion", {}).get("ownerCompletionRecorded", False)
                    != owner_completed_module
                ):
                    duplicate["queueResult"] = "REVIEW_REQUIRED_MODULE_COMPLETION_CHANGE"
                else:
                    duplicate["queueResult"] = "SKIP_DUPLICATE"
                return duplicate

        if args.sequence is None:
            used = [
                int(entry.get("sequence", 0))
                for entry in existing
                if entry.get("date") == intake_date and isinstance(entry.get("sequence"), int)
            ]
            sequence_number = max(used, default=0) + 1
        else:
            sequence_number = args.sequence
        if sequence_number < 1 or sequence_number > 9999:
            raise ContractError("sequence deve estar entre 1 e 9999")
        sequence = f"{sequence_number:04d}"

        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
        entity_prefix = ENTITY_PREFIX_BY_KIND[kind]
        entity_code = f"####{entity_prefix}-{intake_date}-{sequence}-{artifact_hash[:8].upper()}"
        product_uid = hashlib.sha256(
            f"{artifact_hash}|{domain}|{block_key}|{semantic_key}|{privacy}".encode("utf-8")
        ).hexdigest()
        product_code = f"####AGX-{universe}-{block}-{intake_date}-{sequence}-{product_uid[:8].upper()}"
        project_suffix = hashlib.sha256(
            f"{domain}|{semantic_key}".encode("utf-8")
        ).hexdigest()[:10].upper()
        project_code = f"####PRJ-{domain_code}-{project_suffix}"
        procedure_suffix = digest8("ACOPLAR", product_code, artifact_hash, idempotency_key, timestamp)
        procedure_code = f"PRC###-ACOPLAR-{intake_date}-{sequence}-{procedure_suffix}"
        session_suffix = digest8(objective, product_code, intake_date, sequence)
        session_code = f"####SES-{intake_date}-{sequence}-{session_suffix}"
        route_item = route_matches[0]
        receipt_file = f"{idempotency_key}.json"
        if private_domain:
            drive_state = _surface_state("PENDING_ON_DEMAND", "destino privado do domínio + hash remoto")
            notion_state = _surface_state("PENDING_ON_DEMAND", "comando explícito + página privada canônica")
        elif privacy in {"P2", "P3"}:
            drive_state = _surface_state("BLOCKED_PRIVATE_TARGET", "destino clínico privado precisa ser mapeado")
            notion_state = _surface_state("BLOCKED_PRIVATE_TARGET", "base clínica privada precisa ser mapeada")
        else:
            drive_state = _surface_state("PENDING", "pasta privada canônica + hash remoto")
            notion_state = _surface_state("PENDING", "página canônica + UID idempotente")
        public_gate = "privacidade + direitos + metadados + revisão humana"
        if source_project == ORGANIZATION_STUDY_PROJECT and block == "MICRO":
            public_gate = (
                "MODULE_COMPLETED_BY_OWNER + extração de modelo limpo fechado + "
                + public_gate
            )
        elif independent_organization_study_image:
            public_gate = (
                "STANDING_OWNER_AUTHORIZATION_2026-08-01 + ####IMG + paciente + "
                "direitos + ciência quando aplicável + integridade técnica + alt + SHA-256"
            )
        entry = {
            "schemaVersion": "antigravity-nexus-private-intake-v2",
            "revision": 1,
            "queueStatus": "QUEUED_PRIVATE",
            "receiptFile": receipt_file,
            "idempotencyKey": idempotency_key,
            "artifactUid": artifact_hash,
            "intentUid": intent_uid,
            "createdAt": timestamp,
            "updatedAt": timestamp,
            "date": intake_date,
            "sequence": sequence_number,
            "entityCode": entity_code,
            "productCode": product_code,
            "productUid": product_uid,
            "semanticKey": semantic_key,
            "procedureCode": procedure_code,
            "sessionCode": session_code,
            "projectCode": project_code,
            "sourceProjectAlias": source_project,
            "moduleCompletion": {
                "status": (
                    "INDEPENDENT_IMAGE_LANE"
                    if independent_organization_study_image
                    else (
                    "MODULE_COMPLETED_BY_OWNER"
                    if owner_completed_module
                    else "PRIVATE_WORK_IN_PROGRESS"
                    )
                ),
                "ownerCompletionRecorded": owner_completed_module,
                "publicExtractionAllowed": (
                    owner_completed_module or independent_organization_study_image
                ),
            },
            "title": title,
            "objective": objective,
            "kind": kind,
            "block": block,
            "universe": universe,
            "privacy": privacy,
            "domain": domain,
            "domainCode": domain_code,
            "structuralTags": [
                f"###DOMINIO:{domain_code}",
                f"###UNIVERSO:{universe}",
                f"###BLOCO:{block}",
                "###STATUS:RASCUNHO",
                f"###PRIVACIDADE:{privacy}",
            ],
            "source": {
                "blobPath": str(blob_path.relative_to(private_root)),
                "sha256": artifact_hash,
                "sizeBytes": artifact_size,
                "mime": mimetypes.guess_type(source.name)[0] or "application/octet-stream",
                "originalNameHash": hashlib.sha256(source.name.encode("utf-8")).hexdigest(),
            },
            "route": {
                "canonicalSection": route_item.get("canonicalSection"),
                "catalog": route_item.get("catalog"),
                "destination": route_item.get("destination"),
                "gate": route_item.get("gate"),
            },
            "surfaces": {
                "drive": drive_state,
                "notion": notion_state,
                "githubDraft": _surface_state(
                    "BLOCKED_PRIVATE_DOMAIN" if private_domain else (
                        "BLOCKED_PRIVATE" if privacy != "P0" else "BLOCKED_GATES"
                    ),
                    "domínio não público" if private_domain else public_gate,
                ),
                "library": _surface_state(
                    "BLOCKED_PRIVATE_DOMAIN" if private_domain else (
                        "BLOCKED_PRIVATE" if privacy != "P0" else "BLOCKED_GATES"
                    ),
                    "domínio não público" if private_domain else public_gate + " + preview fail-closed",
                ),
                "officialSite": _surface_state(
                    "BLOCKED_PRIVATE_DOMAIN" if private_domain else (
                        "BLOCKED_GATES_STANDING_AUTH"
                        if independent_organization_study_image and privacy == "P0"
                        else "LOCKED"
                    ),
                    "domínio não público" if private_domain else (
                        (
                            "AUD### + HOM### + TOM### + TAF### + autorização permanente exclusiva da imagem"
                            if independent_organization_study_image
                            else "AUD### + HOM### + TOM### + TAF### + comando literal do proprietário"
                        )
                    ),
                ),
            },
            "attestations": {
                "privacyReviewed": False,
                "patientExposureReviewed": False,
                "rightsReviewed": False,
                "metadataSanitized": False,
                "clinicalReviewed": False,
                "scientificGroundingReviewed": False,
                "technicalReviewed": False,
                "ownerModuleCompletionRecorded": owner_completed_module,
                "auditCode": None,
            },
            "events": [
                {
                    "at": timestamp,
                    "type": "INTAKE_SNAPSHOTTED",
                    "procedureCode": procedure_code,
                    "artifactSha256": artifact_hash,
                    "result": "QUEUED_PRIVATE",
                }
            ],
            "publication": {
                "status": "LOCKED",
                "requiredCommand": "PUBLICAR {TAF###-EXATO}",
                "authorizationMode": (
                    "STANDING_OWNER_AUTHORIZATION_2026-08-01"
                    if independent_organization_study_image
                    else "LITERAL_OWNER_COMMAND"
                ),
                "tafCode": None,
            },
        }
        target = queue_dir / receipt_file
        _write_private_json(target, entry)
        result = dict(entry)
        result["queueResult"] = "QUEUED_PRIVATE"
        return result
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)


def sync_plan(queue_dir: Path = PRIVATE_QUEUE) -> dict:
    """Resume a fila sem revelar títulos, paths ou dados do conteúdo."""

    entries = _load_queue(queue_dir)
    items = []
    for entry in entries:
        surfaces = entry.get("surfaces", {})
        items.append(
            {
                "receiptFile": entry.get("receiptFile"),
                "entityCode": entry.get("entityCode"),
                "projectCode": entry.get("projectCode"),
                "productCode": entry.get("productCode"),
                "procedureCode": entry.get("procedureCode"),
                "privacy": entry.get("privacy"),
                "domain": entry.get("domain", "clinical-educational"),
                "surfaceStates": {
                    name: value.get("status") if isinstance(value, dict) else "INVALID"
                    for name, value in surfaces.items()
                },
                "publication": entry.get("publication", {}).get("status"),
            }
        )
    return {
        "schemaVersion": "antigravity-nexus-sync-plan-v1",
        "items": items,
        "count": len(items),
        "publication": "LOCKED",
    }


def _json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _load_json_path(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} ausente ou inválido") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{label} precisa ser objeto JSON")
    return value


def _aware_timestamp(value: str, field: str) -> str:
    normalized = _safe_text(value, field, 48)
    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"{field} precisa ser timestamp ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ContractError(f"{field} precisa informar fuso horário")
    return normalized


def _reject_sensitive_public_text(value: str, field: str) -> str:
    normalized = _safe_text(value, field, 600)
    lowered = normalized.casefold()
    forbidden = (
        "/users/",
        "\\users\\",
        "authorization: bearer",
        "password=",
        "passwd=",
        "token=",
        "access_token",
        "ghp_",
        "github_pat_",
        "sk-",
    )
    if any(marker in lowered for marker in forbidden):
        raise ContractError(f"{field} contém caminho privado ou possível segredo")
    if re.search(r"https?://\S+[?&][^\s=]+=", normalized, flags=re.IGNORECASE):
        raise ContractError(f"{field} contém URL com parâmetros potencialmente sensíveis")
    return normalized


def _validate_release_evidence(
    path: Path,
    product_code: str,
    audit_code: str,
    artifact_root: str,
) -> tuple[dict, str]:
    try:
        status_value = path.lstat()
    except OSError as exc:
        raise ContractError("evidência de homologação ausente") from exc
    if stat.S_ISLNK(status_value.st_mode) or not stat.S_ISREG(status_value.st_mode):
        raise ContractError("evidência de homologação precisa ser arquivo regular")
    if status_value.st_size < 2 or status_value.st_size > 256 * 1024:
        raise ContractError("evidência de homologação excede o limite seguro")
    evidence = _load_json_path(path, "evidência de homologação")
    allowed = {
        "schemaVersion",
        "productCode",
        "reviewer",
        "reviewedAt",
        "confirmations",
        "auditBinding",
        "testRuns",
        "notes",
    }
    if set(evidence) - allowed:
        raise ContractError("evidência contém campos não contratados")
    if evidence.get("schemaVersion") != "antigravity-release-evidence-v1":
        raise ContractError("schema da evidência de homologação é incompatível")
    if evidence.get("productCode") != product_code:
        raise ContractError("evidência aponta para outro produto")
    evidence["reviewer"] = _reject_sensitive_public_text(
        evidence.get("reviewer", ""), "reviewer"
    )
    evidence["reviewedAt"] = _aware_timestamp(
        evidence.get("reviewedAt", ""), "reviewedAt"
    )

    confirmations = evidence.get("confirmations")
    if not isinstance(confirmations, dict) or set(confirmations) != RELEASE_CONFIRMATIONS:
        raise ContractError("evidência precisa conter as quatro confirmações de homologação")
    failed = sorted(
        key for key, value in confirmations.items() if value != "PASS"
    )
    if failed:
        raise ContractError("homologação não aprovada: " + ", ".join(failed))

    audit_binding = evidence.get("auditBinding")
    if not isinstance(audit_binding, dict) or set(audit_binding) != {
        "auditCode", "artifactRootSha256", "status"
    }:
        raise ContractError("evidência precisa vincular AUD### ao root físico atual")
    if (
        audit_binding.get("auditCode") != audit_code
        or audit_binding.get("artifactRootSha256") != artifact_root
        or audit_binding.get("status") != "PASS"
    ):
        raise ContractError("reauditoria não está vinculada ao lote físico atual")

    test_runs = evidence.get("testRuns")
    if not isinstance(test_runs, list) or not test_runs or len(test_runs) > 50:
        raise ContractError("evidência precisa registrar ao menos um teste executado")
    test_ids: set[str] = set()
    for item in test_runs:
        if not isinstance(item, dict) or set(item) != {
            "id", "command", "status", "summary", "executedAt"
        }:
            raise ContractError("registro de teste possui campos inválidos")
        test_id = token(str(item.get("id", "")), "testRuns.id")
        if test_id in test_ids:
            raise ContractError("registro de teste duplicado")
        test_ids.add(test_id)
        item["id"] = test_id
        item["command"] = _reject_sensitive_public_text(
            str(item.get("command", "")), "testRuns.command"
        )
        item["summary"] = _reject_sensitive_public_text(
            str(item.get("summary", "")), "testRuns.summary"
        )
        item["executedAt"] = _aware_timestamp(
            str(item.get("executedAt", "")), "testRuns.executedAt"
        )
        if item.get("status") != "PASS":
            raise ContractError(f"teste {test_id} não possui resultado PASS")

    notes = evidence.get("notes", [])
    if not isinstance(notes, list) or len(notes) > 20:
        raise ContractError("notes precisa ser lista curta")
    evidence["notes"] = [
        _reject_sensitive_public_text(str(note), "notes") for note in notes
    ]
    return evidence, sha256_file(path)


def _relative_regular_file(base: Path, relative: str, root: Path) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ContractError("membro do produto possui path inválido")
    relative_path = Path(relative)
    if relative_path.is_absolute() or any(part in {"", ".", ".."} for part in relative_path.parts):
        raise ContractError(f"membro do produto escapa do diretório: {relative}")
    candidate = base / relative_path
    current = base
    for part in relative_path.parts:
        current = current / part
        try:
            current_status = current.lstat()
        except OSError as exc:
            raise ContractError(f"membro materializado ausente: {relative}") from exc
        if stat.S_ISLNK(current_status.st_mode):
            raise ContractError(f"membro materializado não pode ser symlink: {relative}")
    if not candidate.is_file():
        raise ContractError(f"membro materializado não é arquivo: {relative}")
    try:
        candidate.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise ContractError(f"membro materializado está fora do projeto: {relative}") from exc
    return candidate


def _resolve_public_root(public_root: Path | None, source_root: Path) -> Path:
    """Resolve uma raiz pública materializada sem aceitar atalhos ambíguos."""

    if public_root is None:
        raise ContractError(
            "--public-root é obrigatório para o perfil POST_BUILD_POST_SANITIZE"
        )
    candidate = Path(public_root).expanduser()
    try:
        status_value = candidate.lstat()
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise ContractError("public-root materializado está ausente") from exc
    if stat.S_ISLNK(status_value.st_mode) or not stat.S_ISDIR(status_value.st_mode):
        raise ContractError("public-root precisa ser diretório regular, não symlink")
    if resolved == Path(resolved.anchor) or resolved == source_root.resolve(strict=True):
        raise ContractError(
            "public-root precisa ser uma saída dedicada, distinta da fonte"
        )
    return resolved


def _release_artifact_profile(product: dict, manifest: dict) -> str:
    """Exige uma única declaração explícita do estágio que fornece os bytes."""

    product_release = product.get("releasePreparation")
    manifest_release = manifest.get("releasePreparation")
    if product_release is not None and not isinstance(product_release, dict):
        raise ContractError("releasePreparation do catálogo precisa ser objeto")
    if manifest_release is not None and not isinstance(manifest_release, dict):
        raise ContractError("releasePreparation do manifesto precisa ser objeto")
    declarations = [
        product.get("artifactProfile"),
        (product_release or {}).get("artifactProfile"),
        manifest.get("artifactProfile"),
        (manifest_release or {}).get("artifactProfile"),
    ]
    profiles = {value for value in declarations if value is not None}
    if not profiles:
        # Registros preparados antes da introdução do perfil continuam
        # verificáveis como source-bound. Novas preparações precisam declarar
        # o perfil para não tombar a árvore-fonte por acidente.
        if product.get("tafCode") is not None:
            return SOURCE_BOUND
        raise ContractError(
            "artifactProfile explícito é obrigatório: SOURCE_BOUND ou "
            "POST_BUILD_POST_SANITIZE"
        )
    if len(profiles) != 1 or not profiles.issubset(RELEASE_ARTIFACT_PROFILES):
        raise ContractError("artifactProfile ausente, inválido ou divergente")
    return next(iter(profiles))


def _validate_release_html_state(path: Path) -> None:
    try:
        page_text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ContractError("HTML tombável ausente ou inválido") from exc
    normalized_page = (
        unicodedata.normalize("NFKD", page_text)
        .encode("ascii", "ignore")
        .decode()
        .casefold()
    )
    transient_markers = {
        "candidate_public",
        "candidato publico",
        "estado candidato",
        "sem taf",
        "sem hom",
        "ainda nao e aceite",
        "nao publicada",
        "nao representa aceite ou publicacao",
    }
    found = sorted(marker for marker in transient_markers if marker in normalized_page)
    if found:
        raise ContractError(
            "HTML ainda contém estado editorial transitório: " + ", ".join(found)
        )


def _umbrella_release_artifact_inventory(
    root: Path,
    manifest_path: Path,
    manifest: dict,
) -> tuple[list[dict], str]:
    """Valida um lote guarda-chuva explícito, P0 e limitado ao repositório."""

    allowed_manifest_fields = {
        "schemaVersion",
        "artifactProfile",
        "identity",
        "classification",
        "publication",
        "memberRoot",
        "members",
        "bundle",
        "audit",
        "releasePreparation",
        "supersededReleases",
    }
    extra_manifest_fields = sorted(set(manifest) - allowed_manifest_fields)
    if extra_manifest_fields:
        raise ContractError(
            "manifesto guarda-chuva contém campos não contratados: "
            + ", ".join(extra_manifest_fields)
        )

    member_root_value = manifest.get("memberRoot")
    if (
        not isinstance(member_root_value, str)
        or not member_root_value
        or "\\" in member_root_value
    ):
        raise ContractError("memberRoot do guarda-chuva é inválido")
    repository_wide = member_root_value == "."
    member_root = Path(member_root_value)
    if not repository_wide and (
        member_root.is_absolute()
        or any(part in {"", ".", ".."} for part in member_root.parts)
        or member_root.as_posix() != member_root_value
    ):
        raise ContractError(
            "memberRoot precisa ser '.' ou caminho normalizado relativo ao repositório"
        )
    current = root
    for part in member_root.parts:
        current = current / part
        try:
            current_status = current.lstat()
        except OSError as exc:
            raise ContractError("memberRoot materializado está ausente") from exc
        if stat.S_ISLNK(current_status.st_mode):
            raise ContractError("memberRoot não pode atravessar symlink")
    if not current.is_dir():
        raise ContractError("memberRoot precisa apontar para diretório regular")

    declared_members = manifest.get("members")
    if (
        not isinstance(declared_members, list)
        or not declared_members
        or len(declared_members) > MAX_RELEASE_MEMBERS
    ):
        raise ContractError("members do guarda-chuva precisa ser lista não vazia e limitada")

    manifest_relative = manifest_path.relative_to(root).as_posix()
    mutable_governance_paths = {
        "23_Cosmos_NEXUS/module.manifest.json",
        "23_Cosmos_NEXUS/data/product-catalog.json",
        "23_Cosmos_NEXUS/data/execution-ledger.json",
        "23_Cosmos_NEXUS/data/tombstone-manifest.json",
        "23_Cosmos_NEXUS/data/homologation-reports.json",
    }
    seen_paths: set[str] = set()
    image_codes: set[str] = set()
    members: list[dict] = []
    declared_paths: list[str] = []
    for member in declared_members:
        if not isinstance(member, dict):
            raise ContractError("membro do guarda-chuva precisa ser objeto JSON")
        kind = member.get("kind")
        expected_fields = (
            {"path", "kind", "sha256", "bytes", "catalogCode"}
            if kind == "image"
            else {"path", "kind", "sha256", "bytes"}
        )
        if set(member) != expected_fields or kind not in {"file", "image"}:
            raise ContractError("membro do guarda-chuva possui campos ou kind inválidos")

        relative = member.get("path")
        if not isinstance(relative, str):
            raise ContractError("membro do guarda-chuva possui path inválido")
        relative_path = Path(relative)
        if relative_path.as_posix() != relative:
            raise ContractError(f"membro possui path não normalizado: {relative}")
        if not repository_wide:
            try:
                relative_path.relative_to(member_root)
            except ValueError as exc:
                raise ContractError(f"membro está fora de memberRoot: {relative}") from exc
        if any(part.startswith(".") for part in relative_path.parts):
            raise ContractError(f"membro oculto ou privado não pode ser tombado: {relative}")
        if (
            relative == manifest_relative
            or relative in mutable_governance_paths
            or relative.startswith("23_Cosmos_NEXUS/data/release-reports/")
        ):
            raise ContractError(f"metadado de governança mutável não pode ser membro: {relative}")
        if relative in seen_paths:
            raise ContractError(f"membro duplicado no guarda-chuva: {relative}")
        seen_paths.add(relative)
        declared_paths.append(relative)

        path = _relative_regular_file(root, relative, root)
        actual_hash = sha256_file(path)
        actual_size = path.stat().st_size
        if (
            not HEX64.fullmatch(str(member.get("sha256", "")))
            or member.get("sha256") != actual_hash
            or not isinstance(member.get("bytes"), int)
            or isinstance(member.get("bytes"), bool)
            or member.get("bytes") != actual_size
            or actual_size > MAX_FILE_BYTES
        ):
            raise ContractError(f"membro diverge dos bytes reais: {relative}")

        suffix = path.suffix.casefold()
        if kind == "image":
            if suffix not in UMBRELLA_IMAGE_SUFFIXES:
                raise ContractError(f"kind image possui formato não permitido: {relative}")
            code = member.get("catalogCode", "")
            if (
                not IMG.fullmatch(code)
                or not code.endswith(actual_hash[:8].upper())
                or code in image_codes
            ):
                raise ContractError(f"imagem não possui ####IMG único e coerente: {relative}")
            image_codes.add(code)
            validate_materialized_file(path, "gpt-image", suffix)
        else:
            if suffix not in UMBRELLA_FILE_SUFFIXES:
                raise ContractError(f"arquivo guarda-chuva possui formato não permitido: {relative}")
            if suffix == ".pdf":
                validate_materialized_file(path, "gpt-pdf", suffix)
            elif suffix == ".html":
                _validate_release_html_state(path)
            elif suffix == ".json":
                try:
                    json.loads(path.read_text(encoding="utf-8"))
                except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise ContractError(f"JSON tombável inválido: {relative}") from exc

        record = {
            "path": relative,
            "sha256": actual_hash,
            "bytes": actual_size,
            "kind": kind,
        }
        if kind == "image":
            record["catalogCode"] = member["catalogCode"]
        members.append(record)

    if declared_paths != sorted(declared_paths):
        raise ContractError("members do guarda-chuva precisa estar ordenado por path")

    root_lines = "".join(
        f"{member['path']}\t{member['sha256']}\t{member['bytes']}\n"
        for member in members
    )
    artifact_root = hashlib.sha256(root_lines.encode("utf-8")).hexdigest()
    bundle = manifest.get("bundle")
    expected_bundle_fields = {
        "inventoryPolicy",
        "memberRootAlgorithm",
        "memberCount",
        "totalBytes",
        "aggregateSha256",
    }
    if not isinstance(bundle, dict) or set(bundle) != expected_bundle_fields:
        raise ContractError("bundle do guarda-chuva possui campos inválidos")
    if (
        bundle.get("inventoryPolicy") != UMBRELLA_INVENTORY_POLICY
        or bundle.get("memberRootAlgorithm") != UMBRELLA_ROOT_ALGORITHM
        or bundle.get("memberCount") != len(members)
        or bundle.get("totalBytes") != sum(member["bytes"] for member in members)
        or bundle.get("aggregateSha256") != artifact_root
    ):
        raise ContractError("bundle do guarda-chuva diverge do inventário físico")

    identity = manifest.get("identity", {})
    audit = manifest.get("audit", {})
    audit_evidence = audit.get("auditEvidenceSha256")
    audit_input = "|".join(
        [
            identity.get("productCode", ""),
            artifact_root,
            "patient:passed",
            "rights:passed",
            "science:passed",
            "technical:passed",
            "links:passed",
        ]
    )
    expected_evidence = hashlib.sha256(audit_input.encode("utf-8")).hexdigest()
    if (
        audit_evidence != expected_evidence
        or not AUD.fullmatch(identity.get("auditCode", ""))
        or not identity.get("auditCode", "").endswith(expected_evidence[:8].upper())
    ):
        raise ContractError("AUD### do guarda-chuva não corresponde ao bundle atual")
    return members, artifact_root


def _release_artifact_inventory(
    root: Path,
    manifest_path: Path,
    manifest: dict,
) -> tuple[list[dict], str]:
    if manifest.get("schemaVersion") == UMBRELLA_RELEASE_SCHEMA:
        return _umbrella_release_artifact_inventory(root, manifest_path, manifest)
    base = manifest_path.parent
    entrypoints = manifest.get("entrypoints")
    if not isinstance(entrypoints, dict) or set(entrypoints) != {
        "page", "styles", "references"
    }:
        raise ContractError("manifesto candidato precisa declarar page, styles e references")
    declared: dict[str, Path] = {}
    for kind, relative in entrypoints.items():
        path = _relative_regular_file(base, relative, root)
        if relative in declared:
            raise ContractError("entrypoint duplicado no manifesto candidato")
        declared[relative] = path
        if kind == "page":
            try:
                page_text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                raise ContractError("entrypoint HTML ausente ou inválido") from exc
            normalized_page = (
                unicodedata.normalize("NFKD", page_text)
                .encode("ascii", "ignore")
                .decode()
                .casefold()
            )
            transient_markers = {
                "candidate_public",
                "candidato publico",
                "estado candidato",
                "sem taf",
                "sem hom",
                "ainda nao e aceite",
                "nao publicada",
                "nao representa aceite ou publicacao",
            }
            found = sorted(marker for marker in transient_markers if marker in normalized_page)
            if found:
                raise ContractError(
                    "HTML ainda contém estado editorial transitório: " + ", ".join(found)
                )

    assets = manifest.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ContractError("manifesto candidato não possui assets tombáveis")
    asset_codes: set[str] = set()
    for asset in assets:
        if not isinstance(asset, dict):
            raise ContractError("asset do manifesto candidato é inválido")
        relative = asset.get("path")
        path = _relative_regular_file(base, relative, root)
        if relative in declared:
            raise ContractError(f"membro declarado mais de uma vez: {relative}")
        declared[relative] = path
        actual_hash = sha256_file(path)
        actual_size = path.stat().st_size
        if asset.get("sha256") != actual_hash or asset.get("bytes") != actual_size:
            raise ContractError(f"asset diverge dos bytes reais: {relative}")
        code = asset.get("catalogCode", "")
        if not IMG.fullmatch(code) or not code.endswith(actual_hash[:8].upper()):
            raise ContractError(f"asset não possui ####IMG coerente: {relative}")
        if code in asset_codes:
            raise ContractError("manifesto candidato contém ####IMG duplicado")
        asset_codes.add(code)
        suffix = path.suffix.casefold()
        if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
            validate_materialized_file(path, "gpt-image", suffix)
        if suffix == ".png" and isinstance(asset.get("width"), int) and isinstance(asset.get("height"), int):
            with path.open("rb") as source:
                source.seek(16)
                dimensions = (
                    int.from_bytes(source.read(4), "big"),
                    int.from_bytes(source.read(4), "big"),
                )
            if dimensions != (asset["width"], asset["height"]):
                raise ContractError(f"dimensões do PNG divergentes: {relative}")

    bundle = manifest.get("bundle")
    if not isinstance(bundle, dict):
        raise ContractError("manifesto candidato não possui bundle verificável")
    if bundle.get("assetCount") != len(assets) or bundle.get("totalBytes") != sum(
        asset.get("bytes", -1) for asset in assets
    ):
        raise ContractError("contagem ou bytes agregados do bundle divergem")
    if "assetCatalogAlgorithm" in bundle and "assetRootAlgorithm" not in bundle:
        aggregate_input = "".join(
            f"{asset['slot']}\t{asset['sha256']}\t{asset['bytes']}\n"
            for asset in sorted(assets, key=lambda value: value["slot"])
        )
    elif "assetRootAlgorithm" in bundle and "assetCatalogAlgorithm" not in bundle:
        aggregate_input = "|".join(sorted(asset["sha256"] for asset in assets))
    else:
        raise ContractError("bundle precisa declarar um único algoritmo agregado conhecido")
    aggregate_hash = hashlib.sha256(aggregate_input.encode("utf-8")).hexdigest()
    if bundle.get("aggregateSha256") != aggregate_hash:
        raise ContractError("aggregateSha256 do bundle diverge dos assets reais")

    audit = manifest.get("audit", {})
    audit_evidence = audit.get("auditEvidenceSha256")
    if audit_evidence is not None:
        identity = manifest.get("identity", {})
        audit_input = "|".join(
            [
                identity.get("productCode", ""),
                aggregate_hash,
                "patient:passed",
                "rights:passed",
                "science:passed",
                "technical:passed",
                "links:passed",
            ]
        )
        expected_evidence = hashlib.sha256(audit_input.encode("utf-8")).hexdigest()
        if (
            audit_evidence != expected_evidence
            or not identity.get("auditCode", "").endswith(expected_evidence[:8].upper())
        ):
            raise ContractError("AUD### ou auditEvidenceSha256 não corresponde ao bundle atual")

    actual = {
        path.relative_to(base).as_posix()
        for path in base.rglob("*")
        if path.is_file() and path != manifest_path
    }
    if actual != set(declared):
        missing = sorted(set(declared) - actual)
        extra = sorted(actual - set(declared))
        detail = []
        if missing:
            detail.append("ausentes=" + ",".join(missing))
        if extra:
            detail.append("não declarados=" + ",".join(extra))
        raise ContractError("lote físico não coincide com o manifesto: " + "; ".join(detail))

    members = []
    for relative, path in sorted(declared.items()):
        members.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )
    root_lines = "".join(
        f"{member['path']}\t{member['sha256']}\t{member['bytes']}\n"
        for member in members
    )
    return members, hashlib.sha256(root_lines.encode("utf-8")).hexdigest()


def _release_public_artifact_inventory(
    root: Path,
    public_root: Path | None,
    manifest_path: Path,
    manifest: dict,
) -> tuple[list[dict], str]:
    """Tomba os mesmos membros permitidos pela fonte, usando os bytes públicos."""

    source_members, _ = _release_artifact_inventory(root, manifest_path, manifest)
    public_root = _resolve_public_root(public_root, root)
    public_members: list[dict] = []
    for source_member in source_members:
        relative = source_member["path"]
        path = _relative_regular_file(public_root, relative, public_root)
        actual_size = path.stat().st_size
        if actual_size > MAX_FILE_BYTES:
            raise ContractError(f"membro público excede o limite seguro: {relative}")
        suffix = path.suffix.casefold()
        if suffix in UMBRELLA_IMAGE_SUFFIXES:
            validate_materialized_file(path, "gpt-image", suffix)
        elif suffix == ".pdf":
            validate_materialized_file(path, "gpt-pdf", suffix)
        elif suffix == ".html":
            _validate_release_html_state(path)
        elif suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ContractError(f"JSON público tombável inválido: {relative}") from exc

        record = {
            "path": relative,
            "sha256": sha256_file(path),
            "bytes": actual_size,
        }
        if source_member.get("kind") is not None:
            record["kind"] = source_member["kind"]
        if source_member.get("catalogCode") is not None:
            code = source_member["catalogCode"]
            if not code.endswith(record["sha256"][:8].upper()):
                raise ContractError(
                    f"####IMG público diverge dos bytes catalogados: {relative}"
                )
            record["catalogCode"] = code
        public_members.append(record)

    if manifest.get("schemaVersion") != UMBRELLA_RELEASE_SCHEMA:
        manifest_relative = manifest_path.relative_to(root).as_posix()
        product_relative = manifest_path.parent.relative_to(root)
        public_product = public_root / product_relative
        try:
            product_status = public_product.lstat()
        except OSError as exc:
            raise ContractError("diretório público do produto está ausente") from exc
        if stat.S_ISLNK(product_status.st_mode) or not stat.S_ISDIR(product_status.st_mode):
            raise ContractError("diretório público do produto é inseguro")
        actual_paths: set[str] = set()
        for path in public_product.rglob("*"):
            try:
                path_status = path.lstat()
            except OSError as exc:
                raise ContractError("lote público contém membro inacessível") from exc
            relative = path.relative_to(public_root).as_posix()
            if stat.S_ISLNK(path_status.st_mode):
                raise ContractError(f"lote público contém symlink: {relative}")
            if stat.S_ISREG(path_status.st_mode) and relative != manifest_relative:
                actual_paths.add(relative)
            elif not (
                stat.S_ISDIR(path_status.st_mode)
                or stat.S_ISREG(path_status.st_mode)
            ):
                raise ContractError(f"lote público contém membro inseguro: {relative}")
        declared_paths = {member["path"] for member in public_members}
        if actual_paths != declared_paths:
            missing = sorted(declared_paths - actual_paths)
            extra = sorted(actual_paths - declared_paths)
            detail = []
            if missing:
                detail.append("ausentes=" + ",".join(missing))
            if extra:
                detail.append("não declarados=" + ",".join(extra))
            raise ContractError(
                "lote público não coincide com o manifesto: " + "; ".join(detail)
            )

    root_lines = "".join(
        f"{member['path']}\t{member['sha256']}\t{member['bytes']}\n"
        for member in public_members
    )
    return public_members, hashlib.sha256(root_lines.encode("utf-8")).hexdigest()


def _release_inventory_for_profile(
    root: Path,
    manifest_path: Path,
    manifest: dict,
    artifact_profile: str,
    public_root: Path | None,
) -> tuple[list[dict], str]:
    if artifact_profile == SOURCE_BOUND:
        return _release_artifact_inventory(root, manifest_path, manifest)
    if artifact_profile == POST_BUILD_POST_SANITIZE:
        return _release_public_artifact_inventory(
            root,
            public_root,
            manifest_path,
            manifest,
        )
    raise ContractError("artifactProfile inválido")


def _event_hash(event: dict) -> str:
    payload = dict(event)
    payload.pop("eventHash", None)
    return _canonical_sha256(payload)


def _validate_execution_ledger(ledger: dict) -> str:
    events = ledger.get("events")
    if not isinstance(events, list):
        raise ContractError("ledger de execução não possui events")
    previous = ZERO_HASH
    codes: set[str] = set()
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ContractError(f"evento inválido no ledger: {index}")
        missing = {
            "code",
            "type",
            "subjectCode",
            "timestamp",
            "inputHash",
            "outputHash",
            "result",
            "evidence",
            "previousEventHash",
            "eventHash",
        } - set(event)
        if missing:
            raise ContractError(
                f"evento {index} incompleto: " + ", ".join(sorted(missing))
            )
        code = event.get("code", "")
        if code in codes or not any(
            regex.fullmatch(code) for regex in (PRC, AUD, HOM, TOM, TAF)
        ):
            raise ContractError(f"code inválido ou duplicado no ledger: {code}")
        codes.add(code)
        if not AGX.fullmatch(event.get("subjectCode", "")):
            raise ContractError(f"subjectCode inválido no ledger: {code}")
        _aware_timestamp(event.get("timestamp", ""), f"timestamp do evento {code}")
        if not HEX64.fullmatch(event.get("inputHash", "")) or not HEX64.fullmatch(
            event.get("outputHash", "")
        ):
            raise ContractError(f"inputHash/outputHash inválido no ledger: {code}")
        if not isinstance(event.get("evidence"), dict):
            raise ContractError(f"evidence inválida no ledger: {code}")
        if event.get("previousEventHash") != previous:
            raise ContractError(f"cadeia append-only rompida no evento {code}")
        calculated = _event_hash(event)
        if event.get("eventHash") != calculated:
            raise ContractError(f"hash do evento divergente no ledger: {code}")
        previous = calculated
    head = ledger.get("ledgerHeadSha256", ZERO_HASH)
    if head != previous:
        raise ContractError("ledgerHeadSha256 diverge da cadeia de eventos")
    return previous


def _append_ledger_event(ledger: dict, event: dict) -> None:
    previous = _validate_execution_ledger(ledger)
    if any(item.get("code") == event.get("code") for item in ledger["events"]):
        raise ContractError(f"ledger já contém o código {event.get('code')}")
    record = copy.deepcopy(event)
    record["previousEventHash"] = previous
    record["eventHash"] = _event_hash(record)
    ledger["events"].append(record)
    ledger["ledgerHeadSha256"] = record["eventHash"]


def _transactional_json_update(
    updates: dict[Path, dict],
    post_validate,
    *,
    fail_after: int | None = None,
) -> None:
    """Substitui um conjunto de JSONs sob uma única janela de rollback."""

    originals: dict[Path, tuple[bytes, int] | None] = {}
    staged: dict[Path, Path] = {}
    created_directories: list[Path] = []
    replaced: list[Path] = []
    try:
        for path, value in updates.items():
            missing = []
            parent = path.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for directory in reversed(missing):
                directory.mkdir(mode=0o755)
                created_directories.append(directory)
            if path.exists():
                status_value = path.lstat()
                if stat.S_ISLNK(status_value.st_mode) or not stat.S_ISREG(status_value.st_mode):
                    raise ContractError(f"destino transacional inseguro: {path.name}")
                originals[path] = (path.read_bytes(), stat.S_IMODE(status_value.st_mode))
            else:
                originals[path] = None
            temporary = path.parent / f".{path.name}.{os.getpid()}.{secrets.token_hex(8)}.tmp"
            descriptor = os.open(
                str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644
            )
            try:
                payload = _json_bytes(value)
                view = memoryview(payload)
                while view:
                    written = os.write(descriptor, view)
                    view = view[written:]
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            staged[path] = temporary

        for index, (path, temporary) in enumerate(staged.items(), start=1):
            os.replace(temporary, path)
            replaced.append(path)
            if fail_after is not None and index >= fail_after:
                raise OSError("falha transacional injetada para teste")
        for parent in {path.parent for path in updates}:
            descriptor = os.open(str(parent), os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
        post_validate()
    except Exception:
        for path in reversed(replaced):
            original = originals[path]
            if original is None:
                path.unlink(missing_ok=True)
                continue
            payload, mode = original
            temporary = path.parent / f".{path.name}.{os.getpid()}.{secrets.token_hex(8)}.rollback"
            descriptor = os.open(
                str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode
            )
            try:
                view = memoryview(payload)
                while view:
                    written = os.write(descriptor, view)
                    view = view[written:]
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            os.replace(temporary, path)
            os.chmod(path, mode)
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                pass
        raise
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)


def _release_code_parts(code: str, prefix: str) -> tuple[str, str, int, str]:
    match = re.fullmatch(
        rf"{re.escape(prefix)}-(.+)-(\d{{8}})-(\d{{4}})-([A-F0-9]{{8}})",
        code,
    )
    if not match:
        raise ContractError(f"código {prefix} inválido: {code}")
    return match.group(1), match.group(2), int(match.group(3)), match.group(4)


def _validate_candidate_for_release(product: dict, manifest: dict) -> None:
    identity = manifest.get("identity", {})
    if manifest.get("schemaVersion") not in {
        "antigravity-candidate-product-manifest-v1",
        UMBRELLA_RELEASE_SCHEMA,
    }:
        raise ContractError("produto não usa manifesto candidato homologável")
    if identity.get("productCode") != product.get("productCode"):
        raise ContractError("catálogo e manifesto divergem no ####AGX")
    audit_code = identity.get("auditCode")
    if not AUD.fullmatch(audit_code or "") or product.get("auditCode") != audit_code:
        raise ContractError("produto não possui AUD### coerente")
    classification = manifest.get("classification", {})
    if not (
        classification.get("privacy") == "P0"
        and classification.get("patientData") is False
        and classification.get("publicEligible") is True
    ):
        raise ContractError("somente produto P0, sem paciente e elegível pode ser preparado")
    publication = manifest.get("publication", {})
    if publication.get("officialPublication") is not False or product.get("published") is not False:
        raise ContractError("produto já publicado não pode ser repreparado")
    if publication.get("finalAcceptanceCode") is not None:
        raise ContractError("manifesto já possui aceite final; use a validação idempotente")
    audit = manifest.get("audit", {})
    if audit.get("outcome") != "PASS":
        raise ContractError("auditoria do produto não está aprovada")
    required_audit = {
        "patientExposure",
        "rightsReview",
        "scientificGrounding",
        "technicalReview",
        "linkCheck",
    }
    failed = sorted(
        field
        for field in required_audit
        if audit.get(field, {}).get("status") not in {"passed", "corrected-and-rechecked"}
    )
    if failed:
        raise ContractError("auditoria incompleta: " + ", ".join(failed))
    if product.get("gates", {}).get("automatedTechnical") not in {
        "APROVADO_LOCAL", "APROVADO"
    }:
        raise ContractError("gate técnico automatizado do catálogo não está aprovado")
    if product.get("gates", {}).get("ownerUnlock") != "AUSENTE":
        raise ContractError("owner unlock não deve anteceder o TAF###")


def _default_tombstone_manifest() -> dict:
    return {
        "schemaVersion": "antigravity-tombstone-manifest-v1",
        "version": "1.0.0",
        "updatedAt": None,
        "items": [],
        "rules": [
            "Membros tombados são arquivos físicos declarados no manifesto candidato ou guarda-chuva.",
            "O manifesto-fonte é metadado de governança mutável e não integra o artifactRootSha256.",
            "TOM### e TAF### preparados não publicam, não fazem merge e não liberam GitHub Pages.",
        ],
    }


def _default_homologation_reports() -> dict:
    return {
        "schemaVersion": "antigravity-homologation-reports-v1",
        "version": "1.0.0",
        "updatedAt": None,
        "items": [],
        "rules": [
            "Relatórios aprovados são acrescentados; registros anteriores não são editados.",
            "HOM### registra homologação, mas não autoriza merge, Pages ou publicação.",
        ],
    }


def _validate_superseded_release_history(
    *,
    product: dict,
    manifest: dict,
    source_members: list[dict],
    source_artifact_root: str,
    active_artifact_root: str,
    active_taf_code: str,
    tombstones: list[dict],
    reports: list[dict],
    ledger: dict,
) -> None:
    """Valida a cadeia append-only de releases pré-publicação substituídas.

    O histórico é fechado pelos snapshots de TOM/HOM/ledger. Arquivos-fonte
    atuais podem evoluir e não são usados como substitutos dos bytes antigos.
    """

    catalog_history = product.get("supersededReleases", [])
    manifest_history = manifest.get("supersededReleases", [])
    if (
        not isinstance(catalog_history, list)
        or not isinstance(manifest_history, list)
        or catalog_history != manifest_history
    ):
        raise ContractError("índice de releases superseded é inválido ou divergente")
    history_tafs = [
        record.get("tafCode") if isinstance(record, dict) else None
        for record in catalog_history
    ]
    if len(history_tafs) != len(set(history_tafs)):
        raise ContractError("índice de releases superseded possui TAF### duplicado")

    # Mantidos na assinatura para compatibilidade com validadores existentes;
    # o snapshot histórico confiável é o TOM###, não o diretório-fonte mutável.
    _ = source_members, source_artifact_root

    active_release = product.get("releasePreparation", {})
    supersession_code = active_release.get("supersessionProcedureCode")
    if not catalog_history:
        if supersession_code is not None:
            raise ContractError("release ativa declara supersessão sem histórico")
        expected_tom_codes = {product.get("tombstoneCode")}
        expected_hom_codes = {product.get("homologationCode")}
    else:
        if (
            not PRC.fullmatch(supersession_code or "")
            or active_release.get("supersedesTafCode")
            != catalog_history[-1].get("tafCode")
            or active_release.get("supersessionReason") != SUPERSESSION_REASON
        ):
            raise ContractError("release ativa não aponta a supersessão mais recente")
        expected_tom_codes = {product.get("tombstoneCode")}
        expected_hom_codes = {product.get("homologationCode")}

    seen_taf: set[str] = set()
    seen_supersession_codes: set[str] = set()
    ledger_by_code = {
        event.get("code"): event for event in ledger.get("events", [])
    }
    for index, record in enumerate(catalog_history):
        if not isinstance(record, dict) or set(record) != SUPERSEDED_RELEASE_FIELDS:
            raise ContractError("registro superseded possui campos inválidos")
        old_taf = record.get("tafCode", "")
        old_hom = record.get("homologationCode", "")
        old_tom = record.get("tombstoneCode", "")
        old_procedure = record.get("procedureCode", "")
        old_audit = record.get("auditCode", "")
        supersession = record.get("supersessionProcedureCode", "")
        expected_successor = (
            catalog_history[index + 1].get("tafCode")
            if index + 1 < len(catalog_history)
            else active_taf_code
        )
        expected_successor_root = (
            catalog_history[index + 1].get("artifactRootSha256")
            if index + 1 < len(catalog_history)
            else active_artifact_root
        )
        historical_profile = record.get("artifactProfile")
        historical_root = record.get("artifactRootSha256", "")
        historical_count = record.get("memberCount")
        if (
            not TAF.fullmatch(old_taf)
            or not HOM.fullmatch(old_hom)
            or not TOM.fullmatch(old_tom)
            or not PRC.fullmatch(old_procedure)
            or not AUD.fullmatch(old_audit)
            or not PRC.fullmatch(supersession)
            or old_taf == active_taf_code
            or old_taf in seen_taf
            or supersession in seen_supersession_codes
            or historical_profile not in RELEASE_ARTIFACT_PROFILES
            or not HEX64.fullmatch(historical_root)
            or not isinstance(historical_count, int)
            or historical_count < 1
            or record.get("supersededByTafCode") != expected_successor
            or record.get("reason") != SUPERSESSION_REASON
            or record.get("publication") != "VOID_PREPUBLICATION"
        ):
            raise ContractError("cadeia superseded é inválida, reutilizada ou não linear")
        _aware_timestamp(str(record.get("supersededAt", "")), "supersededAt")
        seen_taf.add(old_taf)
        seen_supersession_codes.add(supersession)
        expected_tom_codes.add(old_tom)
        expected_hom_codes.add(old_hom)

        old_tombstones = [
            item for item in tombstones if item.get("tombstoneCode") == old_tom
        ]
        if len(old_tombstones) != 1:
            raise ContractError("TOM### superseded não resolve registro histórico único")
        old_tombstone = old_tombstones[0]
        old_members = old_tombstone.get("members")
        if not isinstance(old_members, list) or len(old_members) != historical_count:
            raise ContractError("TOM### superseded perdeu o inventário histórico")
        member_paths = [
            member.get("path") if isinstance(member, dict) else None
            for member in old_members
        ]
        if (
            any(
                not isinstance(member, dict)
                or not isinstance(member.get("path"), str)
                or not HEX64.fullmatch(member.get("sha256", ""))
                or not isinstance(member.get("bytes"), int)
                or member.get("bytes", -1) < 0
                for member in old_members
            )
            or member_paths != sorted(member_paths)
            or len(member_paths) != len(set(member_paths))
        ):
            raise ContractError("TOM### superseded possui membros históricos inválidos")
        recomputed_historical_root = hashlib.sha256(
            "".join(
                f"{member['path']}\t{member['sha256']}\t{member['bytes']}\n"
                for member in old_members
            ).encode("utf-8")
        ).hexdigest()
        if (
            old_tombstone.get("productCode") != product.get("productCode")
            or old_tombstone.get("auditCode") != old_audit
            or old_tombstone.get("homologationCode") != old_hom
            or old_tombstone.get("tafCode") != old_taf
            or (old_tombstone.get("artifactProfile") or SOURCE_BOUND)
            != historical_profile
            or old_tombstone.get("artifactRootSha256") != historical_root
            or recomputed_historical_root != historical_root
            or old_tombstone.get("memberCount") != historical_count
            or old_tombstone.get("publication") != "LOCKED"
        ):
            raise ContractError("TOM### superseded foi alterado ou perdeu seu snapshot")

        old_reports = [
            item for item in reports if item.get("homologationCode") == old_hom
        ]
        if len(old_reports) != 1:
            raise ContractError("HOM### superseded não resolve relatório histórico único")
        old_report = old_reports[0]
        old_core = old_report.get("report")
        if (
            not isinstance(old_core, dict)
            or old_report.get("reportSha256") != _canonical_sha256(old_core)
            or old_report.get("procedureCode") != old_procedure
            or old_report.get("tombstoneCode") != old_tom
            or old_report.get("tafCode") != old_taf
            or old_core.get("productCode") != product.get("productCode")
            or old_core.get("auditCode") != old_audit
            or (old_core.get("artifactProfile") or SOURCE_BOUND)
            != historical_profile
            or old_core.get("artifactRootSha256") != historical_root
            or old_core.get("memberCount") != historical_count
            or old_core.get("auditBinding") != {
                "auditCode": old_audit,
                "artifactRootSha256": historical_root,
                "status": "PASS",
            }
            or old_report.get("publication", {}).get("status") != "LOCKED"
            or old_report.get("publication", {}).get("officialPublication") is not False
        ):
            raise ContractError("HOM### superseded foi alterado")

        hom_scope, hom_date, hom_sequence, _ = _release_code_parts(old_hom, "HOM###")
        if old_hom != (
            f"HOM###-{hom_scope}-{hom_date}-{hom_sequence:04d}-"
            f"{digest8(hom_scope, old_report['reportSha256'], old_core['reviewer'], old_core['reviewedAt'])}"
        ):
            raise ContractError("HOM### superseded diverge do relatório histórico")
        tom_scope, tom_date, tom_sequence, _ = _release_code_parts(old_tom, "TOM###")
        if old_tom != (
            f"TOM###-{tom_scope}-{tom_date}-{tom_sequence:04d}-"
            f"{digest8(tom_scope, historical_root, str(historical_count), old_tombstone['frozenAt'])}"
        ):
            raise ContractError("TOM### superseded diverge do snapshot histórico")
        if not old_taf.endswith(
            digest8(
                product["productCode"],
                old_audit,
                old_hom,
                old_tom,
                historical_root,
            )
        ):
            raise ContractError("TAF### superseded diverge da cadeia histórica")

        historical_codes = {old_procedure, old_audit, old_hom, old_tom, old_taf}
        if not historical_codes.issubset(ledger_by_code):
            raise ContractError("ledger perdeu evento da cadeia superseded")
        old_audit_event = ledger_by_code[old_audit]
        if (
            old_audit_event.get("subjectCode") != product.get("productCode")
            or old_audit_event.get("result")
            != "PASS_BOUND_TO_CURRENT_ARTIFACT_ROOT"
            or (
                historical_profile == SOURCE_BOUND
                and old_audit_event.get("inputHash") != historical_root
            )
        ):
            raise ContractError("AUD### histórico não permanece vinculado ao produto")
        supersession_event = ledger_by_code.get(supersession)
        if (
            not isinstance(supersession_event, dict)
            or supersession_event.get("type")
            != "RELEASE_SUPERSEDED_PREPUBLICATION"
            or supersession_event.get("subjectCode") != product.get("productCode")
            or supersession_event.get("inputHash") != historical_root
            or supersession_event.get("outputHash") != expected_successor_root
            or supersession_event.get("result") != SUPERSESSION_REASON
            or supersession_event.get("evidence", {}).get("previousTafCode")
            != old_taf
            or supersession_event.get("evidence", {}).get("replacementTafCode")
            != expected_successor
            or supersession_event.get("evidence", {}).get(
                "previousArtifactRootSha256"
            )
            != historical_root
            or supersession_event.get("evidence", {}).get("artifactRootSha256")
            != expected_successor_root
            or supersession_event.get("evidence", {}).get("auditBinding") != {
                "auditCode": old_audit,
                "artifactRootSha256": expected_successor_root,
                "status": "PASS",
            }
            or supersession_event.get("evidence", {}).get("publication") != "LOCKED"
        ):
            raise ContractError("evento de supersessão está ausente ou divergente")

    product_tom_codes = {
        item.get("tombstoneCode")
        for item in tombstones
        if item.get("productCode") == product.get("productCode")
    }
    product_hom_codes = {
        item.get("homologationCode")
        for item in reports
        if item.get("report", {}).get("productCode") == product.get("productCode")
    }
    if product_tom_codes != expected_tom_codes or product_hom_codes != expected_hom_codes:
        raise ContractError("produto não possui exatamente uma cadeia ativa e histórico indexado")


def validate_release_state(
    root: Path = ROOT,
    *,
    public_root: Path | None = None,
) -> dict:
    root = root.resolve(strict=True)
    data = root / "23_Cosmos_NEXUS/data"
    catalog = _load_json_path(data / "product-catalog.json", "catálogo de produtos")
    ledger = _load_json_path(data / "execution-ledger.json", "ledger de execução")
    head = _validate_execution_ledger(ledger)
    tombstone_path = data / "tombstone-manifest.json"
    tombstones = (
        _load_json_path(tombstone_path, "manifesto de tombamento")
        if tombstone_path.exists()
        else _default_tombstone_manifest()
    )
    items = tombstones.get("items")
    if not isinstance(items, list):
        raise ContractError("manifesto de tombamento não possui items")
    tomb_codes = [
        item.get("tombstoneCode") if isinstance(item, dict) else None
        for item in items
    ]
    if (
        any(not TOM.fullmatch(code or "") for code in tomb_codes)
        or len(tomb_codes) != len(set(tomb_codes))
    ):
        raise ContractError("manifesto de tombamento possui TOM### ausente ou duplicado")
    tomb_by_code = {item["tombstoneCode"]: item for item in items}
    prepared = 0
    ledger_codes = {event.get("code") for event in ledger.get("events", [])}
    for product in catalog.get("items", []):
        taf_code = product.get("tafCode")
        if taf_code is None:
            continue
        prepared += 1
        if not TAF.fullmatch(taf_code):
            raise ContractError("catálogo contém TAF### inválido")
        hom_code = product.get("homologationCode", "")
        tom_code = product.get("tombstoneCode", "")
        audit_code = product.get("auditCode", "")
        release = product.get("releasePreparation", {})
        if not isinstance(release, dict):
            raise ContractError("releasePreparation ativa precisa ser objeto")
        procedure_code = release.get("procedureCode", "")
        supersession_code = release.get("supersessionProcedureCode")
        if not HOM.fullmatch(hom_code) or not TOM.fullmatch(tom_code) or not AUD.fullmatch(audit_code) or not PRC.fullmatch(procedure_code):
            raise ContractError(f"cadeia de aceite incompleta: {product.get('productCode')}")
        required_ledger_codes = {
            audit_code, hom_code, tom_code, taf_code, procedure_code
        }
        if supersession_code is not None:
            if not PRC.fullmatch(supersession_code):
                raise ContractError("código de supersessão ativo é inválido")
            required_ledger_codes.add(supersession_code)
        if not required_ledger_codes.issubset(ledger_codes):
            raise ContractError("ledger não contém toda a cadeia PRC/AUD/HOM/TOM/TAF")
        audit_events = [
            event for event in ledger.get("events", [])
            if event.get("code") == audit_code
        ]
        audit_event_invalid = (
            len(audit_events) != 1
            or audit_events[0].get("subjectCode") != product.get("productCode")
            or audit_events[0].get("result") != "PASS_BOUND_TO_CURRENT_ARTIFACT_ROOT"
        )
        if supersession_code is None:
            audit_event_invalid = audit_event_invalid or (
                audit_events[0].get("inputHash")
                != release.get("artifactRootSha256")
            )
        if audit_event_invalid:
            raise ContractError("AUD### do ledger não está vinculado ao root atual")
        tombstone = tomb_by_code.get(tom_code)
        if not tombstone or tombstone.get("productCode") != product.get("productCode"):
            raise ContractError("TOM### não aponta para o mesmo produto")
        source_path = _relative_regular_file(root, product["source"]["path"], root)
        manifest = _load_json_path(source_path, "manifesto do produto preparado")
        if sha256_file(source_path) != product["source"].get("sha256"):
            raise ContractError("catálogo diverge do manifesto preparado")
        artifact_profile = _release_artifact_profile(product, manifest)
        members, artifact_root = _release_inventory_for_profile(
            root,
            source_path,
            manifest,
            artifact_profile,
            public_root,
        )
        chain_codes = {hom_code, tom_code, taf_code, procedure_code}
        chain_codes.add(supersession_code or audit_code)
        chain_events = [
            event
            for event in ledger.get("events", [])
            if event.get("code") in chain_codes
            and event.get("subjectCode") == product.get("productCode")
        ]
        if artifact_profile == POST_BUILD_POST_SANITIZE and (
            len(chain_events) != len(chain_codes)
            or any(
                event.get("evidence", {}).get("artifactProfile")
                != artifact_profile
                or event.get("evidence", {}).get("artifactRootSha256")
                != artifact_root
                for event in chain_events
            )
        ):
            raise ContractError(
                "ledger público não está vinculado ao perfil e aos bytes finais"
            )
        if supersession_code is not None and artifact_profile != POST_BUILD_POST_SANITIZE:
            raise ContractError("release superseded precisa ativar o perfil público")
        if tombstone.get("members") != members or tombstone.get("artifactRootSha256") != artifact_root:
            raise ContractError("TOM### diverge dos artefatos físicos atuais")
        report_path = _relative_regular_file(root, release.get("homologationReport", ""), root)
        report_collection = _load_json_path(report_path, "relatórios de homologação")
        reports = [
            item for item in report_collection.get("items", [])
            if isinstance(item, dict) and item.get("homologationCode") == hom_code
        ]
        if len(reports) != 1:
            raise ContractError("HOM### não resolve um único relatório de homologação")
        report = reports[0]
        report_core = report.get("report")
        if not isinstance(report_core, dict) or report.get("reportSha256") != _canonical_sha256(report_core):
            raise ContractError("hash do relatório de homologação diverge")
        profile_records = [
            tombstone.get("artifactProfile"),
            release.get("artifactProfile"),
            manifest.get("releasePreparation", {}).get("artifactProfile"),
            report_core.get("artifactProfile"),
        ]
        if artifact_profile == POST_BUILD_POST_SANITIZE:
            if any(value != artifact_profile for value in profile_records):
                raise ContractError(
                    "cadeia pública não declara POST_BUILD_POST_SANITIZE em todos os registros"
                )
        elif any(
            value not in {None, SOURCE_BOUND} for value in profile_records
        ):
            raise ContractError("cadeia source-bound possui artifactProfile divergente")
        source_members, source_artifact_root = _release_artifact_inventory(
            root,
            source_path,
            manifest,
        )
        _validate_superseded_release_history(
            product=product,
            manifest=manifest,
            source_members=source_members,
            source_artifact_root=source_artifact_root,
            active_artifact_root=artifact_root,
            active_taf_code=taf_code,
            tombstones=items,
            reports=report_collection.get("items", []),
            ledger=ledger,
        )
        if (
            report.get("procedureCode") != procedure_code
            or report.get("homologationCode") != hom_code
            or report.get("tombstoneCode") != tom_code
            or report.get("tafCode") != taf_code
            or report_core.get("productCode") != product.get("productCode")
            or report_core.get("auditCode") != audit_code
            or report_core.get("artifactRootSha256") != artifact_root
            or report_core.get("memberCount") != len(members)
            or report_core.get("auditBinding") != {
                "auditCode": audit_code,
                "artifactRootSha256": artifact_root,
                "status": "PASS",
            }
            or report_core.get("outcome") != "PASS"
            or report.get("publication", {}).get("status") != "LOCKED"
            or report.get("publication", {}).get("officialPublication") is not False
        ):
            raise ContractError("relatório de homologação não fecha a mesma cadeia")
        hom_scope, hom_date, hom_sequence, _ = _release_code_parts(hom_code, "HOM###")
        expected_hom = (
            f"HOM###-{hom_scope}-{hom_date}-{hom_sequence:04d}-"
            f"{digest8(hom_scope, report['reportSha256'], report_core['reviewer'], report_core['reviewedAt'])}"
        )
        if hom_code != expected_hom:
            raise ContractError("HOM### diverge do relatório")
        tom_scope, tom_date, tom_sequence, _ = _release_code_parts(tom_code, "TOM###")
        expected_tom = (
            f"TOM###-{tom_scope}-{tom_date}-{tom_sequence:04d}-"
            f"{digest8(tom_scope, artifact_root, str(len(members)), tombstone['frozenAt'])}"
        )
        if tom_code != expected_tom:
            raise ContractError("TOM### diverge do manifesto congelado")
        expected_scope = token(
            f"{product.get('universe')}-{product.get('block')}", "scope"
        )
        taf_match = re.fullmatch(
            r"TAF###-(U1|U2|U3|MUX)-"
            r"(EVO|PLAN|VIS|STUDY|TEMI|REFINE|TUTOR|MICRO|IMGT|PROD|REFS|AUDIT|EXT)-"
            r"(\d{8})-(\d{4})-([A-F0-9]{8})",
            taf_code,
        )
        if taf_match is None:
            raise ContractError("TAF### inválido")
        if (
            hom_scope != expected_scope
            or tom_scope != expected_scope
            or tombstone.get("scope") != expected_scope
            or taf_match.group(1) != product.get("universe")
            or taf_match.group(2) != product.get("block")
            or not (
                hom_date == tom_date == taf_match.group(3)
                and hom_sequence == tom_sequence == int(taf_match.group(4))
            )
        ):
            raise ContractError("PRC/HOM/TOM/TAF divergem no escopo, data ou sequência")
        taf_suffix = digest8(
            product["productCode"], audit_code, hom_code, tom_code, artifact_root
        )
        if not taf_code.endswith(taf_suffix):
            raise ContractError("TAF### diverge da cadeia de aceite")
        if (
            release.get("artifactRootSha256") != artifact_root
            or release.get("memberCount") != len(members)
            or release.get("sourceEvidenceSha256") != report_core.get("sourceEvidenceSha256")
            or tombstone.get("auditCode") != audit_code
            or tombstone.get("homologationCode") != hom_code
            or tombstone.get("tafCode") != taf_code
            or tombstone.get("publication") != "LOCKED"
        ):
            raise ContractError("catálogo, relatório e tombstone divergem")
        publication = manifest.get("publication", {})
        if (
            publication.get("finalAcceptanceCode") != taf_code
            or publication.get("officialPublication") is not False
            or publication.get("officialPublicationCode") is not None
            or publication.get("requiredCommand") != f"PUBLICAR {taf_code}"
            or product.get("published") is not False
            or product.get("gates", {}).get("ownerUnlock") != "AUSENTE"
        ):
            raise ContractError("TAF### preparado contornou a trava de publicação")
    return {
        "status": "OK",
        "preparedReleases": prepared,
        "ledgerEvents": len(ledger.get("events", [])),
        "ledgerHeadSha256": head,
        "publication": "LOCKED",
    }


def release_inventory(
    product_code: str,
    root: Path = ROOT,
    *,
    public_root: Path | None = None,
) -> dict:
    """Calcula o root físico e fornece um modelo PENDING sem alterar arquivos."""

    root = root.resolve(strict=True)
    if not AGX.fullmatch(product_code):
        raise ContractError("product-code ####AGX válido é obrigatório")
    catalog = _load_json_path(
        root / "23_Cosmos_NEXUS/data/product-catalog.json",
        "catálogo de produtos",
    )
    products = [
        item for item in catalog.get("items", [])
        if item.get("productCode") == product_code
    ]
    if len(products) != 1:
        raise ContractError("product-code não resolve um único item do catálogo")
    product = products[0]
    manifest_path = _relative_regular_file(root, product["source"]["path"], root)
    if sha256_file(manifest_path) != product["source"].get("sha256"):
        raise ContractError("hash do manifesto candidato diverge do catálogo")
    manifest = _load_json_path(manifest_path, "manifesto candidato")
    artifact_profile = _release_artifact_profile(product, manifest)
    members, artifact_root = _release_inventory_for_profile(
        root,
        manifest_path,
        manifest,
        artifact_profile,
        public_root,
    )
    return {
        "schemaVersion": "antigravity-release-inventory-v1",
        "productCode": product_code,
        "auditCode": product.get("auditCode"),
        "artifactProfile": artifact_profile,
        "artifactRootSha256": artifact_root,
        "memberCount": len(members),
        "members": members,
        "publication": "LOCKED",
        "evidenceTemplate": {
            "schemaVersion": "antigravity-release-evidence-v1",
            "productCode": product_code,
            "reviewer": "PREENCHER",
            "reviewedAt": "PREENCHER_ISO8601_COM_FUSO",
            "confirmations": {
                "safariMacOS": "PENDING",
                "safariIPhone": "PENDING",
                "clinicalReview": "PENDING",
                "rightsReview": "PENDING",
            },
            "auditBinding": {
                "auditCode": product.get("auditCode"),
                "artifactRootSha256": artifact_root,
                "status": "PENDING",
            },
            "testRuns": [],
            "notes": [],
        },
    }


def supersession_inventory(
    product_code: str,
    supersedes_taf: str,
    *,
    public_root: Path,
    previous_public_root: Path | None = None,
    root: Path = ROOT,
) -> dict:
    """Calcula, sem gravar, uma substituição pré-publicação append-only."""

    root = root.resolve(strict=True)
    public_root = _resolve_public_root(public_root, root)
    previous_public_root = (
        _resolve_public_root(previous_public_root, root)
        if previous_public_root is not None
        else None
    )
    if not AGX.fullmatch(product_code):
        raise ContractError("product-code ####AGX válido é obrigatório")
    if not TAF.fullmatch(supersedes_taf):
        raise ContractError("--supersedes-taf precisa ser TAF### válido")
    catalog = _load_json_path(
        root / "23_Cosmos_NEXUS/data/product-catalog.json",
        "catálogo de produtos",
    )
    products = [
        item for item in catalog.get("items", [])
        if item.get("productCode") == product_code
    ]
    if len(products) != 1:
        raise ContractError("product-code não resolve um único item do catálogo")
    product = products[0]
    if product.get("tafCode") != supersedes_taf:
        raise ContractError("TAF### informado não é a cadeia ativa exata")
    if product.get("published") is not False:
        raise ContractError("release publicada não pode ser superseded")
    manifest_path = _relative_regular_file(root, product["source"]["path"], root)
    if sha256_file(manifest_path) != product["source"].get("sha256"):
        raise ContractError("hash do manifesto preparado diverge do catálogo")
    manifest = _load_json_path(manifest_path, "manifesto preparado")
    old_profile = _release_artifact_profile(product, manifest)
    if old_profile == POST_BUILD_POST_SANITIZE and previous_public_root is None:
        raise ContractError(
            "--previous-public-root é obrigatório ao substituir cadeia POST_BUILD"
        )
    validate_release_state(
        root,
        public_root=previous_public_root or public_root,
    )
    publication = manifest.get("publication", {})
    if (
        publication.get("officialPublication") is not False
        or publication.get("officialPublicationCode") is not None
        or publication.get("finalAcceptanceCode") != supersedes_taf
        or publication.get("requiredCommand") != f"PUBLICAR {supersedes_taf}"
        or product.get("gates", {}).get("ownerUnlock") != "AUSENTE"
    ):
        raise ContractError("cadeia ativa não está LOCKED e inequivocamente não publicada")
    old_members, old_artifact_root = _release_inventory_for_profile(
        root,
        manifest_path,
        manifest,
        old_profile,
        previous_public_root,
    )
    old_release = product.get("releasePreparation", {})
    if (
        old_release.get("artifactRootSha256") != old_artifact_root
        or old_release.get("memberCount") != len(old_members)
    ):
        raise ContractError("snapshot público anterior diverge da cadeia ativa")
    members, artifact_root = _release_public_artifact_inventory(
        root,
        public_root,
        manifest_path,
        manifest,
    )
    if artifact_root == old_artifact_root:
        raise ContractError("novo artefato é idêntico à cadeia ativa")
    return {
        "schemaVersion": "antigravity-release-inventory-v1",
        "productCode": product_code,
        "auditCode": product.get("auditCode"),
        "artifactProfile": POST_BUILD_POST_SANITIZE,
        "supersedesTafCode": supersedes_taf,
        "previousArtifactProfile": old_profile,
        "previousArtifactRootSha256": old_artifact_root,
        "artifactRootSha256": artifact_root,
        "memberCount": len(members),
        "members": members,
        "publication": "LOCKED",
        "evidenceTemplate": {
            "schemaVersion": "antigravity-release-evidence-v1",
            "productCode": product_code,
            "reviewer": "PREENCHER",
            "reviewedAt": "PREENCHER_ISO8601_COM_FUSO",
            "confirmations": {
                "safariMacOS": "PENDING",
                "safariIPhone": "PENDING",
                "clinicalReview": "PENDING",
                "rightsReview": "PENDING",
            },
            "auditBinding": {
                "auditCode": product.get("auditCode"),
                "artifactRootSha256": artifact_root,
                "status": "PENDING",
            },
            "testRuns": [],
            "notes": [],
        },
    }


def _active_child_taf_codes(catalog: dict, child_taf_codes: list[str]) -> list[str]:
    """Resolve referências filhas antigas para a única cadeia ativa atual."""

    if not isinstance(child_taf_codes, list) or not child_taf_codes:
        raise ContractError("guarda-chuva precisa declarar childTafCodes")
    active_codes: list[str] = []
    for child_taf in child_taf_codes:
        if not isinstance(child_taf, str) or not TAF.fullmatch(child_taf):
            raise ContractError("childTafCodes contém TAF### inválido")
        matches: list[str] = []
        for item in catalog.get("items", []):
            active_taf = item.get("tafCode")
            if not isinstance(active_taf, str) or not TAF.fullmatch(active_taf):
                continue
            if active_taf == child_taf:
                matches.append(active_taf)
                continue
            for record in item.get("supersededReleases", []):
                if (
                    record.get("tafCode") == child_taf
                    and record.get("publication") == "VOID_PREPUBLICATION"
                ):
                    matches.append(active_taf)
        if len(matches) != 1:
            raise ContractError(
                "childTafCodes não resolve uma única cadeia ativa no catálogo"
            )
        active_codes.append(matches[0])
    if len(set(active_codes)) != len(active_codes):
        raise ContractError("childTafCodes resolve cadeias ativas duplicadas")
    return active_codes


def prepare_release(
    product_code: str,
    evidence_path: Path,
    release_date: str,
    sequence: int,
    *,
    root: Path = ROOT,
    public_root: Path | None = None,
    fail_after: int | None = None,
) -> dict:
    """Prepara PRC/HOM/TOM/TAF de modo transacional, sem publicar nada."""

    root = root.resolve(strict=True)
    if not AGX.fullmatch(product_code):
        raise ContractError("product-code ####AGX válido é obrigatório")
    date_code = _parse_calendar_date(release_date)
    if sequence < 1 or sequence > 9999:
        raise ContractError("sequence deve estar entre 1 e 9999")
    sequence_code = f"{sequence:04d}"
    data = root / "23_Cosmos_NEXUS/data"
    private_locks = root / ".nexus-sync-private/release-locks"
    _secure_directory(private_locks.parent)
    _secure_directory(private_locks)
    lock_path = private_locks / f"{hashlib.sha256(product_code.encode()).hexdigest()}.lock"
    lock_fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o600)
    os.chmod(lock_path, 0o600)
    fcntl.flock(lock_fd, fcntl.LOCK_EX)
    try:
        catalog_path = data / "product-catalog.json"
        ledger_path = data / "execution-ledger.json"
        module_path = root / "23_Cosmos_NEXUS/module.manifest.json"
        catalog = _load_json_path(catalog_path, "catálogo de produtos")
        ledger = _load_json_path(ledger_path, "ledger de execução")
        _validate_execution_ledger(ledger)
        products = [
            item for item in catalog.get("items", [])
            if item.get("productCode") == product_code
        ]
        if len(products) != 1:
            raise ContractError("product-code não resolve um único item do catálogo")
        product = products[0]
        manifest_path = _relative_regular_file(root, product["source"]["path"], root)
        manifest = _load_json_path(manifest_path, "manifesto candidato")
        if sha256_file(manifest_path) != product["source"].get("sha256"):
            raise ContractError("hash do manifesto candidato diverge do catálogo")
        artifact_profile = _release_artifact_profile(product, manifest)
        members, artifact_root = _release_inventory_for_profile(
            root,
            manifest_path,
            manifest,
            artifact_profile,
            public_root,
        )
        evidence, evidence_hash = _validate_release_evidence(
            evidence_path,
            product_code,
            product.get("auditCode", ""),
            artifact_root,
        )

        if product.get("tafCode") is not None:
            state = validate_release_state(root, public_root=public_root)
            release = product.get("releasePreparation", {})
            if (
                release.get("artifactRootSha256") != artifact_root
                or release.get("sourceEvidenceSha256") != evidence_hash
            ):
                raise ContractError("produto já tombado mudou; crie nova versão e novo ####AGX")
            return {
                "status": "ALREADY_PREPARED",
                "idempotent": True,
                "productCode": product_code,
                "procedureCode": release.get("procedureCode"),
                "homologationCode": product.get("homologationCode"),
                "tombstoneCode": product.get("tombstoneCode"),
                "tafCode": product.get("tafCode"),
                "artifactRootSha256": artifact_root,
                "artifactProfile": artifact_profile,
                "memberCount": len(members),
                "publication": state["publication"],
                "requiredCommand": f"PUBLICAR {product.get('tafCode')}",
            }

        _validate_candidate_for_release(product, manifest)
        now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
        scope = token(f"{product['universe']}-{product['block']}", "scope")
        report_core = {
            "schemaVersion": "antigravity-homologation-report-v1",
            "productCode": product_code,
            "auditCode": product["auditCode"],
            "reviewer": evidence["reviewer"],
            "reviewedAt": evidence["reviewedAt"],
            "sourceEvidenceSha256": evidence_hash,
            "confirmations": evidence["confirmations"],
            "auditBinding": evidence["auditBinding"],
            "testRuns": evidence["testRuns"],
            "notes": evidence["notes"],
            "artifactRootSha256": artifact_root,
            "artifactProfile": artifact_profile,
            "memberCount": len(members),
            "auditOutcome": manifest["audit"]["outcome"],
            "outcome": "PASS",
        }
        report_hash = _canonical_sha256(report_core)
        hom_suffix = digest8(
            scope, report_hash, evidence["reviewer"], evidence["reviewedAt"]
        )
        hom_code = f"HOM###-{scope}-{date_code}-{sequence_code}-{hom_suffix}"
        tom_suffix = digest8(scope, artifact_root, str(len(members)), now)
        tom_code = f"TOM###-{scope}-{date_code}-{sequence_code}-{tom_suffix}"
        taf_suffix = digest8(
            product_code,
            product["auditCode"],
            hom_code,
            tom_code,
            artifact_root,
        )
        taf_code = (
            f"TAF###-{product['universe']}-{product['block']}-"
            f"{date_code}-{sequence_code}-{taf_suffix}"
        )
        output_hash = _canonical_sha256(
            {
                "reportSha256": report_hash,
                "artifactRootSha256": artifact_root,
                "homologationCode": hom_code,
                "tombstoneCode": tom_code,
                "tafCode": taf_code,
            }
        )
        input_hash = sha256_file(manifest_path)
        procedure_suffix = digest8(
            "PREPARAR-RELEASE", product_code, input_hash, output_hash, now
        )
        procedure_code = (
            f"PRC###-PREPARAR-RELEASE-{date_code}-{sequence_code}-{procedure_suffix}"
        )
        report_relative = Path("23_Cosmos_NEXUS/data/homologation-reports.json")
        report_path = root / report_relative
        report_payload = {
            "schemaVersion": "antigravity-homologation-record-v1",
            "report": report_core,
            "reportSha256": report_hash,
            "procedureCode": procedure_code,
            "homologationCode": hom_code,
            "tombstoneCode": tom_code,
            "tafCode": taf_code,
            "preparedAt": now,
            "publication": {
                "status": "LOCKED",
                "officialPublication": False,
                "requiredCommand": f"PUBLICAR {taf_code}",
            },
        }
        report_collection = (
            _load_json_path(report_path, "relatórios de homologação")
            if report_path.exists()
            else _default_homologation_reports()
        )
        if any(
            item.get("homologationCode") == hom_code
            or item.get("report", {}).get("productCode") == product_code
            for item in report_collection.get("items", [])
        ):
            raise ContractError("coleção de homologação já contém o produto ou HOM###")
        report_collection["items"].append(report_payload)
        report_collection["updatedAt"] = now

        tombstone_path = data / "tombstone-manifest.json"
        tombstones = (
            _load_json_path(tombstone_path, "manifesto de tombamento")
            if tombstone_path.exists()
            else _default_tombstone_manifest()
        )
        if any(
            item.get("tombstoneCode") == tom_code
            or item.get("productCode") == product_code
            for item in tombstones.get("items", [])
        ):
            raise ContractError("manifesto de tombamento já contém o produto ou TOM###")
        tombstone_record = {
            "tombstoneCode": tom_code,
            "productCode": product_code,
            "auditCode": product["auditCode"],
            "homologationCode": hom_code,
            "tafCode": taf_code,
            "scope": scope,
            "frozenAt": now,
            "artifactRootAlgorithm": "SHA256 de path, SHA-256 e bytes separados por tabulação, ordenados por path e terminados por nova linha",
            "artifactProfile": artifact_profile,
            "artifactRootSha256": artifact_root,
            "memberCount": len(members),
            "members": members,
            "excludedGovernanceMetadata": [
                manifest_path.relative_to(root).as_posix()
            ],
            "publication": "LOCKED",
        }
        tombstones["items"].append(tombstone_record)
        tombstones["updatedAt"] = now

        manifest_next = copy.deepcopy(manifest)
        manifest_next["publication"].update(
            {
                "status": "release-prepared",
                "officialPublication": False,
                "finalAcceptanceCode": taf_code,
                "officialPublicationCode": None,
                "ownerPublicationAuthorization": False,
                "requiredCommand": f"PUBLICAR {taf_code}",
            }
        )
        manifest_next["releasePreparation"] = {
            "procedureCode": procedure_code,
            "homologationCode": hom_code,
            "homologationReport": report_relative.as_posix(),
            "tombstoneCode": tom_code,
            "tafCode": taf_code,
            "artifactRootSha256": artifact_root,
            "artifactProfile": artifact_profile,
            "memberCount": len(members),
            "sourceEvidenceSha256": evidence_hash,
            "preparedAt": now,
            "publication": "LOCKED",
        }
        manifest_next_hash = hashlib.sha256(_json_bytes(manifest_next)).hexdigest()

        catalog_next = copy.deepcopy(catalog)
        target = next(
            item for item in catalog_next["items"]
            if item.get("productCode") == product_code
        )
        target.update(
            {
                "status": "TAF_PREPARED",
                "homologationCode": hom_code,
                "tombstoneCode": tom_code,
                "tafCode": taf_code,
                "published": False,
                "releasePreparation": {
                    "procedureCode": procedure_code,
                    "homologationReport": report_relative.as_posix(),
                    "artifactRootSha256": artifact_root,
                    "artifactProfile": artifact_profile,
                    "memberCount": len(members),
                    "sourceEvidenceSha256": evidence_hash,
                    "preparedAt": now,
                },
            }
        )
        target["source"]["sha256"] = manifest_next_hash
        target["gates"].update(
            {
                "automatedTechnical": "APROVADO",
                "humanVisual": "APROVADO",
                "clinical": "APROVADO",
                "rights": "APROVADO",
                "ownerUnlock": "AUSENTE",
            }
        )
        catalog_next["updatedAt"] = now

        module_next = _load_json_path(module_path, "manifesto do módulo NEXUS")
        module_next.setdefault("data", {}).update(
            {
                "homologationReports": "data/homologation-reports.json",
                "tombstones": "data/tombstone-manifest.json",
            }
        )
        candidates = [
            item for item in module_next.get("candidateProducts", [])
            if item.get("productCode") == product_code
        ]
        if len(candidates) != 1:
            raise ContractError("manifesto NEXUS não resolve o produto candidato")
        candidates[0].update(
            {
                "status": "release-prepared",
                "tafCode": taf_code,
                "officialPublication": False,
            }
        )
        module_source = module_path.relative_to(root).as_posix()
        module_catalog_items = [
            item for item in catalog_next.get("items", [])
            if item.get("source", {}).get("path") == module_source
        ]
        if len(module_catalog_items) > 1:
            raise ContractError("catálogo possui manifesto NEXUS duplicado")
        if module_catalog_items:
            module_catalog_items[0]["source"]["sha256"] = hashlib.sha256(
                _json_bytes(module_next)
            ).hexdigest()

        ledger_next = copy.deepcopy(ledger)
        ledger_next.setdefault("ledgerHeadSha256", ZERO_HASH)
        common_evidence = {
            "artifactRootSha256": artifact_root,
            "artifactProfile": artifact_profile,
            "homologationReport": report_relative.as_posix(),
            "publication": "LOCKED",
        }
        release_events = [
            {
                "code": procedure_code,
                "type": "RELEASE_PREPARATION",
                "subjectCode": product_code,
                "timestamp": now,
                "inputHash": input_hash,
                "outputHash": output_hash,
                "result": "PASS_PREPARED_NOT_PUBLISHED",
                "evidence": common_evidence,
            },
            {
                "code": product["auditCode"],
                "type": "AUDIT_BOUND_TO_RELEASE_ROOT",
                "subjectCode": product_code,
                "timestamp": now,
                "inputHash": artifact_root,
                "outputHash": manifest.get("audit", {}).get(
                    "auditEvidenceSha256",
                    _canonical_sha256(evidence["auditBinding"]),
                ),
                "result": "PASS_BOUND_TO_CURRENT_ARTIFACT_ROOT",
                "evidence": {
                    **common_evidence,
                    "auditBinding": evidence["auditBinding"],
                },
            },
            {
                "code": hom_code,
                "type": "HOMOLOGATION",
                "subjectCode": product_code,
                "timestamp": now,
                "inputHash": evidence_hash,
                "outputHash": report_hash,
                "result": "PASS",
                "evidence": common_evidence,
            },
            {
                "code": tom_code,
                "type": "TOMBSTONE",
                "subjectCode": product_code,
                "timestamp": now,
                "inputHash": report_hash,
                "outputHash": artifact_root,
                "result": "FROZEN_NOT_PUBLISHED",
                "evidence": common_evidence,
            },
            {
                "code": taf_code,
                "type": "FINAL_ACCEPTANCE_PREPARED",
                "subjectCode": product_code,
                "timestamp": now,
                "inputHash": artifact_root,
                "outputHash": hashlib.sha256(taf_code.encode("utf-8")).hexdigest(),
                "result": "PREPARED_AWAITING_LITERAL_OWNER_COMMAND",
                "evidence": {
                    **common_evidence,
                    "requiredCommand": f"PUBLICAR {taf_code}",
                },
            },
        ]
        existing_ledger_codes = {
            event.get("code") for event in ledger_next.get("events", [])
        }
        for event in release_events:
            if event["code"] == product["auditCode"] and event["code"] in existing_ledger_codes:
                continue
            _append_ledger_event(ledger_next, event)
        ledger_next.update(
            {
                "updatedAt": now,
                "status": "release-prepared-publication-locked",
            }
        )

        updates = {
            report_path: report_collection,
            tombstone_path: tombstones,
            manifest_path: manifest_next,
            module_path: module_next,
            catalog_path: catalog_next,
            ledger_path: ledger_next,
        }
        _transactional_json_update(
            updates,
            lambda: validate_release_state(root, public_root=public_root),
            fail_after=fail_after,
        )
        return {
            "status": "PREPARED",
            "idempotent": False,
            "productCode": product_code,
            "procedureCode": procedure_code,
            "homologationCode": hom_code,
            "tombstoneCode": tom_code,
            "tafCode": taf_code,
            "artifactRootSha256": artifact_root,
            "artifactProfile": artifact_profile,
            "memberCount": len(members),
            "homologationReport": report_relative.as_posix(),
            "publication": "LOCKED",
            "requiredCommand": f"PUBLICAR {taf_code}",
        }
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)


def supersede_release(
    product_code: str,
    supersedes_taf: str,
    evidence_path: Path,
    release_date: str,
    sequence: int,
    *,
    reason: str,
    public_root: Path,
    previous_public_root: Path | None = None,
    root: Path = ROOT,
    fail_after: int | None = None,
) -> dict:
    """Substitui uma cadeia LOCKED pré-publicação sem apagar o histórico."""

    root = root.resolve(strict=True)
    if not AGX.fullmatch(product_code):
        raise ContractError("product-code ####AGX válido é obrigatório")
    if not TAF.fullmatch(supersedes_taf):
        raise ContractError("--supersedes-taf precisa ser TAF### válido")
    if reason != SUPERSESSION_REASON:
        raise ContractError(f"--reason precisa ser exatamente {SUPERSESSION_REASON}")
    date_code = _parse_calendar_date(release_date)
    if sequence < 1 or sequence > 9999:
        raise ContractError("sequence deve estar entre 1 e 9999")
    sequence_code = f"{sequence:04d}"
    public_root = _resolve_public_root(public_root, root)
    previous_public_root = (
        _resolve_public_root(previous_public_root, root)
        if previous_public_root is not None
        else None
    )

    data = root / "23_Cosmos_NEXUS/data"
    private_locks = root / ".nexus-sync-private/release-locks"
    _secure_directory(private_locks.parent)
    _secure_directory(private_locks)
    lock_path = private_locks / f"{hashlib.sha256(product_code.encode()).hexdigest()}.lock"
    lock_fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o600)
    os.chmod(lock_path, 0o600)
    fcntl.flock(lock_fd, fcntl.LOCK_EX)
    try:
        catalog_path = data / "product-catalog.json"
        ledger_path = data / "execution-ledger.json"
        module_path = root / "23_Cosmos_NEXUS/module.manifest.json"
        tombstone_path = data / "tombstone-manifest.json"
        report_relative = Path("23_Cosmos_NEXUS/data/homologation-reports.json")
        report_path = root / report_relative
        catalog = _load_json_path(catalog_path, "catálogo de produtos")
        ledger = _load_json_path(ledger_path, "ledger de execução")
        _validate_execution_ledger(ledger)
        tombstones = _load_json_path(tombstone_path, "manifesto de tombamento")
        report_collection = _load_json_path(
            report_path,
            "relatórios de homologação",
        )
        products = [
            item for item in catalog.get("items", [])
            if item.get("productCode") == product_code
        ]
        if len(products) != 1:
            raise ContractError("product-code não resolve um único item do catálogo")
        product = products[0]
        if product.get("tafCode") != supersedes_taf:
            raise ContractError("TAF### informado não é a cadeia ativa exata")
        if product.get("published") is not False:
            raise ContractError("release publicada não pode ser superseded")
        old_release = product.get("releasePreparation")
        if not isinstance(old_release, dict):
            raise ContractError("cadeia ativa não possui releasePreparation válida")

        manifest_path = _relative_regular_file(root, product["source"]["path"], root)
        if sha256_file(manifest_path) != product["source"].get("sha256"):
            raise ContractError("hash do manifesto preparado diverge do catálogo")
        manifest = _load_json_path(manifest_path, "manifesto preparado")
        old_profile = _release_artifact_profile(product, manifest)
        if old_profile == POST_BUILD_POST_SANITIZE and previous_public_root is None:
            raise ContractError(
                "--previous-public-root é obrigatório ao substituir cadeia POST_BUILD"
            )
        # O snapshot anterior fecha contra o build antigo; a nova cadeia fecha
        # somente depois contra ``public_root`` dentro da transação.
        validate_release_state(
            root,
            public_root=previous_public_root or public_root,
        )
        publication = manifest.get("publication", {})
        if (
            publication.get("officialPublication") is not False
            or publication.get("officialPublicationCode") is not None
            or publication.get("finalAcceptanceCode") != supersedes_taf
            or publication.get("requiredCommand") != f"PUBLICAR {supersedes_taf}"
            or product.get("gates", {}).get("ownerUnlock") != "AUSENTE"
        ):
            raise ContractError("cadeia ativa não está LOCKED e inequivocamente não publicada")

        old_members, old_artifact_root = _release_inventory_for_profile(
            root,
            manifest_path,
            manifest,
            old_profile,
            previous_public_root,
        )
        if (
            old_release.get("artifactRootSha256") != old_artifact_root
            or old_release.get("memberCount") != len(old_members)
        ):
            raise ContractError("índice ativo não fecha o snapshot público anterior")
        members, artifact_root = _release_public_artifact_inventory(
            root,
            public_root,
            manifest_path,
            manifest,
        )
        if artifact_root == old_artifact_root:
            raise ContractError("novo artefato é idêntico à cadeia ativa")
        evidence, evidence_hash = _validate_release_evidence(
            evidence_path,
            product_code,
            product.get("auditCode", ""),
            artifact_root,
        )

        now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
            "+00:00", "Z"
        )
        scope = token(f"{product['universe']}-{product['block']}", "scope")
        report_core = {
            "schemaVersion": "antigravity-homologation-report-v1",
            "productCode": product_code,
            "auditCode": product["auditCode"],
            "reviewer": evidence["reviewer"],
            "reviewedAt": evidence["reviewedAt"],
            "sourceEvidenceSha256": evidence_hash,
            "confirmations": evidence["confirmations"],
            "auditBinding": evidence["auditBinding"],
            "testRuns": evidence["testRuns"],
            "notes": evidence["notes"],
            "artifactRootSha256": artifact_root,
            "artifactProfile": POST_BUILD_POST_SANITIZE,
            "memberCount": len(members),
            "auditOutcome": manifest["audit"]["outcome"],
            "outcome": "PASS",
        }
        report_hash = _canonical_sha256(report_core)
        hom_code = (
            f"HOM###-{scope}-{date_code}-{sequence_code}-"
            f"{digest8(scope, report_hash, evidence['reviewer'], evidence['reviewedAt'])}"
        )
        tom_code = (
            f"TOM###-{scope}-{date_code}-{sequence_code}-"
            f"{digest8(scope, artifact_root, str(len(members)), now)}"
        )
        taf_code = (
            f"TAF###-{product['universe']}-{product['block']}-"
            f"{date_code}-{sequence_code}-"
            f"{digest8(product_code, product['auditCode'], hom_code, tom_code, artifact_root)}"
        )
        output_hash = _canonical_sha256(
            {
                "reportSha256": report_hash,
                "artifactRootSha256": artifact_root,
                "homologationCode": hom_code,
                "tombstoneCode": tom_code,
                "tafCode": taf_code,
                "supersedesTafCode": supersedes_taf,
            }
        )
        input_hash = sha256_file(manifest_path)
        procedure_code = (
            f"PRC###-PREPARAR-RELEASE-{date_code}-{sequence_code}-"
            f"{digest8('PREPARAR-RELEASE', product_code, input_hash, output_hash, now)}"
        )
        supersession_code = (
            f"PRC###-SUPERSEDE-RELEASE-{date_code}-{sequence_code}-"
            f"{digest8('SUPERSEDE-RELEASE', product_code, supersedes_taf, taf_code, old_artifact_root, artifact_root, reason, now)}"
        )
        proposed_codes = {
            procedure_code,
            supersession_code,
            hom_code,
            tom_code,
            taf_code,
        }
        if len(proposed_codes) != 5:
            raise ContractError("colisão interna ao gerar nova cadeia")
        existing_codes = {
            event.get("code") for event in ledger.get("events", [])
        }
        existing_codes.update(
            item.get("tombstoneCode") for item in tombstones.get("items", [])
        )
        existing_codes.update(
            item.get("homologationCode")
            for item in report_collection.get("items", [])
        )
        reserved_coordinates = (
            f"PRC###-PREPARAR-RELEASE-{date_code}-{sequence_code}-",
            f"PRC###-SUPERSEDE-RELEASE-{date_code}-{sequence_code}-",
            f"HOM###-{scope}-{date_code}-{sequence_code}-",
            f"TOM###-{scope}-{date_code}-{sequence_code}-",
            f"TAF###-{product['universe']}-{product['block']}-{date_code}-{sequence_code}-",
        )
        coordinate_collision = any(
            isinstance(code, str)
            and any(code.startswith(prefix) for prefix in reserved_coordinates)
            for code in existing_codes
        )
        if (
            proposed_codes & existing_codes
            or taf_code == supersedes_taf
            or coordinate_collision
        ):
            raise ContractError("colisão ou reutilização de código na nova cadeia")

        report_payload = {
            "schemaVersion": "antigravity-homologation-record-v1",
            "report": report_core,
            "reportSha256": report_hash,
            "procedureCode": procedure_code,
            "homologationCode": hom_code,
            "tombstoneCode": tom_code,
            "tafCode": taf_code,
            "preparedAt": now,
            "publication": {
                "status": "LOCKED",
                "officialPublication": False,
                "requiredCommand": f"PUBLICAR {taf_code}",
            },
        }
        reports_next = copy.deepcopy(report_collection)
        reports_next["items"].append(report_payload)
        reports_next["updatedAt"] = now

        tombstone_record = {
            "tombstoneCode": tom_code,
            "productCode": product_code,
            "auditCode": product["auditCode"],
            "homologationCode": hom_code,
            "tafCode": taf_code,
            "scope": scope,
            "frozenAt": now,
            "artifactRootAlgorithm": "SHA256 de path, SHA-256 e bytes separados por tabulação, ordenados por path e terminados por nova linha",
            "artifactProfile": POST_BUILD_POST_SANITIZE,
            "artifactRootSha256": artifact_root,
            "memberCount": len(members),
            "members": members,
            "excludedGovernanceMetadata": [
                manifest_path.relative_to(root).as_posix()
            ],
            "publication": "LOCKED",
        }
        tombstones_next = copy.deepcopy(tombstones)
        tombstones_next["items"].append(tombstone_record)
        tombstones_next["updatedAt"] = now

        superseded_record = {
            "procedureCode": old_release["procedureCode"],
            "auditCode": product["auditCode"],
            "homologationCode": product["homologationCode"],
            "tombstoneCode": product["tombstoneCode"],
            "tafCode": supersedes_taf,
            "artifactProfile": old_profile,
            "artifactRootSha256": old_artifact_root,
            "memberCount": len(old_members),
            "supersededAt": now,
            "supersededByTafCode": taf_code,
            "supersessionProcedureCode": supersession_code,
            "reason": reason,
            "publication": "VOID_PREPUBLICATION",
        }
        superseded_history = copy.deepcopy(product.get("supersededReleases", []))
        superseded_history.append(superseded_record)

        manifest_next = copy.deepcopy(manifest)
        if manifest_next.get("schemaVersion") == UMBRELLA_RELEASE_SCHEMA:
            identity_next = manifest_next.get("identity")
            if not isinstance(identity_next, dict):
                raise ContractError("identity do guarda-chuva é inválida")
            if "childTafCodes" in identity_next:
                identity_next["childTafCodes"] = _active_child_taf_codes(
                    catalog,
                    identity_next.get("childTafCodes"),
                )
        manifest_next["artifactProfile"] = POST_BUILD_POST_SANITIZE
        manifest_next["supersededReleases"] = superseded_history
        manifest_next["publication"].update(
            {
                "status": "release-prepared",
                "officialPublication": False,
                "finalAcceptanceCode": taf_code,
                "officialPublicationCode": None,
                "ownerPublicationAuthorization": False,
                "requiredCommand": f"PUBLICAR {taf_code}",
            }
        )
        manifest_next["releasePreparation"] = {
            "procedureCode": procedure_code,
            "homologationCode": hom_code,
            "homologationReport": report_relative.as_posix(),
            "tombstoneCode": tom_code,
            "tafCode": taf_code,
            "artifactRootSha256": artifact_root,
            "artifactProfile": POST_BUILD_POST_SANITIZE,
            "memberCount": len(members),
            "sourceEvidenceSha256": evidence_hash,
            "preparedAt": now,
            "supersessionProcedureCode": supersession_code,
            "supersedesTafCode": supersedes_taf,
            "supersessionReason": reason,
            "publication": "LOCKED",
        }
        manifest_next_hash = hashlib.sha256(_json_bytes(manifest_next)).hexdigest()

        catalog_next = copy.deepcopy(catalog)
        target = next(
            item for item in catalog_next["items"]
            if item.get("productCode") == product_code
        )
        target.update(
            {
                "artifactProfile": POST_BUILD_POST_SANITIZE,
                "status": "TAF_PREPARED",
                "homologationCode": hom_code,
                "tombstoneCode": tom_code,
                "tafCode": taf_code,
                "published": False,
                "supersededReleases": superseded_history,
                "releasePreparation": {
                    "procedureCode": procedure_code,
                    "homologationReport": report_relative.as_posix(),
                    "artifactRootSha256": artifact_root,
                    "artifactProfile": POST_BUILD_POST_SANITIZE,
                    "memberCount": len(members),
                    "sourceEvidenceSha256": evidence_hash,
                    "preparedAt": now,
                    "supersessionProcedureCode": supersession_code,
                    "supersedesTafCode": supersedes_taf,
                    "supersessionReason": reason,
                },
            }
        )
        target["source"]["sha256"] = manifest_next_hash
        target["gates"].update(
            {
                "automatedTechnical": "APROVADO",
                "humanVisual": "APROVADO",
                "clinical": "APROVADO",
                "rights": "APROVADO",
                "ownerUnlock": "AUSENTE",
            }
        )
        catalog_next["updatedAt"] = now

        module_next = _load_json_path(module_path, "manifesto do módulo NEXUS")
        candidates = [
            item for item in module_next.get("candidateProducts", [])
            if item.get("productCode") == product_code
        ]
        if len(candidates) != 1:
            raise ContractError("manifesto NEXUS não resolve o produto candidato")
        candidates[0].update(
            {
                "status": "release-prepared",
                "tafCode": taf_code,
                "officialPublication": False,
            }
        )
        if manifest.get("schemaVersion") == UMBRELLA_RELEASE_SCHEMA:
            module_publication = module_next.get("publication")
            if not isinstance(module_publication, dict):
                raise ContractError("publication do manifesto NEXUS é inválida")
            module_publication.update(
                {
                    "published": False,
                    "tafIssued": True,
                    "stationTafCode": taf_code,
                    "requiredCommand": f"PUBLICAR {taf_code}",
                    "ownerPublicationAuthorization": False,
                }
            )
        module_source = module_path.relative_to(root).as_posix()
        module_catalog_items = [
            item for item in catalog_next.get("items", [])
            if item.get("source", {}).get("path") == module_source
        ]
        if len(module_catalog_items) > 1:
            raise ContractError("catálogo possui manifesto NEXUS duplicado")
        if module_catalog_items:
            module_catalog_items[0]["source"]["sha256"] = hashlib.sha256(
                _json_bytes(module_next)
            ).hexdigest()

        common_evidence = {
            "artifactRootSha256": artifact_root,
            "artifactProfile": POST_BUILD_POST_SANITIZE,
            "homologationReport": report_relative.as_posix(),
            "publication": "LOCKED",
        }
        supersession_event = {
            "code": supersession_code,
            "type": "RELEASE_SUPERSEDED_PREPUBLICATION",
            "subjectCode": product_code,
            "timestamp": now,
            "inputHash": old_artifact_root,
            "outputHash": artifact_root,
            "result": reason,
            "evidence": {
                **common_evidence,
                "previousTafCode": supersedes_taf,
                "replacementTafCode": taf_code,
                "previousArtifactRootSha256": old_artifact_root,
                "auditBinding": evidence["auditBinding"],
                "reason": reason,
            },
        }
        release_events = [
            supersession_event,
            {
                "code": procedure_code,
                "type": "RELEASE_PREPARATION",
                "subjectCode": product_code,
                "timestamp": now,
                "inputHash": input_hash,
                "outputHash": output_hash,
                "result": "PASS_PREPARED_NOT_PUBLISHED",
                "evidence": common_evidence,
            },
            {
                "code": hom_code,
                "type": "HOMOLOGATION",
                "subjectCode": product_code,
                "timestamp": now,
                "inputHash": evidence_hash,
                "outputHash": report_hash,
                "result": "PASS",
                "evidence": common_evidence,
            },
            {
                "code": tom_code,
                "type": "TOMBSTONE",
                "subjectCode": product_code,
                "timestamp": now,
                "inputHash": report_hash,
                "outputHash": artifact_root,
                "result": "FROZEN_NOT_PUBLISHED",
                "evidence": common_evidence,
            },
            {
                "code": taf_code,
                "type": "FINAL_ACCEPTANCE_PREPARED",
                "subjectCode": product_code,
                "timestamp": now,
                "inputHash": artifact_root,
                "outputHash": hashlib.sha256(taf_code.encode("utf-8")).hexdigest(),
                "result": "PREPARED_AWAITING_LITERAL_OWNER_COMMAND",
                "evidence": {
                    **common_evidence,
                    "requiredCommand": f"PUBLICAR {taf_code}",
                },
            },
        ]
        ledger_next = copy.deepcopy(ledger)
        for event in release_events:
            _append_ledger_event(ledger_next, event)
        ledger_next.update(
            {
                "updatedAt": now,
                "status": "release-prepared-publication-locked",
            }
        )

        updates = {
            report_path: reports_next,
            tombstone_path: tombstones_next,
            manifest_path: manifest_next,
            module_path: module_next,
            catalog_path: catalog_next,
            ledger_path: ledger_next,
        }
        _transactional_json_update(
            updates,
            lambda: validate_release_state(root, public_root=public_root),
            fail_after=fail_after,
        )
        return {
            "status": "SUPERSEDED_PREPUBLICATION",
            "idempotent": False,
            "productCode": product_code,
            "supersededTafCode": supersedes_taf,
            "supersessionProcedureCode": supersession_code,
            "procedureCode": procedure_code,
            "homologationCode": hom_code,
            "tombstoneCode": tom_code,
            "tafCode": taf_code,
            "artifactProfile": POST_BUILD_POST_SANITIZE,
            "artifactRootSha256": artifact_root,
            "memberCount": len(members),
            "publication": "LOCKED",
            "requiredCommand": f"PUBLICAR {taf_code}",
        }
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)


def _validate_block_item(item: dict, block_id: str, schema: dict, relations: set[str]) -> None:
    """Validação fail-closed dos invariantes editoriais usados na árvore pública."""

    required = set(schema.get("required", []))
    properties = set(schema.get("properties", {}))
    if not required or not required.issubset(properties):
        raise ContractError("schema de bloco exige campos ausentes em properties")
    missing = sorted(required - set(item))
    if missing:
        raise ContractError(f"item {item.get('id', '?')} sem campos: {', '.join(missing)}")
    extra = sorted(set(item) - properties)
    if extra:
        raise ContractError(f"item {item.get('id', '?')} contém campos não contratados: {', '.join(extra)}")
    if item.get("blockId") != block_id:
        raise ContractError(f"item {item.get('id', '?')} diverge do bloco {block_id}")
    if not AGX.fullmatch(item.get("productCode", "")):
        raise ContractError(f"item {item.get('id', '?')} possui ####AGX inválido")

    render_statuses = set(
        schema["properties"]["render"]["properties"]["status"].get("enum", [])
    )
    if item.get("render", {}).get("status") not in render_statuses:
        raise ContractError(f"item {item.get('id', '?')} possui render.status inválido")

    privacy = item.get("privacy", {})
    audit = item.get("audit", {})
    public_eligible = privacy.get("publicEligible") is True
    if public_eligible:
        if privacy.get("classification") != "P0" or privacy.get("patientData") is not False:
            raise ContractError(f"item {item.get('id', '?')} tenta publicar privacidade incompatível")
        if audit.get("patientExposure") not in {"passed", "corrected"}:
            raise ContractError(f"item {item.get('id', '?')} sem gate de paciente")
        for field in ("rightsReview", "technicalReview", "linkCheck"):
            if audit.get(field) != "passed":
                raise ContractError(f"item {item.get('id', '?')} sem gate {field}")

        image_paths = {
            artifact.get("path")
            for artifact in item.get("render", {}).get("artifacts", [])
            if artifact.get("kind") == "image"
        }
        if image_paths:
            asset_codes = item.get("assetCodes")
            if not isinstance(asset_codes, list) or len(asset_codes) != len(image_paths):
                raise ContractError(
                    f"item {item.get('id', '?')} precisa catalogar cada imagem com ####IMG"
                )
            coded_paths = {asset.get("path") for asset in asset_codes}
            codes = [asset.get("code") for asset in asset_codes]
            if coded_paths != image_paths or len(codes) != len(set(codes)):
                raise ContractError(
                    f"item {item.get('id', '?')} possui catálogo de imagens incompleto ou duplicado"
                )
            for asset in asset_codes:
                code = asset.get("code", "")
                digest = asset.get("sha256", "")
                if not IMG.fullmatch(code) or not HEX64.fullmatch(digest):
                    raise ContractError(
                        f"item {item.get('id', '?')} possui código ou hash de imagem inválido"
                    )
                if not code.endswith(digest[:8].upper()):
                    raise ContractError(
                        f"item {item.get('id', '?')} usa ####IMG divergente dos bytes servidos"
                    )
                if asset.get("publicationStatus") not in {"candidate-public", "published"}:
                    raise ContractError(
                        f"item {item.get('id', '?')} contém imagem pública sem estado catalogável"
                    )

    if item.get("contentClass") in {"clinical", "mixed"}:
        references = item.get("references", [])
        strong_roles = {reference.get("role") for reference in references}
        if not strong_roles.intersection({"primary", "guideline", "official"}):
            raise ContractError(f"item clínico {item.get('id', '?')} sem referência forte")
        if audit.get("scientificGrounding") != "passed":
            raise ContractError(f"item clínico {item.get('id', '?')} sem gate científico")

    if block_id == "estudo-microparticulado" and public_eligible:
        closed = item.get("closedMicroparticle")
        if not isinstance(closed, dict):
            raise ContractError(
                f"micropartícula pública {item.get('id', '?')} sem contrato de fechamento"
            )
        required_true = {
            "cleanPublicModel",
            "allPromptsAnswered",
            "answersCorrected",
            "answersJustified",
            "selfContained",
            "personalStateRemoved",
        }
        invalid_true = sorted(field for field in required_true if closed.get(field) is not True)
        if invalid_true:
            raise ContractError(
                f"micropartícula pública {item.get('id', '?')} incompleta: "
                + ", ".join(invalid_true)
            )
        if closed.get("ownerCompletionStatus") != "MODULE_COMPLETED_BY_OWNER":
            raise ContractError(
                f"micropartícula pública {item.get('id', '?')} sem conclusão integral do proprietário"
            )
        if closed.get("extractionStatus") != "extracted-clean-model":
            raise ContractError(
                f"micropartícula pública {item.get('id', '?')} não foi extraída como modelo limpo"
            )
        if closed.get("followUpMonitor") is not False or closed.get("recoveryLoop") is not False:
            raise ContractError(
                f"micropartícula pública {item.get('id', '?')} contém monitor ou alça de recuperação"
            )
        references = item.get("references", [])
        reference_roles = {reference.get("role") for reference in references}
        if not reference_roles.intersection({"primary", "guideline", "official", "methodology"}):
            raise ContractError(
                f"micropartícula pública {item.get('id', '?')} sem referência científica pertinente"
            )
        if item.get("provenance", {}).get("reviewStatus") != "reviewed":
            raise ContractError(
                f"micropartícula pública {item.get('id', '?')} sem revisão de proveniência"
            )
        if item.get("render", {}).get("status") not in {"candidate-public", "published"}:
            raise ContractError(
                f"micropartícula pública {item.get('id', '?')} ainda não é um bloco fechado renderizado"
            )
        if audit.get("scientificGrounding") != "passed":
            raise ContractError(
                f"micropartícula pública {item.get('id', '?')} sem gate científico"
            )

    for edge in item.get("edges", []):
        if edge.get("relation") not in relations:
            raise ContractError(f"item {item.get('id', '?')} usa relação fora do vocabulário")


def validate(*, public_root: Path | None = None) -> dict:
    required = [
        "cosmos.json", "atlas.json", "block-registry.json", "tag-topology.json",
        "surface-routing.json", "command-contract.json", "render-recipes.json",
        "product-lifecycle.json", "product-code-contract.json", "product-catalog.json", "entity-code-contract.json",
        "governance-code-contract.json", "sync-contract.json", "content-routing.json",
        "document-sync-contract.json", "living-organism-contract.json",
        "execution-ledger.json", "daily-update-contract.json",
        "editorial-audit-contract.json", "project-domain-routing.json",
        "project-sync-contract.json",
    ]
    payloads = {name: load_json(DATA / name) for name in required}

    cosmos = payloads["cosmos.json"]
    nodes = cosmos.get("nodes", [])
    edges = cosmos.get("edges", [])
    node_ids = [item.get("id") for item in nodes]
    if len(node_ids) != len(set(node_ids)) or any(not value for value in node_ids):
        raise ContractError("IDs de nós ausentes ou duplicados")
    endpoints = set(node_ids)
    invalid_edges = [edge for edge in edges if edge.get("from") not in endpoints or edge.get("to") not in endpoints]
    if invalid_edges:
        raise ContractError(f"Arestas com endpoint inválido: {len(invalid_edges)}")
    if len(cosmos.get("universes", [])) != 3 or len(cosmos.get("constellations", [])) != 7:
        raise ContractError("O organismo exige exatamente 3 universos e 7 constelações")

    topology = payloads["tag-topology.json"]
    relations = set(topology.get("relations", []))
    graph_relations = {edge.get("relation") for edge in edges}
    if not graph_relations.issubset(relations):
        missing_relations = ", ".join(sorted(graph_relations - relations))
        raise ContractError(f"Relações do grafo fora do vocabulário: {missing_relations}")

    schema = load_json(COSMOS / "blocks/_schemas/block-item.schema.json")
    template = load_json(COSMOS / "blocks/_templates/item.template.json")

    blocks = payloads["block-registry.json"].get("blocks", [])
    expected_blocks = {
        "evolucao", "plano-terapeutico", "motor-visual", "organizador-estudos",
        "turbo-temi", "refinaria-temi", "tutor", "estudo-microparticulado",
        "imagens-turbo-temi", "produtos-turbo-temi", "referencias-evidencias",
        "auditoria-publicacao", "extensoes",
    }
    block_ids = {item.get("id") for item in blocks}
    if block_ids != expected_blocks or len(blocks) != len(expected_blocks):
        raise ContractError("Registro de blocos está incompleto ou duplicado")
    for block in blocks:
        path = COSMOS / block["ingestionPath"]
        items = load_json(path).get("items")
        if not isinstance(items, list):
            raise ContractError(f"items inválido: {path.relative_to(ROOT)}")
        for item in items:
            if not isinstance(item, dict):
                raise ContractError(f"item não é objeto: {path.relative_to(ROOT)}")
            _validate_block_item(item, block["id"], schema, relations)
    _validate_block_item(template, "evolucao", schema, relations)

    atlas = payloads["atlas.json"].get("items", [])
    image_codes: set[str] = set()
    for item in atlas:
        path = COSMOS / item["image"]
        actual_hash = sha256_file(path)
        asset = item.get("asset", {})
        if actual_hash != asset.get("sha256"):
            raise ContractError(f"Hash divergente: {path.relative_to(ROOT)}")
        if jpeg_dimensions(path) != (asset.get("width"), asset.get("height")):
            raise ContractError(f"Dimensões divergentes: {path.relative_to(ROOT)}")
        code = item.get("catalogCode", "")
        if code in image_codes or not code.endswith(actual_hash[:8].upper()):
            raise ContractError(f"Código de imagem inválido/duplicado: {code}")
        image_codes.add(code)
        raw = path.read_bytes()
        if b"Exif\x00\x00" in raw or b"Photoshop 3.0" in raw or b"http://ns.adobe.com/xap/1.0/" in raw:
            raise ContractError(f"Metadado sensível residual: {path.relative_to(ROOT)}")

    audit_contract = payloads["editorial-audit-contract.json"]
    pillar_ids = [pillar.get("id") for pillar in audit_contract.get("pillars", [])]
    if pillar_ids != ["patient-exposure", "copyright-rights", "scientific-grounding"]:
        raise ContractError("Auditoria editorial precisa manter os três pilares na ordem canônica")

    domain_contract = payloads["project-domain-routing.json"]
    domains = {item.get("id"): item for item in domain_contract.get("domains", [])}
    if set(domains) != set(DOMAINS):
        raise ContractError("Roteamento de domínios está incompleto")
    for domain_id, config in domains.items():
        if DOMAINS[domain_id]["private"]:
            if config.get("githubEligible") is not False or config.get("officialSiteEligible") is not False:
                raise ContractError(f"Domínio privado {domain_id} permite superfície pública")

    sync = payloads["sync-contract.json"]
    if not sync.get("publicationLock", {}).get("lockedByDefault"):
        raise ContractError("Trava de publicação precisa estar ativa por padrão")
    if sync.get("publicationLock", {}).get("forbiddenWithoutUnlock") != [
        "push main", "merge", "auto-merge", "Pages deploy", "site publisher"
    ]:
        raise ContractError("Fronteira de publicação divergente")

    lifecycle = payloads["product-lifecycle.json"].get("stages", [])
    if [stage.get("order") for stage in lifecycle] != list(range(1, len(lifecycle) + 1)):
        raise ContractError("Etapas do ciclo não são contínuas")
    if [stage.get("id") for stage in lifecycle[-4:]] != ["homologation", "tombstone", "owner-unlock", "publish"]:
        raise ContractError("Fecho HOM → TOM/TAF → autorização → PUB ausente")
    if payloads["governance-code-contract.json"].get("hashInputs", {}).get(
        "TAF###"
    ) != "product_code|audit_code|homologation_code|tombstone_code|artifact_root_sha256":
        raise ContractError("TAF### precisa vincular explicitamente o AUD###")

    products = payloads["product-catalog.json"].get("items", [])
    product_codes = [item.get("productCode") for item in products]
    if len(product_codes) != len(set(product_codes)) or any(
        not AGX.fullmatch(value or "") for value in product_codes
    ):
        raise ContractError("Catálogo de produtos contém código inválido ou duplicado")
    for product in products:
        if product.get("tafCode") is not None and not TAF.fullmatch(product["tafCode"]):
            raise ContractError("Catálogo contém TAF### inválido")
        if product.get("published") and not product.get("tafCode"):
            raise ContractError("Produto publicado sem TAF###")

    release_state = validate_release_state(ROOT, public_root=public_root)

    return {
        "status": "OK",
        "universes": 3,
        "constellations": 7,
        "localNodes": len(nodes),
        "localEdges": len(edges),
        "blocks": len(blocks),
        "images": len(atlas),
        "imageRights": payloads["atlas.json"].get("rights", {}).get("publicationAttestation"),
        "auditPillars": len(pillar_ids),
        "privateDomains": sum(1 for value in DOMAINS.values() if value["private"]),
        "lifecycleStages": len(lifecycle),
        "preparedReleases": release_state["preparedReleases"],
        "ledgerEvents": release_state["ledgerEvents"],
        "publication": "LOCKED",
    }


def _reject_superseded_taf(taf_code: str, root: Path = ROOT) -> None:
    catalog_path = root / "23_Cosmos_NEXUS/data/product-catalog.json"
    if not catalog_path.exists():
        return
    catalog = _load_json_path(catalog_path, "catálogo de produtos")
    for product in catalog.get("items", []):
        for record in product.get("supersededReleases", []):
            if isinstance(record, dict) and record.get("tafCode") == taf_code:
                raise ContractError(
                    "TAF### superseded/VOID_PREPUBLICATION não pode gerar publicação"
                )


def issue_code(args: argparse.Namespace) -> str:
    date = _parse_calendar_date(args.date)
    sequence = f"{args.sequence:04d}"
    if args.sequence < 1 or args.sequence > 9999:
        raise ContractError("sequence deve estar entre 1 e 9999")
    artifact = args.artifact_sha256.lower()
    if not HEX64.fullmatch(artifact):
        raise ContractError("artifact-sha256 deve conter 64 caracteres hexadecimais")

    if args.kind == "procedure":
        action = token(args.action, "action")
        suffix = digest8(action, args.subject, artifact, date, sequence)
        return f"PRC###-{action}-{date}-{sequence}-{suffix}"
    if args.kind == "homologation":
        scope = token(args.scope, "scope")
        suffix = digest8(scope, args.subject, artifact, date, sequence)
        return f"HOM###-{scope}-{date}-{sequence}-{suffix}"
    if args.kind == "audit":
        scope = token(args.scope, "scope")
        suffix = digest8(scope, args.subject, artifact, date, sequence)
        return f"AUD###-{scope}-{date}-{sequence}-{suffix}"
    if args.kind == "tombstone":
        scope = token(args.scope, "scope")
        suffix = digest8(scope, args.subject, artifact, date, sequence)
        return f"TOM###-{scope}-{date}-{sequence}-{suffix}"
    if args.kind == "final-product":
        universe = args.universe.upper()
        block = args.block.upper()
        if universe not in UNIVERSES or block not in BLOCKS:
            raise ContractError("universe/block inválido para TAF###")
        if not AGX.fullmatch(args.product_code or ""):
            raise ContractError("product-code ####AGX válido é obrigatório")
        if not re.fullmatch(r"HOM###[A-Z0-9-]+", args.homologation_code or ""):
            raise ContractError("homologation-code HOM### válido é obrigatório")
        if not re.fullmatch(r"AUD###[A-Z0-9-]+", args.audit_code or ""):
            raise ContractError("audit-code AUD### válido é obrigatório")
        if not re.fullmatch(r"TOM###[A-Z0-9-]+", args.tombstone_code or ""):
            raise ContractError("tombstone-code TOM### válido é obrigatório")
        suffix = digest8(
            args.product_code,
            args.audit_code,
            args.homologation_code,
            args.tombstone_code,
            artifact,
        )
        return f"TAF###-{universe}-{block}-{date}-{sequence}-{suffix}"
    if args.kind == "publication":
        final_code = args.final_product_code or ""
        if not TAF.fullmatch(final_code):
            raise ContractError("final-product-code TAF### válido é obrigatório")
        _reject_superseded_taf(final_code)
        authorization_mode = getattr(
            args, "authorization_mode", "literal-owner-command"
        )
        if authorization_mode == "standing-organization-study-image":
            if getattr(args, "source_project", None) != ORGANIZATION_STUDY_PROJECT:
                raise ContractError(
                    "autorização permanente só vale para @ORGANIZACAODEESTUDO"
                )
            if not re.fullmatch(r"TAF###-(U1|U2|U3|MUX)-IMGT-[0-9]{8}-[0-9]{4}-[A-F0-9]{8}", final_code):
                raise ContractError(
                    "autorização permanente só vale para TAF### de imagem IMGT"
                )
            if not IMG.fullmatch(args.subject):
                raise ContractError(
                    "autorização permanente exige uma imagem ####IMG catalogada como subject"
                )
            authorization_evidence = "STANDING_OWNER_AUTHORIZATION_2026-08-01"
        else:
            expected = f"PUBLICAR {final_code}"
            if args.owner_command != expected:
                raise ContractError(f"autorização literal exigida: {expected}")
            authorization_evidence = args.owner_command
        suffix = digest8(final_code, authorization_evidence, artifact, args.subject)
        return f"PUB###-{date}-{sequence}-{suffix}"
    raise ContractError(f"kind desconhecido: {args.kind}")


def route(kind: str) -> dict:
    routes = load_json(DATA / "content-routing.json").get("routes", [])
    matches = [item for item in routes if item.get("kind") == kind]
    if len(matches) != 1:
        raise ContractError(f"tipo de conteúdo não resolvido de forma única: {kind}")
    return matches[0]


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Barramento local NEXUS Cosmos")
    sub = root.add_subparsers(dest="command", required=True)
    validate_parser = sub.add_parser(
        "validate", help="validar contratos, grafo, blocos e imagens"
    )
    status_parser = sub.add_parser("status", help="mostrar resumo fail-closed")
    for validation_parser in (validate_parser, status_parser):
        validation_parser.add_argument(
            "--public-root",
            help="saída materializada exigida quando houver release de perfil público",
        )
    route_parser = sub.add_parser("route", help="resolver a seção canônica de um conteúdo")
    route_parser.add_argument("--kind", required=True)

    code = sub.add_parser("code", help="gerar código verificável sem gravar ou publicar")
    code.add_argument("--kind", required=True, choices=["procedure", "audit", "homologation", "tombstone", "final-product", "publication"])
    code.add_argument("--date", required=True)
    code.add_argument("--sequence", required=True, type=int)
    code.add_argument("--subject", required=True)
    code.add_argument("--artifact-sha256", required=True)
    code.add_argument("--action", default="EXECUTE")
    code.add_argument("--scope", default="NEXUS-COSMOS")
    code.add_argument("--universe", default="MUX")
    code.add_argument("--block", default="EXT")
    code.add_argument("--product-code")
    code.add_argument("--homologation-code")
    code.add_argument("--audit-code")
    code.add_argument("--tombstone-code")
    code.add_argument("--final-product-code")
    code.add_argument("--owner-command")
    code.add_argument(
        "--authorization-mode",
        default="literal-owner-command",
        choices=["literal-owner-command", "standing-organization-study-image"],
    )
    code.add_argument("--source-project", choices=sorted(SOURCE_PROJECTS))

    intake = sub.add_parser(
        "intake",
        help="registrar Word/PDF/imagem na fila privada de sincronização",
    )
    intake.add_argument("--source", required=True, help="caminho do arquivo materializado")
    intake.add_argument(
        "--block",
        required=True,
        choices=sorted(BLOCK_ALIASES),
        help="sessão/bloco de destino sem #",
    )
    intake.add_argument(
        "--kind",
        default="auto",
        choices=sorted(SAFE_INTAKE_KINDS),
        help="tipo seguro de documento/imagem ou auto",
    )
    intake.add_argument("--universe", default="MUX")
    intake.add_argument("--domain", default="clinical-educational", choices=sorted(DOMAINS))
    intake.add_argument(
        "--source-project",
        choices=sorted(SOURCE_PROJECTS),
        help="alias público do projeto-fonte; IDs internos nunca entram no recibo público",
    )
    intake.add_argument(
        "--owner-completed-module",
        action="store_true",
        help="registra conclusão integral declarada pelo proprietário para @ORGANIZACAODEESTUDO",
    )
    intake.add_argument("--privacy", default="P1", help="P1 privado por padrão; use P0 somente após revisão")
    intake.add_argument("--title")
    intake.add_argument("--objective", default="catalogar-renderizar-sincronizar-rascunho")
    intake.add_argument("--date", default=date.today().isoformat())
    intake.add_argument("--sequence", type=int)
    sub.add_parser("sync-plan", help="listar pendências sem revelar paths ou títulos")
    release = sub.add_parser(
        "prepare-release",
        help="preparar PRC/HOM/TOM/TAF transacionalmente, sem publicar",
    )
    release.add_argument("--product-code", required=True)
    release.add_argument(
        "--evidence",
        required=True,
        help="JSON público e estrito com testes e confirmações humanas",
    )
    release.add_argument("--date", default=date.today().isoformat())
    release.add_argument("--sequence", required=True, type=int)
    release.add_argument(
        "--public-root",
        help="saída materializada após build e sanitize; obrigatória no perfil público",
    )
    validate_release = sub.add_parser(
        "validate-release",
        help="validar ledger, relatórios, tombstones e TAF sem publicar",
    )
    validate_release.add_argument(
        "--public-root",
        help="saída materializada após build e sanitize; obrigatória no perfil público",
    )
    inventory = sub.add_parser(
        "release-inventory",
        help="calcular membros/root e modelo de evidência PENDING sem gravar",
    )
    inventory.add_argument("--product-code", required=True)
    inventory.add_argument(
        "--public-root",
        help="saída materializada após build e sanitize; obrigatória no perfil público",
    )
    supersede_inventory_parser = sub.add_parser(
        "supersede-inventory",
        help="calcular root público para substituir TAF LOCKED sem gravar",
    )
    supersede_inventory_parser.add_argument("--product-code", required=True)
    supersede_inventory_parser.add_argument("--supersedes-taf", required=True)
    supersede_inventory_parser.add_argument("--public-root", required=True)
    supersede_inventory_parser.add_argument(
        "--previous-public-root",
        help="snapshot público anterior; obrigatório para cadeia POST_BUILD",
    )
    supersede = sub.add_parser(
        "supersede-release",
        help="substituir cadeia LOCKED pré-publicação sem apagar histórico",
    )
    supersede.add_argument("--product-code", required=True)
    supersede.add_argument("--supersedes-taf", required=True)
    supersede.add_argument("--evidence", required=True)
    supersede.add_argument("--date", default=date.today().isoformat())
    supersede.add_argument("--sequence", required=True, type=int)
    supersede.add_argument("--public-root", required=True)
    supersede.add_argument(
        "--previous-public-root",
        help="snapshot público anterior; obrigatório para cadeia POST_BUILD",
    )
    supersede.add_argument(
        "--reason",
        required=True,
        choices=[SUPERSESSION_REASON],
    )
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command in {"validate", "status"}:
            print(
                json.dumps(
                    validate(
                        public_root=(
                            Path(args.public_root).expanduser()
                            if args.public_root
                            else None
                        )
                    ),
                    ensure_ascii=False,
                    indent=2,
                )
            )
        elif args.command == "route":
            print(json.dumps(route(args.kind), ensure_ascii=False, indent=2))
        elif args.command == "code":
            print(issue_code(args))
        elif args.command == "intake":
            result = enqueue_intake(args)
            public_result = {
                "queueResult": result.get("queueResult"),
                "receiptFile": result.get("receiptFile"),
                "entityCode": result.get("entityCode"),
                "projectCode": result.get("projectCode"),
                "productCode": result.get("productCode"),
                "procedureCode": result.get("procedureCode"),
                "privacy": result.get("privacy"),
                "domain": result.get("domain"),
                "surfaceStates": {
                    name: value.get("status")
                    for name, value in result.get("surfaces", {}).items()
                    if isinstance(value, dict)
                },
                "publication": result.get("publication", {}).get("status"),
            }
            if result.get("queueResult") == "REVIEW_REQUIRED_PRIVACY_CHANGE":
                public_result["requestedPrivacy"] = result.get("requestedPrivacy")
            print(json.dumps(public_result, ensure_ascii=False, indent=2))
        elif args.command == "sync-plan":
            print(json.dumps(sync_plan(), ensure_ascii=False, indent=2))
        elif args.command == "prepare-release":
            result = prepare_release(
                args.product_code,
                Path(args.evidence).expanduser(),
                args.date,
                args.sequence,
                public_root=(
                    Path(args.public_root).expanduser()
                    if args.public_root
                    else None
                ),
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.command == "validate-release":
            print(
                json.dumps(
                    validate_release_state(
                        public_root=(
                            Path(args.public_root).expanduser()
                            if args.public_root
                            else None
                        )
                    ),
                    ensure_ascii=False,
                    indent=2,
                )
            )
        elif args.command == "release-inventory":
            print(
                json.dumps(
                    release_inventory(
                        args.product_code,
                        public_root=(
                            Path(args.public_root).expanduser()
                            if args.public_root
                            else None
                        ),
                    ),
                    ensure_ascii=False,
                    indent=2,
                )
            )
        elif args.command == "supersede-inventory":
            print(
                json.dumps(
                    supersession_inventory(
                        args.product_code,
                        args.supersedes_taf,
                        public_root=Path(args.public_root).expanduser(),
                        previous_public_root=(
                            Path(args.previous_public_root).expanduser()
                            if args.previous_public_root
                            else None
                        ),
                    ),
                    ensure_ascii=False,
                    indent=2,
                )
            )
        elif args.command == "supersede-release":
            print(
                json.dumps(
                    supersede_release(
                        args.product_code,
                        args.supersedes_taf,
                        Path(args.evidence).expanduser(),
                        args.date,
                        args.sequence,
                        reason=args.reason,
                        public_root=Path(args.public_root).expanduser(),
                        previous_public_root=(
                            Path(args.previous_public_root).expanduser()
                            if args.previous_public_root
                            else None
                        ),
                    ),
                    ensure_ascii=False,
                    indent=2,
                )
            )
    except ContractError as exc:
        print(f"BLOQUEADO: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
