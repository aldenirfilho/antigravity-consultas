#!/usr/bin/env python3
"""Preparação transacional e fail-closed do aceite NEXUS."""

from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]


def load_bus():
    spec = importlib.util.spec_from_file_location(
        "nexus_release_preparation_test",
        ROOT / "scripts_admin/nexus_cosmos.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


class NexusReleasePreparationTests(unittest.TestCase):
    bus = load_bus()

    def test_taf_contract_binds_the_audit_code(self) -> None:
        governance = json.loads(
            (ROOT / "23_Cosmos_NEXUS/data/governance-code-contract.json").read_text(
                encoding="utf-8"
            )
        )
        entities = json.loads(
            (ROOT / "23_Cosmos_NEXUS/data/entity-code-contract.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            governance["hashInputs"]["TAF###"],
            "product_code|audit_code|homologation_code|tombstone_code|artifact_root_sha256",
        )
        final_product = next(
            item for item in entities["entities"] if item["entity"] == "final-product"
        )
        self.assertIn("audit_code", final_product["identity"])

    def make_fixture(self, root: Path) -> tuple[str, Path, dict[str, Path]]:
        product_code = "####AGX-MUX-PROD-20260801-0009-AAAAAAAA"
        module = root / "23_Cosmos_NEXUS"
        data = module / "data"
        product = module / "products/produto-fixture"
        assets = product / "assets"
        assets.mkdir(parents=True)
        (product / "index.html").write_text("<!doctype html><title>Fixture</title>\n", encoding="utf-8")
        (product / "styles.css").write_text("body { color: #fff; }\n", encoding="utf-8")
        write_json(product / "references.json", {"items": []})
        png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwC"
            "AAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        )
        asset_path = assets / "visual.png"
        asset_path.write_bytes(png)
        asset_hash = hashlib.sha256(png).hexdigest()
        aggregate_input = f"1\t{asset_hash}\t{len(png)}\n"
        aggregate_hash = hashlib.sha256(aggregate_input.encode("utf-8")).hexdigest()
        audit_input = "|".join(
            [
                product_code,
                aggregate_hash,
                "patient:passed",
                "rights:passed",
                "science:passed",
                "technical:passed",
                "links:passed",
            ]
        )
        audit_evidence_hash = hashlib.sha256(audit_input.encode("utf-8")).hexdigest()
        audit_code = f"AUD###-PROD-20260801-0009-{audit_evidence_hash[:8].upper()}"
        manifest = {
            "schemaVersion": "antigravity-candidate-product-manifest-v1",
            "identity": {
                "id": "produto-fixture",
                "semanticKey": "produto-fixture",
                "title": "Produto fixture",
                "version": "1.0.0",
                "productCode": product_code,
                "productUid": "a" * 64,
                "auditCode": audit_code,
            },
            "classification": {
                "contentClass": "non-clinical",
                "privacy": "P0",
                "synthetic": True,
                "patientData": False,
                "publicEligible": True,
            },
            "publication": {
                "status": "candidate-public",
                "officialPublication": False,
                "finalAcceptanceCode": None,
                "officialPublicationCode": None,
                "releaseBoundary": "Somente preparação; publicação bloqueada.",
            },
            "assets": [
                {
                    "slot": 1,
                    "catalogCode": f"####IMG-20260801-0001-{asset_hash[:8].upper()}",
                    "publicationStatus": "candidate-public",
                    "path": "assets/visual.png",
                    "title": "Visual fixture",
                    "mime": "image/png",
                    "width": 1,
                    "height": 1,
                    "bytes": len(png),
                    "sha256": asset_hash,
                    "alt": "Pixel sintético de teste.",
                }
            ],
            "bundle": {
                "assetCatalogAlgorithm": "SHA256 de linhas slot, hash e bytes",
                "aggregateSha256": aggregate_hash,
                "assetCount": 1,
                "totalBytes": len(png),
            },
            "audit": {
                "outcome": "PASS",
                "auditEvidenceSha256": audit_evidence_hash,
                "patientExposure": {"status": "passed"},
                "rightsReview": {"status": "passed"},
                "scientificGrounding": {"status": "passed"},
                "technicalReview": {"status": "passed"},
                "linkCheck": {"status": "passed"},
            },
            "entrypoints": {
                "page": "index.html",
                "styles": "styles.css",
                "references": "references.json",
            },
        }
        manifest_path = product / "product.manifest.json"
        write_json(manifest_path, manifest)
        _, artifact_root = self.bus._release_artifact_inventory(
            root, manifest_path, manifest
        )
        manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        catalog = {
            "schemaVersion": "antigravity-cosmos-product-catalog-v1",
            "version": "1.0.0",
            "updatedAt": "2026-08-01",
            "items": [
                {
                    "productCode": product_code,
                    "productUid": "a" * 64,
                    "title": "Produto fixture",
                    "semanticKey": "produto-fixture",
                    "version": "1.0.0",
                    "universe": "MUX",
                    "block": "PROD",
                    "privacy": "P0",
                    "artifactProfile": self.bus.SOURCE_BOUND,
                    "status": "CANDIDATE_PUBLIC",
                    "source": {
                        "path": manifest_path.relative_to(root).as_posix(),
                        "sha256": manifest_hash,
                    },
                    "graphNode": "produto-fixture",
                    "auditCode": audit_code,
                    "homologationCode": None,
                    "tombstoneCode": None,
                    "tafCode": None,
                    "published": False,
                    "gates": {
                        "automatedTechnical": "APROVADO_LOCAL",
                        "humanVisual": "PENDENTE",
                        "clinical": "PENDENTE",
                        "rights": "APROVADO",
                        "ownerUnlock": "AUSENTE",
                    },
                }
            ],
        }
        write_json(data / "product-catalog.json", catalog)
        write_json(
            data / "execution-ledger.json",
            {
                "schemaVersion": "antigravity-execution-ledger-v1",
                "version": "1.0.0",
                "updatedAt": "2026-08-01",
                "status": "ready-empty",
                "events": [],
                "rules": ["Append-only"],
            },
        )
        write_json(
            module / "module.manifest.json",
            {
                "schemaVersion": "antigravity-cosmos-module-v1",
                "publication": {
                    "published": False,
                    "unlockCommand": "PUBLICAR {TAF###-EXATO}",
                },
                "candidateProducts": [
                    {
                        "id": "produto-fixture",
                        "productCode": product_code,
                        "status": "candidate-public",
                        "officialPublication": False,
                    }
                ],
            },
        )
        evidence = {
            "schemaVersion": "antigravity-release-evidence-v1",
            "productCode": product_code,
            "reviewer": "Revisor humano fixture",
            "reviewedAt": "2026-08-01T12:00:00-03:00",
            "confirmations": {
                "safariMacOS": "PASS",
                "safariIPhone": "PASS",
                "clinicalReview": "PASS",
                "rightsReview": "PASS",
            },
            "auditBinding": {
                "auditCode": audit_code,
                "artifactRootSha256": artifact_root,
                "status": "PASS",
            },
            "testRuns": [
                {
                    "id": "unit-tests",
                    "command": "python3 -m unittest tests.test_fixture",
                    "status": "PASS",
                    "summary": "1 teste executado sem falha",
                    "executedAt": "2026-08-01T11:55:00-03:00",
                }
            ],
            "notes": ["Fixture sem dados pessoais."],
        }
        evidence_path = root / "evidence.json"
        write_json(evidence_path, evidence)
        return product_code, evidence_path, {
            "catalog": data / "product-catalog.json",
            "ledger": data / "execution-ledger.json",
            "module": module / "module.manifest.json",
            "manifest": manifest_path,
            "asset": asset_path,
        }

    def prepare(self, root: Path, product_code: str, evidence: Path, **kwargs):
        return self.bus.prepare_release(
            product_code,
            evidence,
            "2026-08-01",
            9,
            root=root,
            **kwargs,
        )

    def make_umbrella_fixture(
        self,
        root: Path,
        *,
        member_root: str = "23_Cosmos_NEXUS",
        include_radar: bool = False,
    ) -> tuple[str, Path, dict[str, Path]]:
        product_code, _, paths = self.make_fixture(root)
        module = root / "23_Cosmos_NEXUS"
        umbrella_path = module / "releases/nexus-station.manifest.json"
        page_path = module / "index.html"
        page_path.write_text(
            "<!doctype html><title>Estação NEXUS homologável</title>\n",
            encoding="utf-8",
        )
        station_path = module / "data/station.json"
        write_json(station_path, {"privacy": "P0", "patientData": False})
        image_path = module / "assets/atlas/visual.png"
        image_path.parent.mkdir(parents=True, exist_ok=True)
        image_bytes = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwC"
            "AAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        )
        image_path.write_bytes(image_bytes)
        member_paths = [image_path, station_path, page_path]
        if include_radar:
            radar_path = root / "15_Radar_Cientifico/data/umbrella-feed.json"
            write_json(
                radar_path,
                {"privacy": "P0", "patientData": False, "reviewStatus": "reviewed"},
            )
            member_paths.append(radar_path)
        members = []
        for path in sorted(member_paths):
            relative = path.relative_to(root).as_posix()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            member = {
                "path": relative,
                "kind": "image" if path == image_path else "file",
                "sha256": digest,
                "bytes": path.stat().st_size,
            }
            if path == image_path:
                member["catalogCode"] = (
                    f"####IMG-20260801-0099-{digest[:8].upper()}"
                )
            members.append(member)
        root_lines = "".join(
            f"{member['path']}\t{member['sha256']}\t{member['bytes']}\n"
            for member in members
        )
        artifact_root = hashlib.sha256(root_lines.encode("utf-8")).hexdigest()
        audit_input = "|".join(
            [
                product_code,
                artifact_root,
                "patient:passed",
                "rights:passed",
                "science:passed",
                "technical:passed",
                "links:passed",
            ]
        )
        audit_hash = hashlib.sha256(audit_input.encode("utf-8")).hexdigest()
        audit_code = f"AUD###-EXT-20260801-0009-{audit_hash[:8].upper()}"
        manifest = {
            "schemaVersion": self.bus.UMBRELLA_RELEASE_SCHEMA,
            "identity": {
                "id": "nexus-station",
                "semanticKey": "nexus-station",
                "title": "Estação NEXUS",
                "version": "1.0.0",
                "productCode": product_code,
                "productUid": "a" * 64,
                "auditCode": audit_code,
            },
            "classification": {
                "contentClass": "mixed",
                "privacy": "P0",
                "synthetic": True,
                "patientData": False,
                "publicEligible": True,
            },
            "publication": {
                "status": "candidate-public",
                "officialPublication": False,
                "finalAcceptanceCode": None,
                "officialPublicationCode": None,
                "releaseBoundary": "Somente preparação; publicação bloqueada.",
            },
            "memberRoot": member_root,
            "members": members,
            "bundle": {
                "inventoryPolicy": self.bus.UMBRELLA_INVENTORY_POLICY,
                "memberRootAlgorithm": self.bus.UMBRELLA_ROOT_ALGORITHM,
                "memberCount": len(members),
                "totalBytes": sum(member["bytes"] for member in members),
                "aggregateSha256": artifact_root,
            },
            "audit": {
                "outcome": "PASS",
                "auditEvidenceSha256": audit_hash,
                "patientExposure": {"status": "passed"},
                "rightsReview": {"status": "passed"},
                "scientificGrounding": {"status": "passed"},
                "technicalReview": {"status": "passed"},
                "linkCheck": {"status": "passed"},
            },
        }
        write_json(umbrella_path, manifest)
        catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
        product = catalog["items"][0]
        product["source"] = {
            "path": umbrella_path.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(umbrella_path.read_bytes()).hexdigest(),
        }
        product["auditCode"] = audit_code
        write_json(paths["catalog"], catalog)
        evidence = {
            "schemaVersion": "antigravity-release-evidence-v1",
            "productCode": product_code,
            "reviewer": "Revisor humano fixture",
            "reviewedAt": "2026-08-01T12:00:00-03:00",
            "confirmations": {
                "safariMacOS": "PASS",
                "safariIPhone": "PASS",
                "clinicalReview": "PASS",
                "rightsReview": "PASS",
            },
            "auditBinding": {
                "auditCode": audit_code,
                "artifactRootSha256": artifact_root,
                "status": "PASS",
            },
            "testRuns": [
                {
                    "id": "umbrella-tests",
                    "command": "python3 -m unittest tests.test_umbrella",
                    "status": "PASS",
                    "summary": "Teste guarda-chuva executado sem falha",
                    "executedAt": "2026-08-01T11:55:00-03:00",
                }
            ],
            "notes": ["Fixture guarda-chuva P0 sem dados pessoais."],
        }
        evidence_path = root / "umbrella-evidence.json"
        write_json(evidence_path, evidence)
        paths.update(
            {
                "manifest": umbrella_path,
                "page": page_path,
                "station": station_path,
                "umbrella_image": image_path,
            }
        )
        return product_code, evidence_path, paths

    def update_umbrella_source_hash(self, paths: dict[str, Path]) -> None:
        catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
        catalog["items"][0]["source"]["sha256"] = hashlib.sha256(
            paths["manifest"].read_bytes()
        ).hexdigest()
        write_json(paths["catalog"], catalog)

    def set_artifact_profile(
        self,
        paths: dict[str, Path],
        artifact_profile: str,
    ) -> None:
        catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
        catalog["items"][0]["artifactProfile"] = artifact_profile
        write_json(paths["catalog"], catalog)

    def bind_evidence_to_inventory(self, evidence: Path, inventory: dict) -> None:
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        payload["auditBinding"]["artifactRootSha256"] = inventory[
            "artifactRootSha256"
        ]
        write_json(evidence, payload)

    def make_supersession_fixture(
        self,
        workspace: Path,
    ) -> tuple[Path, Path, str, Path, dict[str, Path], dict, dict]:
        root = workspace / "source"
        public_root = workspace / "site"
        product_code, evidence, paths = self.make_fixture(root)
        old_release = self.prepare(root, product_code, evidence)
        shutil.copytree(root, public_root)
        public_product = public_root / paths["manifest"].parent.relative_to(root)
        public_page = public_product / "index.html"
        public_page.write_text(
            public_page.read_text(encoding="utf-8")
            + "<footer data-editorial-attribution>Antigravity</footer>\n",
            encoding="utf-8",
        )
        public_references = public_product / "references.json"
        references = json.loads(public_references.read_text(encoding="utf-8"))
        references["totalFiles"] = len(references["items"])
        write_json(public_references, references)
        inventory = self.bus.supersession_inventory(
            product_code,
            old_release["tafCode"],
            root=root,
            public_root=public_root,
        )
        self.bind_evidence_to_inventory(evidence, inventory)
        paths.update(
            {
                "tombstones": root / "23_Cosmos_NEXUS/data/tombstone-manifest.json",
                "reports": root / "23_Cosmos_NEXUS/data/homologation-reports.json",
                "public_page": public_page,
            }
        )
        return (
            root,
            public_root,
            product_code,
            evidence,
            paths,
            old_release,
            inventory,
        )

    def test_prepares_real_members_and_keeps_publication_locked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, evidence, paths = self.make_fixture(root)
            catalog_before_inventory = paths["catalog"].read_bytes()
            inventory = self.bus.release_inventory(product_code, root)
            self.assertEqual(inventory["memberCount"], 4)
            self.assertEqual(inventory["evidenceTemplate"]["auditBinding"]["status"], "PENDING")
            self.assertEqual(paths["catalog"].read_bytes(), catalog_before_inventory)
            result = self.prepare(root, product_code, evidence)

            self.assertEqual(result["status"], "PREPARED")
            self.assertRegex(result["procedureCode"], r"^PRC###-PREPARAR-RELEASE-")
            self.assertRegex(result["homologationCode"], r"^HOM###-")
            self.assertRegex(result["tombstoneCode"], r"^TOM###-")
            self.assertRegex(result["tafCode"], r"^TAF###-MUX-PROD-")
            self.assertEqual(result["publication"], "LOCKED")
            self.assertEqual(result["memberCount"], 4)

            state = self.bus.validate_release_state(root)
            self.assertEqual(state["preparedReleases"], 1)
            self.assertEqual(state["ledgerEvents"], 5)
            catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
            product = catalog["items"][0]
            self.assertFalse(product["published"])
            self.assertEqual(product["gates"]["ownerUnlock"], "AUSENTE")
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            self.assertFalse(manifest["publication"]["officialPublication"])
            self.assertIsNone(manifest["publication"]["officialPublicationCode"])
            self.assertEqual(
                manifest["publication"]["requiredCommand"],
                f"PUBLICAR {result['tafCode']}",
            )
            publication_args = SimpleNamespace(
                kind="publication",
                date="2026-08-01",
                sequence=9,
                artifact_sha256=result["artifactRootSha256"],
                subject=product_code,
                final_product_code=result["tafCode"],
                owner_command="publicar oficial",
                authorization_mode="literal-owner-command",
                source_project=None,
            )
            with self.assertRaisesRegex(self.bus.ContractError, "autorização literal"):
                self.bus.issue_code(publication_args)
            publication_args.owner_command = f"PUBLICAR {result['tafCode']}"
            self.assertRegex(self.bus.issue_code(publication_args), r"^PUB###-")

    def test_prepares_repo_relative_umbrella_and_keeps_publication_locked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, evidence, _ = self.make_umbrella_fixture(root)
            inventory = self.bus.release_inventory(product_code, root)
            self.assertEqual(inventory["memberCount"], 3)
            image_members = [
                member for member in inventory["members"]
                if member["kind"] == "image"
            ]
            self.assertEqual(len(image_members), 1)
            self.assertRegex(image_members[0]["catalogCode"], r"^####IMG-")
            self.assertTrue(
                all(
                    "catalogCode" not in member
                    for member in inventory["members"]
                    if member["kind"] == "file"
                )
            )

            first = self.prepare(root, product_code, evidence)
            self.assertEqual(first["status"], "PREPARED")
            self.assertEqual(first["publication"], "LOCKED")
            self.assertEqual(first["memberCount"], 3)
            second = self.prepare(root, product_code, evidence)
            self.assertEqual(second["status"], "ALREADY_PREPARED")
            self.assertEqual(second["tafCode"], first["tafCode"])
            self.assertEqual(
                self.bus.validate_release_state(root)["publication"],
                "LOCKED",
            )

    def test_post_build_profile_tombstones_public_bytes_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            root = workspace / "source"
            public_root = workspace / "site"
            product_code, evidence, paths = self.make_fixture(root)
            self.set_artifact_profile(
                paths,
                self.bus.POST_BUILD_POST_SANITIZE,
            )
            shutil.copytree(root, public_root)
            public_page = public_root / paths["manifest"].parent.relative_to(root) / "index.html"
            public_page.write_text(
                public_page.read_text(encoding="utf-8")
                + "<footer data-editorial-attribution>Antigravity</footer>\n",
                encoding="utf-8",
            )
            public_references = public_page.parent / "references.json"
            references = json.loads(public_references.read_text(encoding="utf-8"))
            references["totalFiles"] = len(references["items"])
            write_json(public_references, references)

            with self.assertRaisesRegex(self.bus.ContractError, "--public-root"):
                self.bus.release_inventory(product_code, root)
            with self.assertRaisesRegex(self.bus.ContractError, "saída dedicada"):
                self.bus.release_inventory(
                    product_code,
                    root,
                    public_root=root,
                )
            public_link = workspace / "site-link"
            public_link.symlink_to(public_root, target_is_directory=True)
            with self.assertRaisesRegex(self.bus.ContractError, "não symlink"):
                self.bus.release_inventory(
                    product_code,
                    root,
                    public_root=public_link,
                )

            inventory = self.bus.release_inventory(
                product_code,
                root,
                public_root=public_root,
            )
            self.assertEqual(
                inventory["artifactProfile"],
                self.bus.POST_BUILD_POST_SANITIZE,
            )
            self.bind_evidence_to_inventory(evidence, inventory)
            source_page = paths["manifest"].parent / "index.html"
            public_member = next(
                member
                for member in inventory["members"]
                if member["path"].endswith("/index.html")
            )
            self.assertEqual(
                public_member["sha256"],
                hashlib.sha256(public_page.read_bytes()).hexdigest(),
            )
            self.assertNotEqual(
                public_member["sha256"],
                hashlib.sha256(source_page.read_bytes()).hexdigest(),
            )

            result = self.prepare(
                root,
                product_code,
                evidence,
                public_root=public_root,
            )
            self.assertEqual(
                result["artifactProfile"],
                self.bus.POST_BUILD_POST_SANITIZE,
            )
            tombstones = json.loads(
                (root / "23_Cosmos_NEXUS/data/tombstone-manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            tombstone = tombstones["items"][0]
            self.assertEqual(
                tombstone["artifactProfile"],
                self.bus.POST_BUILD_POST_SANITIZE,
            )
            self.assertEqual(tombstone["members"], inventory["members"])
            with self.assertRaisesRegex(self.bus.ContractError, "--public-root"):
                self.bus.validate_release_state(root)
            self.assertEqual(
                self.bus.validate_release_state(
                    root,
                    public_root=public_root,
                )["publication"],
                "LOCKED",
            )
            repeated = self.prepare(
                root,
                product_code,
                evidence,
                public_root=public_root,
            )
            self.assertEqual(repeated["status"], "ALREADY_PREPARED")
            self.assertEqual(repeated["tafCode"], result["tafCode"])

            public_page.write_bytes(public_page.read_bytes() + b"tamper")
            with self.assertRaisesRegex(
                self.bus.ContractError,
                "bytes finais",
            ):
                self.bus.validate_release_state(
                    root,
                    public_root=public_root,
                )

    def test_post_build_umbrella_preserves_allowlist_and_public_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            root = workspace / "source"
            public_root = workspace / "site"
            product_code, evidence, paths = self.make_umbrella_fixture(root)
            self.set_artifact_profile(
                paths,
                self.bus.POST_BUILD_POST_SANITIZE,
            )
            source_manifest_before = paths["manifest"].read_bytes()
            shutil.copytree(root, public_root)
            public_page = public_root / paths["page"].relative_to(root)
            public_page.write_text(
                public_page.read_text(encoding="utf-8")
                + "<footer data-editorial-attribution>Antigravity</footer>\n",
                encoding="utf-8",
            )
            public_station = public_root / paths["station"].relative_to(root)
            station = json.loads(public_station.read_text(encoding="utf-8"))
            station["totalFiles"] = 1
            write_json(public_station, station)

            inventory = self.bus.release_inventory(
                product_code,
                root,
                public_root=public_root,
            )
            self.bind_evidence_to_inventory(evidence, inventory)
            image_member = next(
                member for member in inventory["members"] if member["kind"] == "image"
            )
            station_member = next(
                member
                for member in inventory["members"]
                if member["path"] == paths["station"].relative_to(root).as_posix()
            )
            self.assertRegex(image_member["catalogCode"], r"^####IMG-")
            self.assertEqual(
                station_member["sha256"],
                hashlib.sha256(public_station.read_bytes()).hexdigest(),
            )
            self.assertNotEqual(
                station_member["sha256"],
                hashlib.sha256(paths["station"].read_bytes()).hexdigest(),
            )
            self.assertEqual(paths["manifest"].read_bytes(), source_manifest_before)

            self.prepare(
                root,
                product_code,
                evidence,
                public_root=public_root,
            )
            self.assertEqual(
                self.bus.validate_release_state(
                    root,
                    public_root=public_root,
                )["preparedReleases"],
                1,
            )

    def test_supersede_release_preserves_history_and_activates_one_public_chain(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            (
                root,
                public_root,
                product_code,
                evidence,
                paths,
                old_release,
                inventory,
            ) = self.make_supersession_fixture(Path(temporary))
            old_tombstones = json.loads(
                paths["tombstones"].read_text(encoding="utf-8")
            )["items"]
            old_reports = json.loads(
                paths["reports"].read_text(encoding="utf-8")
            )["items"]
            old_events = json.loads(paths["ledger"].read_text(encoding="utf-8"))[
                "events"
            ]

            result = self.bus.supersede_release(
                product_code,
                old_release["tafCode"],
                evidence,
                "2026-08-01",
                10,
                reason=self.bus.SUPERSESSION_REASON,
                public_root=public_root,
                root=root,
            )
            self.assertEqual(result["status"], "SUPERSEDED_PREPUBLICATION")
            self.assertEqual(result["publication"], "LOCKED")
            self.assertEqual(
                result["artifactProfile"],
                self.bus.POST_BUILD_POST_SANITIZE,
            )
            self.assertEqual(
                result["artifactRootSha256"],
                inventory["artifactRootSha256"],
            )
            self.assertNotEqual(result["tafCode"], old_release["tafCode"])
            self.assertEqual(
                result["requiredCommand"],
                f"PUBLICAR {result['tafCode']}",
            )

            catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
            product = catalog["items"][0]
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            self.assertEqual(product["tafCode"], result["tafCode"])
            self.assertEqual(manifest["publication"]["finalAcceptanceCode"], result["tafCode"])
            self.assertEqual(product["supersededReleases"], manifest["supersededReleases"])
            self.assertEqual(len(product["supersededReleases"]), 1)
            self.assertEqual(
                product["supersededReleases"][0]["tafCode"],
                old_release["tafCode"],
            )
            self.assertEqual(
                product["supersededReleases"][0]["publication"],
                "VOID_PREPUBLICATION",
            )

            tombstones = json.loads(
                paths["tombstones"].read_text(encoding="utf-8")
            )["items"]
            reports = json.loads(
                paths["reports"].read_text(encoding="utf-8")
            )["items"]
            events = json.loads(paths["ledger"].read_text(encoding="utf-8"))[
                "events"
            ]
            self.assertEqual(tombstones[: len(old_tombstones)], old_tombstones)
            self.assertEqual(reports[: len(old_reports)], old_reports)
            self.assertEqual(events[: len(old_events)], old_events)
            self.assertEqual(len(tombstones), 2)
            self.assertEqual(len(reports), 2)
            self.assertEqual(len(events), 10)
            self.assertTrue(
                any(
                    event["type"] == "RELEASE_SUPERSEDED_PREPUBLICATION"
                    for event in events
                )
            )
            self.assertFalse(
                any("CLINICAL" in event["type"] for event in events[len(old_events):])
            )
            state = self.bus.validate_release_state(
                root,
                public_root=public_root,
            )
            self.assertEqual(state["preparedReleases"], 1)
            self.assertEqual(state["publication"], "LOCKED")
            with self.assertRaisesRegex(self.bus.ContractError, "superseded"):
                self.bus._reject_superseded_taf(old_release["tafCode"], root)
            self.bus._reject_superseded_taf(result["tafCode"], root)

            with self.assertRaisesRegex(self.bus.ContractError, "--public-root"):
                self.bus.validate_release_state(root)
            paths["public_page"].write_bytes(
                paths["public_page"].read_bytes() + b"tamper"
            )
            with self.assertRaisesRegex(self.bus.ContractError, "bytes finais"):
                self.bus.validate_release_state(root, public_root=public_root)

    def test_supersede_release_blocks_wrong_taf_published_and_rolls_back(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            (
                root,
                public_root,
                product_code,
                evidence,
                paths,
                old_release,
                _,
            ) = self.make_supersession_fixture(Path(temporary))
            protected = {
                name: path.read_bytes()
                for name, path in paths.items()
                if name in {
                    "catalog",
                    "ledger",
                    "module",
                    "manifest",
                    "tombstones",
                    "reports",
                }
            }
            with self.assertRaisesRegex(self.bus.ContractError, "cadeia ativa exata"):
                self.bus.supersede_release(
                    product_code,
                    "TAF###-MUX-PROD-20260801-0009-DEADBEEF",
                    evidence,
                    "2026-08-01",
                    10,
                    reason=self.bus.SUPERSESSION_REASON,
                    public_root=public_root,
                    root=root,
                )
            with self.assertRaisesRegex(self.bus.ContractError, "--reason"):
                self.bus.supersede_release(
                    product_code,
                    old_release["tafCode"],
                    evidence,
                    "2026-08-01",
                    10,
                    reason="OUTRA_RAZAO",
                    public_root=public_root,
                    root=root,
                )
            with self.assertRaisesRegex(self.bus.ContractError, "colisão"):
                self.bus.supersede_release(
                    product_code,
                    old_release["tafCode"],
                    evidence,
                    "2026-08-01",
                    9,
                    reason=self.bus.SUPERSESSION_REASON,
                    public_root=public_root,
                    root=root,
                )
            with self.assertRaisesRegex(OSError, "falha transacional injetada"):
                self.bus.supersede_release(
                    product_code,
                    old_release["tafCode"],
                    evidence,
                    "2026-08-01",
                    10,
                    reason=self.bus.SUPERSESSION_REASON,
                    public_root=public_root,
                    root=root,
                    fail_after=3,
                )
            self.assertEqual(
                {
                    name: path.read_bytes()
                    for name, path in paths.items()
                    if name in protected
                },
                protected,
            )
            self.assertEqual(self.bus.validate_release_state(root)["preparedReleases"], 1)

        with tempfile.TemporaryDirectory() as temporary:
            (
                root,
                public_root,
                product_code,
                evidence,
                paths,
                old_release,
                _,
            ) = self.make_supersession_fixture(Path(temporary))
            catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
            catalog["items"][0]["published"] = True
            write_json(paths["catalog"], catalog)
            with self.assertRaises(self.bus.ContractError):
                self.bus.supersede_release(
                    product_code,
                    old_release["tafCode"],
                    evidence,
                    "2026-08-01",
                    10,
                    reason=self.bus.SUPERSESSION_REASON,
                    public_root=public_root,
                    root=root,
                )

    def test_superseded_taf_reuse_and_history_collision_fail_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            (
                root,
                public_root,
                product_code,
                evidence,
                paths,
                old_release,
                _,
            ) = self.make_supersession_fixture(Path(temporary))
            result = self.bus.supersede_release(
                product_code,
                old_release["tafCode"],
                evidence,
                "2026-08-01",
                10,
                reason=self.bus.SUPERSESSION_REASON,
                public_root=public_root,
                root=root,
            )
            catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
            catalog["items"][0]["tafCode"] = old_release["tafCode"]
            write_json(paths["catalog"], catalog)
            with self.assertRaises(self.bus.ContractError):
                self.bus.validate_release_state(root, public_root=public_root)

        with tempfile.TemporaryDirectory() as temporary:
            (
                root,
                public_root,
                product_code,
                evidence,
                paths,
                old_release,
                _,
            ) = self.make_supersession_fixture(Path(temporary))
            self.bus.supersede_release(
                product_code,
                old_release["tafCode"],
                evidence,
                "2026-08-01",
                10,
                reason=self.bus.SUPERSESSION_REASON,
                public_root=public_root,
                root=root,
            )
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            manifest["supersededReleases"].append(
                dict(manifest["supersededReleases"][0])
            )
            write_json(paths["manifest"], manifest)
            catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
            catalog["items"][0]["supersededReleases"] = manifest[
                "supersededReleases"
            ]
            catalog["items"][0]["source"]["sha256"] = hashlib.sha256(
                paths["manifest"].read_bytes()
            ).hexdigest()
            write_json(paths["catalog"], catalog)
            with self.assertRaisesRegex(self.bus.ContractError, "índice"):
                self.bus.validate_release_state(root, public_root=public_root)

    def test_supersede_release_supports_umbrella_public_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            root = workspace / "source"
            public_root = workspace / "site"
            product_code, evidence, paths = self.make_umbrella_fixture(root)
            old_release = self.prepare(root, product_code, evidence)
            shutil.copytree(root, public_root)
            public_page = public_root / paths["page"].relative_to(root)
            public_page.write_text(
                public_page.read_text(encoding="utf-8")
                + "<footer data-editorial-attribution>Antigravity</footer>\n",
                encoding="utf-8",
            )
            public_station = public_root / paths["station"].relative_to(root)
            station = json.loads(public_station.read_text(encoding="utf-8"))
            station["totalFiles"] = 1
            write_json(public_station, station)
            inventory = self.bus.supersession_inventory(
                product_code,
                old_release["tafCode"],
                root=root,
                public_root=public_root,
            )
            self.bind_evidence_to_inventory(evidence, inventory)
            result = self.bus.supersede_release(
                product_code,
                old_release["tafCode"],
                evidence,
                "2026-08-01",
                10,
                reason=self.bus.SUPERSESSION_REASON,
                public_root=public_root,
                root=root,
            )
            self.assertNotEqual(result["tafCode"], old_release["tafCode"])
            self.assertEqual(result["memberCount"], 3)
            module = json.loads(paths["module"].read_text(encoding="utf-8"))
            self.assertEqual(
                module["publication"]["stationTafCode"],
                result["tafCode"],
            )
            self.assertEqual(
                module["publication"]["requiredCommand"],
                f"PUBLICAR {result['tafCode']}",
            )
            self.assertEqual(
                self.bus.validate_release_state(
                    root,
                    public_root=public_root,
                )["publication"],
                "LOCKED",
            )

    def test_umbrella_child_tafs_resolve_superseded_codes_to_active_chains(self) -> None:
        old_a = "TAF###-MUX-PROD-20260801-0001-AAAAAAAA"
        new_a = "TAF###-MUX-PROD-20260801-0004-BBBBBBBB"
        active_b = "TAF###-U3-IMGT-20260801-0005-CCCCCCCC"
        catalog = {
            "items": [
                {
                    "tafCode": new_a,
                    "supersededReleases": [
                        {
                            "tafCode": old_a,
                            "supersededByTafCode": new_a,
                            "publication": "VOID_PREPUBLICATION",
                        }
                    ],
                },
                {"tafCode": active_b, "supersededReleases": []},
            ]
        }
        self.assertEqual(
            self.bus._active_child_taf_codes(catalog, [old_a, active_b]),
            [new_a, active_b],
        )
        with self.assertRaisesRegex(self.bus.ContractError, "única cadeia ativa"):
            self.bus._active_child_taf_codes(catalog, [
                "TAF###-MUX-EXT-20260801-0006-DDDDDDDD"
            ])

    def test_umbrella_can_explicitly_scope_members_to_repository_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, _, paths = self.make_umbrella_fixture(
                root,
                member_root=".",
                include_radar=True,
            )
            inventory = self.bus.release_inventory(product_code, root)
            self.assertEqual(inventory["memberCount"], 4)
            prefixes = {
                member["path"].split("/", 1)[0]
                for member in inventory["members"]
            }
            self.assertEqual(
                prefixes,
                {"15_Radar_Cientifico", "23_Cosmos_NEXUS"},
            )

        for invalid_root in ("./", "23_Cosmos_NEXUS/.."):
            with self.subTest(invalid_root=invalid_root), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                product_code, _, paths = self.make_umbrella_fixture(root)
                manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
                manifest["memberRoot"] = invalid_root
                write_json(paths["manifest"], manifest)
                self.update_umbrella_source_hash(paths)
                with self.assertRaisesRegex(self.bus.ContractError, "memberRoot"):
                    self.bus.release_inventory(product_code, root)

    def test_umbrella_rejects_incoherent_image_code_and_file_code(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, _, paths = self.make_umbrella_fixture(root)
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            image = next(item for item in manifest["members"] if item["kind"] == "image")
            image["catalogCode"] = "####IMG-20260801-0099-DEADBEEF"
            write_json(paths["manifest"], manifest)
            self.update_umbrella_source_hash(paths)
            with self.assertRaisesRegex(self.bus.ContractError, "####IMG"):
                self.bus.release_inventory(product_code, root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, _, paths = self.make_umbrella_fixture(root)
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            file_member = next(item for item in manifest["members"] if item["kind"] == "file")
            file_member["catalogCode"] = "####IMG-20260801-0098-DEADBEEF"
            write_json(paths["manifest"], manifest)
            self.update_umbrella_source_hash(paths)
            with self.assertRaisesRegex(self.bus.ContractError, "campos ou kind"):
                self.bus.release_inventory(product_code, root)

    def test_umbrella_rejects_stale_bundle_and_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, _, paths = self.make_umbrella_fixture(root)
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            manifest["bundle"]["totalBytes"] += 1
            write_json(paths["manifest"], manifest)
            self.update_umbrella_source_hash(paths)
            with self.assertRaisesRegex(self.bus.ContractError, "bundle"):
                self.bus.release_inventory(product_code, root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, _, paths = self.make_umbrella_fixture(root)
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            manifest["audit"]["auditEvidenceSha256"] = "0" * 64
            write_json(paths["manifest"], manifest)
            self.update_umbrella_source_hash(paths)
            with self.assertRaisesRegex(self.bus.ContractError, "AUD###"):
                self.bus.release_inventory(product_code, root)

    def test_umbrella_rejects_escape_symlink_and_mutable_governance_member(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, _, paths = self.make_umbrella_fixture(root)
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            manifest["members"][0]["path"] = "outside.png"
            write_json(paths["manifest"], manifest)
            self.update_umbrella_source_hash(paths)
            with self.assertRaisesRegex(self.bus.ContractError, "fora de memberRoot"):
                self.bus.release_inventory(product_code, root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, _, paths = self.make_umbrella_fixture(root)
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            link = root / "23_Cosmos_NEXUS/assets/atlas/link.png"
            link.symlink_to(paths["umbrella_image"])
            digest = hashlib.sha256(paths["umbrella_image"].read_bytes()).hexdigest()
            member = {
                "path": link.relative_to(root).as_posix(),
                "kind": "image",
                "sha256": digest,
                "bytes": paths["umbrella_image"].stat().st_size,
                "catalogCode": f"####IMG-20260801-0098-{digest[:8].upper()}",
            }
            manifest["members"].append(member)
            manifest["members"].sort(key=lambda item: item["path"])
            with self.assertRaisesRegex(self.bus.ContractError, "symlink"):
                self.bus._release_artifact_inventory(root, paths["manifest"], manifest)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, _, paths = self.make_umbrella_fixture(root)
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            catalog_path = paths["catalog"]
            manifest["members"].append(
                {
                    "path": catalog_path.relative_to(root).as_posix(),
                    "kind": "file",
                    "sha256": hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
                    "bytes": catalog_path.stat().st_size,
                }
            )
            manifest["members"].sort(key=lambda item: item["path"])
            with self.assertRaisesRegex(self.bus.ContractError, "governança mutável"):
                self.bus._release_artifact_inventory(root, paths["manifest"], manifest)

    def test_two_products_are_superseded_sequentially_with_public_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            root = workspace / "source"
            public_root = workspace / "site"
            product_a, evidence_a, paths = self.make_fixture(root)

            product_b = "####AGX-U3-IMGT-20260801-0010-BBBBBBBB"
            product_b_dir = root / "23_Cosmos_NEXUS/products/produto-fixture-b"
            shutil.copytree(paths["manifest"].parent, product_b_dir)
            manifest_b_path = product_b_dir / "product.manifest.json"
            manifest_b = json.loads(manifest_b_path.read_text(encoding="utf-8"))
            manifest_b["identity"].update(
                {
                    "id": "produto-fixture-b",
                    "semanticKey": "produto-fixture-b",
                    "title": "Produto fixture B",
                    "productCode": product_b,
                    "productUid": "b" * 64,
                }
            )
            audit_input = "|".join(
                [
                    product_b,
                    manifest_b["bundle"]["aggregateSha256"],
                    "patient:passed",
                    "rights:passed",
                    "science:passed",
                    "technical:passed",
                    "links:passed",
                ]
            )
            audit_hash = hashlib.sha256(audit_input.encode("utf-8")).hexdigest()
            audit_b = f"AUD###-IMGT-20260801-0010-{audit_hash[:8].upper()}"
            manifest_b["identity"]["auditCode"] = audit_b
            manifest_b["audit"]["auditEvidenceSha256"] = audit_hash
            write_json(manifest_b_path, manifest_b)
            _, artifact_root_b = self.bus._release_artifact_inventory(
                root,
                manifest_b_path,
                manifest_b,
            )

            catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
            item_b = json.loads(json.dumps(catalog["items"][0]))
            item_b.update(
                {
                    "productCode": product_b,
                    "productUid": "b" * 64,
                    "title": "Produto fixture B",
                    "semanticKey": "produto-fixture-b",
                    "universe": "U3",
                    "block": "IMGT",
                    "graphNode": "produto-fixture-b",
                    "auditCode": audit_b,
                }
            )
            item_b["source"] = {
                "path": manifest_b_path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(manifest_b_path.read_bytes()).hexdigest(),
            }
            catalog["items"].append(item_b)
            write_json(paths["catalog"], catalog)

            module = json.loads(paths["module"].read_text(encoding="utf-8"))
            module["candidateProducts"].append(
                {
                    "id": "produto-fixture-b",
                    "productCode": product_b,
                    "status": "candidate-public",
                    "officialPublication": False,
                }
            )
            write_json(paths["module"], module)

            evidence_b_payload = json.loads(evidence_a.read_text(encoding="utf-8"))
            evidence_b_payload["productCode"] = product_b
            evidence_b_payload["auditBinding"] = {
                "auditCode": audit_b,
                "artifactRootSha256": artifact_root_b,
                "status": "PASS",
            }
            evidence_b = root / "evidence-b.json"
            write_json(evidence_b, evidence_b_payload)

            old_a = self.bus.prepare_release(
                product_a,
                evidence_a,
                "2026-08-01",
                9,
                root=root,
            )
            old_b = self.bus.prepare_release(
                product_b,
                evidence_b,
                "2026-08-01",
                10,
                root=root,
            )
            shutil.copytree(root, public_root)
            for manifest_path in (paths["manifest"], manifest_b_path):
                public_product = public_root / manifest_path.parent.relative_to(root)
                public_page = public_product / "index.html"
                public_page.write_text(
                    public_page.read_text(encoding="utf-8")
                    + "<footer data-editorial-attribution>Antigravity</footer>\n",
                    encoding="utf-8",
                )
                references_path = public_product / "references.json"
                references = json.loads(references_path.read_text(encoding="utf-8"))
                references["totalFiles"] = len(references["items"])
                write_json(references_path, references)

            inventory_a = self.bus.supersession_inventory(
                product_a,
                old_a["tafCode"],
                root=root,
                public_root=public_root,
            )
            self.bind_evidence_to_inventory(evidence_a, inventory_a)
            self.bus.supersede_release(
                product_a,
                old_a["tafCode"],
                evidence_a,
                "2026-08-01",
                11,
                reason=self.bus.SUPERSESSION_REASON,
                root=root,
                public_root=public_root,
            )

            inventory_b = self.bus.supersession_inventory(
                product_b,
                old_b["tafCode"],
                root=root,
                public_root=public_root,
            )
            self.bind_evidence_to_inventory(evidence_b, inventory_b)
            self.bus.supersede_release(
                product_b,
                old_b["tafCode"],
                evidence_b,
                "2026-08-01",
                12,
                reason=self.bus.SUPERSESSION_REASON,
                root=root,
                public_root=public_root,
            )
            state = self.bus.validate_release_state(
                root,
                public_root=public_root,
            )
            self.assertEqual(state["preparedReleases"], 2)
            self.assertEqual(state["ledgerEvents"], 20)
            self.assertEqual(state["publication"], "LOCKED")

    def test_repeated_identical_preparation_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, evidence, _ = self.make_fixture(root)
            first = self.prepare(root, product_code, evidence)
            second = self.prepare(root, product_code, evidence)
            self.assertEqual(second["status"], "ALREADY_PREPARED")
            self.assertTrue(second["idempotent"])
            self.assertEqual(second["tafCode"], first["tafCode"])
            self.assertEqual(self.bus.validate_release_state(root)["ledgerEvents"], 5)

    def test_transaction_rolls_back_every_public_json_on_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, evidence, paths = self.make_fixture(root)
            before = {name: path.read_bytes() for name, path in paths.items() if name != "asset"}

            with self.assertRaisesRegex(OSError, "falha transacional injetada"):
                self.prepare(root, product_code, evidence, fail_after=3)

            after = {name: path.read_bytes() for name, path in paths.items() if name != "asset"}
            self.assertEqual(after, before)
            self.assertFalse((root / "23_Cosmos_NEXUS/data/tombstone-manifest.json").exists())
            self.assertFalse(
                (root / "23_Cosmos_NEXUS/data/homologation-reports.json").exists()
            )

    def test_tampering_breaks_tombstone_and_append_only_chain(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, evidence, paths = self.make_fixture(root)
            self.prepare(root, product_code, evidence)
            paths["asset"].write_bytes(paths["asset"].read_bytes() + b"tamper")
            with self.assertRaises(self.bus.ContractError):
                self.bus.validate_release_state(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, evidence, paths = self.make_fixture(root)
            self.prepare(root, product_code, evidence)
            ledger = json.loads(paths["ledger"].read_text(encoding="utf-8"))
            ledger["events"][0]["result"] = "EDITED"
            write_json(paths["ledger"], ledger)
            with self.assertRaisesRegex(self.bus.ContractError, "hash do evento"):
                self.bus.validate_release_state(root)

    def test_fail_closed_for_incomplete_human_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, evidence, paths = self.make_fixture(root)
            payload = json.loads(evidence.read_text(encoding="utf-8"))
            payload["confirmations"]["safariIPhone"] = "PENDING"
            write_json(evidence, payload)
            with self.assertRaisesRegex(self.bus.ContractError, "homologação não aprovada"):
                self.prepare(root, product_code, evidence)
            self.assertIsNone(
                json.loads(paths["catalog"].read_text(encoding="utf-8"))["items"][0]["tafCode"]
            )

    def test_blocks_transient_html_and_stale_audit_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, _, paths = self.make_fixture(root)
            page = paths["manifest"].parent / "index.html"
            page.write_text("<!doctype html><p>Sem TAF; estado candidato.</p>\n", encoding="utf-8")
            with self.assertRaisesRegex(self.bus.ContractError, "estado editorial transitório"):
                self.bus.release_inventory(product_code, root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, _, paths = self.make_fixture(root)
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            manifest["audit"]["auditEvidenceSha256"] = "0" * 64
            write_json(paths["manifest"], manifest)
            catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
            catalog["items"][0]["source"]["sha256"] = hashlib.sha256(
                paths["manifest"].read_bytes()
            ).hexdigest()
            write_json(paths["catalog"], catalog)
            with self.assertRaisesRegex(self.bus.ContractError, "auditEvidenceSha256"):
                self.bus.release_inventory(product_code, root)

    def test_module_manifest_hash_is_reconciled_when_cataloged(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            product_code, evidence, paths = self.make_fixture(root)
            module_hash = hashlib.sha256(paths["module"].read_bytes()).hexdigest()
            catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
            catalog["items"].append(
                {
                    "productCode": "####AGX-MUX-EXT-20260801-0001-CCCCCCCC",
                    "source": {
                        "path": paths["module"].relative_to(root).as_posix(),
                        "sha256": module_hash,
                    },
                    "tafCode": None,
                }
            )
            write_json(paths["catalog"], catalog)
            self.prepare(root, product_code, evidence)
            catalog = json.loads(paths["catalog"].read_text(encoding="utf-8"))
            nexus = catalog["items"][1]
            self.assertEqual(
                nexus["source"]["sha256"],
                hashlib.sha256(paths["module"].read_bytes()).hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
