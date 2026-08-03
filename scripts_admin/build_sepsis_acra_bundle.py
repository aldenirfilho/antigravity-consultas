#!/usr/bin/env python3
"""Gera o bundle ACRA offline da sessão Sepse Ultra Expert.

Os dez JSON em ``acra/`` são a fonte canônica. O arquivo JavaScript derivado
não contém data de geração, depende apenas desses arquivos e pode ser conferido
sem escrita com ``--check``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "01_Modulos_Clinicos" / "Sepse_Choque_Septico"
SOURCE_DIR = MODULE / "acra"
OUTPUT = MODULE / "data" / "acra-bundle.js"

BUNDLE_SCHEMA = "antigravity-sepsis-acra-bundle-v1"
ARTIFACT_SCHEMA = "1.0"
EXPECTED_ARTIFACTS = 10
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{2,63}$")
FILE_PATTERN = re.compile(r"^acra-sepse-(\d{2})-[a-z0-9-]+\.json$")
ALLOWED_COMPONENTS = frozenset(
    {
        "callout",
        "tabs",
        "accordion",
        "cards",
        "numberedSteps",
        "comparisonTable",
        "thresholdTable",
        "checklist",
        "quiz",
        "keyValueGrid",
        "sources",
        "progress",
        "followupActions",
    }
)
ALLOWED_ACTIONS = frozenset(
    {"continueResearch", "deepen", "compare", "verify", "quiz", "review"}
)
ROOT_KEYS = frozenset(
    {
        "version",
        "id",
        "title",
        "subtitle",
        "mode",
        "summary",
        "critical",
        "components",
        "actions",
        "sources",
    }
)


class BundleError(ValueError):
    """Erro determinístico de contrato do bundle."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BundleError(message)


def is_https_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlsplit(value)
    return (
        parsed.scheme == "https"
        and bool(parsed.netloc)
        and not parsed.username
        and not parsed.password
    )


def collect_ids(value: object, *, path: str, seen: set[str]) -> None:
    if isinstance(value, dict):
        item_id = value.get("id")
        if item_id is not None:
            require(
                isinstance(item_id, str) and bool(ID_PATTERN.fullmatch(item_id)),
                f"{path}: identificador ACRA inválido",
            )
            require(item_id not in seen, f"{path}: identificador duplicado: {item_id}")
            seen.add(item_id)
        for key, nested in value.items():
            collect_ids(nested, path=f"{path}/{key}", seen=seen)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            collect_ids(nested, path=f"{path}/{index}", seen=seen)


def validate_artifact(artifact: object, *, filename: str) -> dict[str, object]:
    require(isinstance(artifact, dict), f"{filename}: raiz deve ser objeto")
    require(set(artifact) == ROOT_KEYS, f"{filename}: propriedades de raiz inválidas")
    require(artifact["version"] == ARTIFACT_SCHEMA, f"{filename}: schema não suportado")
    require(artifact["mode"] == "tutorial", f"{filename}: modo deve ser tutorial")

    for key in ("id", "title", "subtitle", "summary"):
        require(
            isinstance(artifact[key], str) and bool(artifact[key].strip()),
            f"{filename}: {key} deve ser texto não vazio",
        )

    critical = artifact["critical"]
    components = artifact["components"]
    actions = artifact["actions"]
    sources = artifact["sources"]
    require(isinstance(critical, list) and critical, f"{filename}: critical vazio")
    require(
        isinstance(components, list) and 1 <= len(components) <= 24,
        f"{filename}: quantidade de componentes inválida",
    )
    require(isinstance(actions, list) and actions, f"{filename}: actions vazio")
    require(isinstance(sources, list) and sources, f"{filename}: sources vazio")

    component_ids: set[str] = set()
    source_ids: set[str] = set()
    action_ids: set[str] = set()
    for component in components:
        require(isinstance(component, dict), f"{filename}: componente inválido")
        require(
            component.get("type") in ALLOWED_COMPONENTS,
            f"{filename}: componente não permitido: {component.get('type')!r}",
        )
        require(isinstance(component.get("id"), str), f"{filename}: componente sem id")
        component_ids.add(component["id"])

        if component["type"] == "comparisonTable":
            columns = component.get("columns")
            rows = component.get("rows")
            require(isinstance(columns, list) and columns, f"{filename}: tabela sem colunas")
            require(isinstance(rows, list) and rows, f"{filename}: tabela sem linhas")
            for row in rows:
                require(
                    isinstance(row, dict)
                    and isinstance(row.get("cells"), list)
                    and len(row["cells"]) == len(columns),
                    f"{filename}: células não correspondem às colunas",
                )

        if component["type"] == "quiz":
            questions = component.get("questions")
            require(isinstance(questions, list) and questions, f"{filename}: quiz vazio")
            for question in questions:
                require(isinstance(question, dict), f"{filename}: questão inválida")
                options = question.get("options")
                require(isinstance(options, list) and len(options) >= 2, f"{filename}: opções inválidas")
                option_ids = {
                    option.get("id") for option in options if isinstance(option, dict)
                }
                require(
                    question.get("correctOptionId") in option_ids,
                    f"{filename}: resposta correta não referencia uma opção",
                )

    require(
        len(component_ids) == len(components),
        f"{filename}: ids de componente duplicados",
    )

    for source in sources:
        require(isinstance(source, dict), f"{filename}: fonte inválida")
        require(is_https_url(source.get("url")), f"{filename}: fonte deve usar HTTPS")
        require(isinstance(source.get("id"), str), f"{filename}: fonte sem id")
        source_ids.add(source["id"])
    require(len(source_ids) == len(sources), f"{filename}: ids de fonte duplicados")

    for action in actions:
        require(isinstance(action, dict), f"{filename}: ação inválida")
        require(action.get("kind") in ALLOWED_ACTIONS, f"{filename}: ação não permitida")
        require(action.get("requiresPreview") is True, f"{filename}: ação sem prévia obrigatória")
        require(isinstance(action.get("id"), str), f"{filename}: ação sem id")
        contexts = action.get("contextComponentIds")
        require(isinstance(contexts, list), f"{filename}: contexto de ação inválido")
        require(
            not (set(contexts) - component_ids),
            f"{filename}: ação referencia componente inexistente",
        )
        action_ids.add(action["id"])
    require(len(action_ids) == len(actions), f"{filename}: ids de ação duplicados")

    for component in components:
        if component["type"] == "sources":
            require(
                set(component.get("sourceIds", [])) == source_ids,
                f"{filename}: componente sources não coincide com as fontes",
            )
        if component["type"] == "followupActions":
            require(
                set(component.get("actionIds", [])) == action_ids,
                f"{filename}: followupActions não coincide com as ações",
            )

    collect_ids(artifact, path=f"/{filename}", seen=set())
    return artifact


def source_paths() -> list[Path]:
    paths = sorted(SOURCE_DIR.glob("*.json"), key=lambda item: item.name)
    require(
        len(paths) == EXPECTED_ARTIFACTS,
        f"esperados {EXPECTED_ARTIFACTS} JSON canônicos; encontrados {len(paths)}",
    )
    ordinals: list[int] = []
    for path in paths:
        match = FILE_PATTERN.fullmatch(path.name)
        require(match is not None, f"nome canônico inválido: {path.name}")
        ordinals.append(int(match.group(1)))
    require(ordinals == list(range(1, 11)), "a sequência canônica deve ser 01–10")
    return paths


def canonical_json(value: object, *, pretty: bool = False) -> str:
    if pretty:
        return json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        allow_nan=False,
    )


def build_payload() -> dict[str, object]:
    entries: list[dict[str, object]] = []
    artifact_ids: set[str] = set()

    for path in source_paths():
        raw = path.read_bytes()
        try:
            artifact = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise BundleError(f"{path.name}: JSON inválido: {error}") from error
        validated = validate_artifact(artifact, filename=path.name)
        require(validated["id"] not in artifact_ids, f"id global duplicado: {validated['id']}")
        artifact_ids.add(str(validated["id"]))
        entries.append(
            {
                "artifact": validated,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "source": f"acra/{path.name}",
            }
        )

    content_digest = hashlib.sha256(
        canonical_json([entry["artifact"] for entry in entries]).encode("utf-8")
    ).hexdigest()
    return {
        "artifactCount": EXPECTED_ARTIFACTS,
        "artifactSchemaVersion": ARTIFACT_SCHEMA,
        "contentSha256": content_digest,
        "entries": entries,
        "schemaVersion": BUNDLE_SCHEMA,
    }


def render_bundle(payload: dict[str, object]) -> str:
    serialized = canonical_json(payload, pretty=True)
    return f'''/* Gerado por scripts_admin/build_sepsis_acra_bundle.py. Não editar. */
(function registerSepsisAcraBundle(root) {{
  "use strict";

  const bundle = {serialized};

  function deepFreeze(value) {{
    if (!value || typeof value !== "object" || Object.isFrozen(value)) return value;
    Object.keys(value).forEach((key) => deepFreeze(value[key]));
    return Object.freeze(value);
  }}

  Object.defineProperty(root, "SEPSE_ACRA_BUNDLE", {{
    configurable: false,
    enumerable: true,
    value: deepFreeze(bundle),
    writable: false
  }});
}})(globalThis);
'''


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="confere paridade sem alterar o bundle",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        expected = render_bundle(build_payload())
    except BundleError as error:
        print(f"ERRO: {error}", file=sys.stderr)
        return 2

    if args.check:
        if not OUTPUT.is_file():
            print(f"ERRO: bundle ausente: {OUTPUT.relative_to(ROOT)}", file=sys.stderr)
            return 1
        actual = OUTPUT.read_text(encoding="utf-8")
        if actual != expected:
            print("ERRO: bundle ACRA desatualizado; execute o builder.", file=sys.stderr)
            return 1
        print(f"PASS: bundle ACRA em paridade ({EXPECTED_ARTIFACTS}/10).")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    previous = OUTPUT.read_text(encoding="utf-8") if OUTPUT.is_file() else None
    if previous == expected:
        print(f"PASS: bundle ACRA já estava em paridade ({EXPECTED_ARTIFACTS}/10).")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    print(f"GERADO: {OUTPUT.relative_to(ROOT)} ({EXPECTED_ARTIFACTS}/10).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
