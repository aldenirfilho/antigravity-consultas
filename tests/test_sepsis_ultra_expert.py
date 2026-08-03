#!/usr/bin/env python3
"""Contratos clínicos, visuais e do primeiro bloco público de sepse."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "01_Modulos_Clinicos/Sepse_Choque_Septico"
NODE = Path(
    "/Users/aldenirpro/.cache/codex-runtimes/"
    "codex-primary-runtime/dependencies/node/bin/node"
)


def load_catalog() -> dict:
    script = (
        "global.window={};"
        f"require({json.dumps(str(MODULE / 'data/catalog.js'))});"
        "process.stdout.write(JSON.stringify(window.SEPSE_ULTRA_EXPERT));"
    )
    result = subprocess.run(
        [str(NODE), "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


class SepsisUltraExpertPublicPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = (MODULE / "index.html").read_text(encoding="utf-8")
        cls.app = (MODULE / "assets/app.js").read_text(encoding="utf-8")
        cls.styles = (MODULE / "assets/styles.css").read_text(encoding="utf-8")
        cls.visual_runtime = (MODULE / "assets/visual-runtime.js").read_text(
            encoding="utf-8"
        )
        cls.acra_runtime = (MODULE / "assets/acra-runtime.js").read_text(
            encoding="utf-8"
        )
        cls.acra_controller = (MODULE / "assets/acra-controller.js").read_text(
            encoding="utf-8"
        )
        cls.catalog_source = (MODULE / "data/catalog.js").read_text(
            encoding="utf-8"
        )
        cls.catalog = load_catalog()
        cls.manifest = json.loads(
            (MODULE / "module.manifest.json").read_text(encoding="utf-8")
        )
        cls.visual_plan = json.loads(
            (MODULE / "data/visual-plan.json").read_text(encoding="utf-8")
        )
        cls.acra_plan = json.loads(
            (MODULE / "data/acra-plan.json").read_text(encoding="utf-8")
        )
        cls.visual_assets = json.loads(
            (MODULE / "data/visual-assets.json").read_text(encoding="utf-8")
        )

    def test_required_local_files_exist_and_are_nontrivial(self) -> None:
        minimum_sizes = {
            "index.html": 20_000,
            "assets/app.js": 15_000,
            "assets/styles.css": 12_000,
            "assets/theme-bootstrap.js": 500,
            "data/catalog.js": 25_000,
            "data/visual-plan.json": 10_000,
            "data/visual-assets.json": 20_000,
            "data/acra-plan.json": 4_000,
            "data/acra-bundle.js": 100_000,
            "assets/visual-runtime.js": 1_000,
            "assets/acra-runtime.js": 20_000,
            "assets/acra-controller.js": 5_000,
            "module.manifest.json": 2_000,
        }
        for relative, minimum in minimum_sizes.items():
            with self.subTest(relative=relative):
                self.assertGreaterEqual((MODULE / relative).stat().st_size, minimum)

    def test_manifest_authorizes_only_the_original_public_preview(self) -> None:
        self.assertEqual(self.manifest["status"], "em-revisao-medica")
        publication = self.manifest["publication"]
        self.assertEqual(publication["mode"], "public-preview")
        self.assertTrue(publication["publicPreview"])
        self.assertTrue(publication["clinicalReviewOngoing"])
        self.assertTrue(publication["ownerPublicationAuthorization"])
        self.assertEqual(
            publication["authorizedScope"],
            "primeiro-bloco-funcional-sepse-ultra-expert-b127-b152",
        )
        self.assertEqual(publication["blockedBlocks"][:2], ["B153", "B154"])
        self.assertIn(
            "especificações SUE2-A de disfunção orgânica e POCUS séptico",
            publication["excludedFromThisPublication"],
        )
        self.assertEqual(self.manifest["contentInventory"]["generatedImages"], 60)
        self.assertEqual(self.manifest["contentInventory"]["createdAcra"], 10)
        self.assertEqual(self.manifest["contentInventory"]["integratedImages"], 60)
        self.assertEqual(self.manifest["contentInventory"]["integratedAcra"], 10)
        self.assertEqual(
            self.manifest["reviewGate"]["phase4"],
            "public-preview-authorized-continuous-clinical-review",
        )

    def test_visual_plan_has_exactly_60_separate_widescreen_slots(self) -> None:
        items = self.visual_plan["items"]
        self.assertEqual(len(items), 60)
        self.assertEqual(self.visual_plan["generated"], 60)
        self.assertEqual(self.visual_plan["status"], "integrated-local-candidate")
        self.assertEqual(self.visual_plan["target"]["aspectRatio"], "16:9")
        self.assertEqual(self.visual_plan["target"]["masterSize"], "1672x941")
        self.assertEqual(len({item["id"] for item in items}), 60)
        self.assertEqual(len({item["file"] for item in items}), 60)
        for item in items:
            self.assertRegex(item["id"], r"^IMG-\d{2}$")
            self.assertTrue(item["file"].endswith(".png"))
            self.assertTrue(item["sourceIds"])

    def test_acra_plan_has_exactly_10_created_artifacts(self) -> None:
        items = self.acra_plan["items"]
        self.assertEqual(len(items), 10)
        self.assertEqual(self.acra_plan["created"], 10)
        self.assertEqual(self.acra_plan["status"], "integrated-local-candidate")
        self.assertEqual(
            self.acra_plan["policy"]["phase"],
            "fase-4a-local-b127-b152-autorizada",
        )
        self.assertEqual(len({item["id"] for item in items}), 10)
        self.assertEqual(len({item["file"] for item in items}), 10)
        self.assertTrue(
            all(item["status"] == "integrated-local-candidate" for item in items)
        )
        for item in items:
            with self.subTest(item=item["id"]):
                self.assertRegex(item["file"], r"^acra/acra-sepse-\d{2}-.+\.json$")
                self.assertTrue((MODULE / item["file"]).is_file())

    def test_phase_three_contains_exactly_10_safe_portable_acra(self) -> None:
        acra_dir = MODULE / "acra"
        artifacts = sorted(acra_dir.glob("*.json"))
        self.assertEqual(len(artifacts), 10)

        required_root = {
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
        allowed_components = {
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
        allowed_actions = {
            "continueResearch",
            "deepen",
            "compare",
            "verify",
            "quiz",
            "review",
        }
        catalog_urls = {item["url"] for item in self.catalog["references"]}
        runtime_source = self.index + self.app + self.styles

        for path in artifacts:
            with self.subTest(path=path.name):
                artifact = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(required_root.issubset(artifact))
                self.assertNotIn("metadata", artifact)
                self.assertEqual(artifact["version"], "1.0")
                self.assertEqual(artifact["mode"], "tutorial")
                self.assertGreaterEqual(len(artifact["critical"]), 3)
                self.assertNotIn(path.name, runtime_source)

                components = artifact["components"]
                component_ids = {item["id"] for item in components}
                self.assertEqual(len(component_ids), len(components))
                self.assertFalse(
                    {item["type"] for item in components} - allowed_components
                )
                for layer in ("M0", "M1", "M2", "M3", "M4", "M5", "M6"):
                    self.assertTrue(
                        any(item.get("title", "").startswith(layer) for item in components),
                        f"{path.name} não contém a camada {layer}",
                    )

                quizzes = [item for item in components if item["type"] == "quiz"]
                self.assertEqual(len(quizzes), 1)
                self.assertEqual(len(quizzes[0]["questions"]), 3)
                spaced = [
                    item
                    for item in components
                    if item["type"] == "checklist"
                    and item.get("title", "").startswith("M6")
                ]
                self.assertEqual(len(spaced), 1)
                self.assertGreaterEqual(len(spaced[0]["items"]), 5)

                source_components = [
                    item for item in components if item["type"] == "sources"
                ]
                followup_components = [
                    item for item in components if item["type"] == "followupActions"
                ]
                self.assertEqual(len(source_components), 1)
                self.assertEqual(len(followup_components), 1)

                sources = artifact["sources"]
                source_ids = {item["id"] for item in sources}
                self.assertEqual(len(source_ids), len(sources))
                self.assertEqual(set(source_components[0]["sourceIds"]), source_ids)
                for source in sources:
                    self.assertTrue(source["url"].startswith("https://"))
                    self.assertIn(source["url"], catalog_urls)

                actions = artifact["actions"]
                action_ids = {item["id"] for item in actions}
                self.assertEqual(len(action_ids), len(actions))
                self.assertEqual(
                    set(followup_components[0]["actionIds"]),
                    action_ids,
                )
                for action in actions:
                    self.assertIn(action["kind"], allowed_actions)
                    self.assertIs(action["requiresPreview"], True)
                    self.assertFalse(
                        set(action.get("contextComponentIds", [])) - component_ids
                    )

                collected_ids: list[str] = []

                def collect_ids(value: object) -> None:
                    if isinstance(value, dict):
                        if isinstance(value.get("id"), str):
                            collected_ids.append(value["id"])
                        for nested in value.values():
                            collect_ids(nested)
                    elif isinstance(value, list):
                        for nested in value:
                            collect_ids(nested)

                collect_ids(artifact)
                self.assertEqual(len(collected_ids), len(set(collected_ids)))

                safety_text = json.dumps(artifact, ensure_ascii=False).casefold()
                self.assertIn("sintétic", safety_text)
                self.assertIn("educacional", safety_text)
                self.assertTrue(
                    any(
                        marker in safety_text
                        for marker in (
                            "não substitui",
                            "não é protocolo",
                            "não constitui protocolo",
                            "não é prescrição",
                            "não prescreve",
                            "não indica procedimento",
                        )
                    )
                )

    def test_catalog_counts_and_quiz_invariants(self) -> None:
        self.assertEqual(len(self.catalog["timeline"]), 7)
        self.assertEqual(len(self.catalog["phenotypes"]["hemodynamic"]), 5)
        self.assertEqual(len(self.catalog["phenotypes"]["seneca"]), 4)
        self.assertEqual(len(self.catalog["phenotypes"]["molecular"]), 3)
        self.assertEqual(len(self.catalog["organSupport"]), 8)
        self.assertEqual(len(self.catalog["frontier"]), 10)
        self.assertEqual(len(self.catalog["cases"]), 4)
        self.assertEqual(len(self.catalog["questions"]), 8)
        self.assertGreaterEqual(len(self.catalog["references"]), 19)
        for collection in (self.catalog["cases"], self.catalog["questions"]):
            for item in collection:
                self.assertEqual(len(item["options"]), 4)
                self.assertEqual(len(item["feedback"]), len(item["options"]))
                self.assertIn(item["correct"], range(len(item["options"])))

    def test_every_granular_source_id_resolves_to_an_https_reference(self) -> None:
        references = {item["id"]: item for item in self.catalog["references"]}
        self.assertEqual(len(references), len(self.catalog["references"]))
        self.assertTrue(all(item["url"].startswith("https://") for item in references.values()))

        sourced_items = list(self.catalog["timeline"])
        sourced_items += self.catalog["organSupport"]
        sourced_items += self.catalog["frontier"]
        sourced_items += self.catalog["cases"]
        sourced_items += self.catalog["questions"]
        for profiles in self.catalog["phenotypes"].values():
            sourced_items += profiles
        sourced_items += self.visual_plan["items"]
        sourced_items += self.acra_plan["items"]

        for item in sourced_items:
            with self.subTest(item=item.get("id", item.get("title"))):
                self.assertTrue(item.get("sourceIds"))
                self.assertFalse(set(item["sourceIds"]) - set(references))

    def test_html_has_offline_csp_and_no_remote_runtime(self) -> None:
        self.assertIn("connect-src 'none'", self.index)
        self.assertIn("form-action 'none'", self.index)
        self.assertNotRegex(self.index, r'<script[^>]+src="https?://')
        self.assertNotRegex(self.index, r'<link[^>]+href="https?://')
        self.assertNotRegex(self.index, r'<img[^>]+src="https?://')
        runtime_source = "\n".join(
            (
                self.app,
                self.visual_runtime,
                self.acra_runtime,
                self.acra_controller,
            )
        )
        for forbidden in ("fetch(", "XMLHttpRequest", "WebSocket", "sendBeacon"):
            self.assertNotIn(forbidden, runtime_source)

    def test_storage_is_limited_to_visual_and_synthetic_learning_state(self) -> None:
        self.assertIn("antigravity:a11y:v1", self.index)
        self.assertNotIn("storagePrefix", self.app)
        self.assertIn("antigravity:sepse-acra:mode:v1", self.acra_controller)
        self.assertIn("antigravity:sepse-acra:progress:v1", self.acra_controller)
        for sensitive in (
            "earlyWard",
            "earlyTreatment",
            "lateIcu",
            "infection",
            "shock",
            "refractoryForm",
        ):
            self.assertNotRegex(
                self.app + self.acra_controller,
                rf"storage\.(?:set|get)\([^\n]*{re.escape(sensitive)}",
            )

    def test_static_ids_are_unique_and_fragment_links_resolve(self) -> None:
        ids = re.findall(r'(?<![\w-])id="([^"]+)"', self.index)
        self.assertEqual(len(ids), len(set(ids)))
        fragments = set(re.findall(r'href="#([^"]+)"', self.index))
        self.assertFalse(fragments - set(ids))

    def test_accessibility_contracts_are_present(self) -> None:
        self.assertIn('id="deathCounter" aria-live="off"', self.index)
        self.assertIn('scope="col"', self.index)
        self.assertIn('scope="row"', self.index)
        self.assertIn("prefers-reduced-motion", self.styles)
        self.assertIn("@media print", self.styles)
        self.assertIn('role="tab"', self.index)
        self.assertIn("bindRovingTabs", self.app)
        for key in ("ArrowRight", "ArrowLeft", "Home", "End"):
            self.assertIn(key, self.app)
        self.assertIn("noopener noreferrer", self.app)
        self.assertIn("noscript-warning", self.index)
        self.assertIn('id="visualDialog"', self.index)
        self.assertIn('id="acraStage"', self.index)
        self.assertIn("stageReturnFocus", self.acra_controller)
        self.assertIn("closeStage(true)", self.acra_controller)
        self.assertIn("closeControl.focus()", self.acra_controller)
        self.assertIn("@media (max-width: 360px)", self.styles)

    def test_core_clinical_guardrails_are_explicit(self) -> None:
        combined = self.index + self.catalog_source
        markers = (
            "idealmente ≤1 h",
            "até 3 h",
            "≥30 mL/kg",
            "Não é autorização para bolus repetidos cegamente",
            "Noradrenalina primeiro",
            "Adicionar vasopressina",
            "Adicionar adrenalina",
            "idealmente em até 6 h",
            "não constituem classificação validada nem protocolo oficial",
            "EVIDÊNCIA INSUFICIENTE",
            "SUGERE CONTRA",
            "revisão humana",
            "não é contagem observada em tempo real",
        )
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertIn(marker.casefold(), combined.casefold())

    def test_module_is_registered_in_central_public_navigation(self) -> None:
        public_path = "01_Modulos_Clinicos/Sepse_Choque_Septico"
        central_files = (
            ROOT / "index.html",
            ROOT / "data/site_manifest.json",
            ROOT / "data/navigation.json",
            ROOT / "data/topics.json",
            ROOT / "data/connections.json",
            ROOT / "06_Infra_Site_E_Assets/data/home-manifest.json",
        )
        for path in central_files:
            with self.subTest(path=path.name):
                self.assertIn(public_path, path.read_text(encoding="utf-8"))

        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("🦠 Sepse <sup", home)
        self.assertIn("60 visuais expandidos", home)
        self.assertIn("10 ACRA opcionais", home)

    def test_phase_four_integrates_exactly_60_visuals_with_optimized_derivatives(self) -> None:
        image_dir = MODULE / "assets/images"
        expected = {item["file"] for item in self.visual_plan["items"]}
        originals = sorted(image_dir.glob("*.png"))
        reviewed = sorted((image_dir / "reviewed").glob("*.png"))
        optimized = sorted((image_dir / "optimized").glob("*.jpg"))
        self.assertEqual({path.name for path in originals}, expected)
        self.assertEqual(len(originals), 60)
        self.assertEqual(len(reviewed), 2)
        self.assertEqual(len(optimized), 120)
        self.assertEqual(len(self.visual_assets["items"]), 60)
        self.assertEqual(self.index.count('data-visual-id="IMG-'), 60)

        digests = set()
        for path in originals:
            with self.subTest(path=path.name):
                self.assertEqual(path.parent, image_dir)
                header = path.read_bytes()[:24]
                self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
                width, height = struct.unpack(">II", header[16:24])
                self.assertEqual((width, height), (1672, 941))
                digests.add(hashlib.sha256(path.read_bytes()).hexdigest())
                self.assertIn(path.name, self.index)
        self.assertEqual(len(digests), 60)

        for item in self.visual_assets["items"]:
            with self.subTest(item=item["id"]):
                self.assertTrue((MODULE / item["master"]["path"]).is_file())
                self.assertEqual(len(item["derivatives"]), 2)
                self.assertTrue(item["alt"])
                self.assertTrue(item["caption"])
                self.assertTrue(item["longDescription"])
                for derivative in item["derivatives"]:
                    self.assertTrue((MODULE / derivative["path"]).is_file())

    def test_visuals_use_expanded_magazine_mode_with_sources_and_download(self) -> None:
        self.assertIn(".visual-grid--2", self.styles)
        self.assertIn("grid-template-columns: minmax(0, 1fr)", self.styles)
        self.assertIn(".visual-download", self.styles)
        self.assertIn("details.open = true", self.visual_runtime)
        self.assertIn("downloadLink.download", self.visual_runtime)
        self.assertIn("buildSourceLinks", self.visual_runtime)
        self.assertEqual(self.index.count('class="clinical-visual"'), 60)
        self.assertEqual(self.index.count('data-source-ids="'), 60)

    def test_phase_four_integrates_exactly_10_optional_acra_slots(self) -> None:
        self.assertEqual(self.index.count('class="acra-slot"'), 10)
        self.assertEqual(self.index.count("data-acra-open"), 10)
        self.assertIn("PARCIAL é o padrão", self.index)
        self.assertIn('data-acra-mode="auto"', self.index)
        self.assertIn('data-acra-mode="off"', self.index)
        self.assertIn("data/acra-bundle.js", self.index)
        self.assertIn("assets/acra-runtime.js", self.index)
        self.assertIn("assets/acra-controller.js", self.index)


if __name__ == "__main__":
    unittest.main()
