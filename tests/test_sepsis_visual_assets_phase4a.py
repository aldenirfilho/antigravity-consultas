#!/usr/bin/env python3
"""Contratos do pipeline visual local da Fase 4A de Sepse Ultra Expert."""

from __future__ import annotations

import hashlib
import json
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "01_Modulos_Clinicos/Sepse_Choque_Septico"
IMAGE_DIR = MODULE / "assets/images"
OPTIMIZED_DIR = IMAGE_DIR / "optimized"
VISUAL_PLAN_PATH = MODULE / "data/visual-plan.json"
VISUAL_ASSETS_PATH = MODULE / "data/visual-assets.json"
REVISED_IDS = {"IMG-08", "IMG-18"}
NEW_MAGAZINE_IDS = {f"IMG-{number:02d}" for number in range(41, 61)}
REVIEW_PENDING_IDS = ["IMG-08", "IMG-18", *sorted(NEW_MAGAZINE_IDS)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"PNG inválido: {path}")
    return struct.unpack(">II", header[16:24])


def jpeg_dimensions(path: Path) -> tuple[int, int]:
    payload = path.read_bytes()
    if payload[:2] != b"\xff\xd8":
        raise AssertionError(f"JPEG inválido: {path}")

    start_of_frame = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
    }
    offset = 2
    while offset + 8 < len(payload):
        if payload[offset] != 0xFF:
            offset += 1
            continue
        while offset < len(payload) and payload[offset] == 0xFF:
            offset += 1
        marker = payload[offset]
        offset += 1
        if marker == 0xD8 or marker == 0x01 or 0xD0 <= marker <= 0xD7:
            continue
        if marker in {0xD9, 0xDA}:
            break
        segment_length = struct.unpack(">H", payload[offset : offset + 2])[0]
        if marker in start_of_frame:
            height = struct.unpack(">H", payload[offset + 3 : offset + 5])[0]
            width = struct.unpack(">H", payload[offset + 5 : offset + 7])[0]
            return width, height
        offset += segment_length

    raise AssertionError(f"Dimensões JPEG não encontradas: {path}")


class SepsisVisualAssetsPhase4ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.visual_plan = json.loads(VISUAL_PLAN_PATH.read_text(encoding="utf-8"))
        cls.visual_assets_source = VISUAL_ASSETS_PATH.read_text(encoding="utf-8")
        cls.visual_assets = json.loads(cls.visual_assets_source)

    def test_manifest_is_deterministic_and_complete(self) -> None:
        assets = self.visual_assets
        self.assertEqual(assets["schemaVersion"], "antigravity-visual-assets-v1")
        self.assertEqual(assets["moduleId"], "sepse-ultra-expert")
        self.assertEqual(assets["derivedFrom"], "data/visual-plan.json")
        self.assertEqual(assets["status"], "integrated-local-owner-review-pending")
        self.assertEqual(self.visual_plan["status"], "integrated-local-candidate")
        self.assertEqual(assets["generator"]["tool"], "sips")
        self.assertEqual(assets["generator"]["version"], "316")
        self.assertEqual(assets["generator"]["format"], "jpeg")
        self.assertEqual(assets["generator"]["quality"], 88)
        self.assertEqual(assets["generator"]["widths"], [960, 1672])
        self.assertIs(assets["generator"]["mastersPreserved"], True)
        self.assertEqual(
            assets["inventory"],
            {
                "originalMastersPreserved": 60,
                "integrationMasters": 60,
                "reviewedMasters": 2,
                "derivatives": 120,
                "generatedRevisions": 2,
                "reviewPending": 22,
            },
        )
        self.assertEqual(len(assets["items"]), 60)
        self.assertEqual(
            self.visual_assets_source,
            json.dumps(assets, ensure_ascii=False, indent=2) + "\n",
        )

    def test_manifest_preserves_visual_plan_order_and_semantics(self) -> None:
        plan_items = self.visual_plan["items"]
        asset_items = self.visual_assets["items"]
        self.assertEqual(
            [item["id"] for item in asset_items],
            [item["id"] for item in plan_items],
        )

        for plan, asset in zip(plan_items, asset_items, strict=True):
            with self.subTest(item=plan["id"]):
                self.assertEqual(asset["anchor"], plan["anchor"])
                self.assertEqual(asset["title"], plan["title"])
                self.assertEqual(asset["role"], plan["role"])
                self.assertEqual(asset["sourceIds"], plan["sourceIds"])
                normalized_title = plan["title"].rstrip(".")
                brief = plan["brief"]
                self.assertEqual(
                    asset["alt"],
                    f"{normalized_title}. {brief}",
                )
                self.assertEqual(
                    asset["caption"],
                    f"{plan['title']} — {brief}",
                )
                self.assertIn(plan["id"], asset["longDescription"])
                self.assertIn(plan["role"], asset["longDescription"])
                self.assertIn(brief, asset["longDescription"])
                self.assertGreater(len(asset["alt"]), 40)
                self.assertGreater(len(asset["caption"]), 40)
                self.assertGreater(len(asset["longDescription"]), 100)

    def test_original_and_reviewed_png_masters_are_preserved_and_hashed(self) -> None:
        original_masters = sorted(IMAGE_DIR.glob("*.png"))
        reviewed_masters = sorted((IMAGE_DIR / "reviewed").glob("*.png"))
        self.assertEqual(len(original_masters), 60)
        self.assertEqual(len(reviewed_masters), 2)
        self.assertEqual(
            {path.name for path in original_masters},
            {item["file"] for item in self.visual_plan["items"]},
        )
        self.assertEqual(
            {path.name for path in reviewed_masters},
            {
                "img-08-relogio-completo.png",
                "img-18-noradrenalina-periferica.png",
            },
        )

        original_set_lines: list[str] = []
        integration_set_lines: list[str] = []
        for item in self.visual_assets["items"]:
            master = item["master"]
            path = MODULE / master["path"]
            original = item.get("originalMaster", master)
            original_path = MODULE / original["path"]
            with self.subTest(item=item["id"]):
                expected_parent = IMAGE_DIR / "reviewed" if item["id"] in REVISED_IDS else IMAGE_DIR
                self.assertEqual(path.parent, expected_parent)
                self.assertEqual(original_path.parent, IMAGE_DIR)
                self.assertEqual(master["format"], "png")
                self.assertEqual(png_dimensions(path), (1672, 941))
                self.assertEqual((master["width"], master["height"]), (1672, 941))
                self.assertEqual(master["bytes"], path.stat().st_size)
                self.assertEqual(master["sha256"], sha256(path))
                self.assertEqual(original["bytes"], original_path.stat().st_size)
                self.assertEqual(original["sha256"], sha256(original_path))
                original_set_lines.append(f"{item['id']}:{original['sha256']}")
                integration_set_lines.append(
                    f"{item['id']}:{master['path']}:{master['sha256']}"
                )

        original_set_hash = hashlib.sha256(
            ("\n".join(original_set_lines) + "\n").encode("utf-8")
        ).hexdigest()
        integration_set_hash = hashlib.sha256(
            ("\n".join(integration_set_lines) + "\n").encode("utf-8")
        ).hexdigest()
        self.assertEqual(
            original_set_hash,
            self.visual_assets["integrity"]["originalMasterSetSha256"],
        )
        self.assertEqual(
            integration_set_hash,
            self.visual_assets["integrity"]["integrationMasterSetSha256"],
        )
        self.assertEqual(
            original_set_hash,
            "8d580d5d00d4cbe52860eda7e0a5c3c5657b9319e05db61bb98c8c1e71b3f8a4",
        )

    def test_exactly_120_optimized_jpegs_match_recorded_integrity(self) -> None:
        actual = sorted(OPTIMIZED_DIR.glob("*.jpg"))
        self.assertEqual(len(actual), 120)
        self.assertFalse([path for path in OPTIMIZED_DIR.iterdir() if path.suffix != ".jpg"])

        expected_paths: set[Path] = set()
        set_lines: list[str] = []
        master_bytes = 0
        derivative_bytes = 0
        bytes_960 = 0
        bytes_1672 = 0

        for item in self.visual_assets["items"]:
            master_bytes += item["master"]["bytes"]
            stem = Path(item["master"]["path"]).stem
            derivatives = item["derivatives"]
            self.assertEqual(len(derivatives), 2)
            self.assertEqual(
                [Path(entry["path"]).name for entry in derivatives],
                [f"{stem}-960.jpg", f"{stem}-1672.jpg"],
            )
            self.assertEqual(
                [(entry["width"], entry["height"]) for entry in derivatives],
                [(960, 540), (1672, 941)],
            )

            for derivative in derivatives:
                path = MODULE / derivative["path"]
                expected_paths.add(path)
                derivative_bytes += derivative["bytes"]
                if derivative["width"] == 960:
                    bytes_960 += derivative["bytes"]
                else:
                    bytes_1672 += derivative["bytes"]
                with self.subTest(item=item["id"], path=path.name):
                    self.assertEqual(path.parent, OPTIMIZED_DIR)
                    self.assertEqual(derivative["format"], "jpeg")
                    self.assertEqual(
                        jpeg_dimensions(path),
                        (derivative["width"], derivative["height"]),
                    )
                    self.assertEqual(derivative["bytes"], path.stat().st_size)
                    self.assertEqual(derivative["sha256"], sha256(path))
                set_lines.append(
                    f"{item['id']}:{derivative['path']}:{derivative['sha256']}"
                )

        self.assertEqual(set(actual), expected_paths)
        self.assertLess(derivative_bytes, master_bytes)
        self.assertLess(bytes_960, bytes_1672)
        derivative_set_hash = hashlib.sha256(
            ("\n".join(set_lines) + "\n").encode("utf-8")
        ).hexdigest()
        self.assertEqual(
            derivative_set_hash,
            self.visual_assets["integrity"]["derivativeSetSha256"],
        )

    def test_img_08_and_img_18_use_generated_revisions_pending_owner_review(self) -> None:
        revised = {
            item["id"]: item
            for item in self.visual_assets["items"]
            if item.get("generatedRevision")
        }
        self.assertEqual(set(revised), REVISED_IDS)
        self.assertEqual(
            self.visual_assets["review"]["pendingIds"],
            REVIEW_PENDING_IDS,
        )
        self.assertIs(self.visual_assets["review"]["clinicalBlocker"], False)
        for identifier, item in revised.items():
            with self.subTest(item=identifier):
                self.assertIs(item["reviewPending"], True)
                self.assertNotIn("clinicalReviewRequired", item)
                self.assertEqual(
                    item["revisionSource"],
                    item["master"]["path"],
                )
                self.assertEqual(
                    Path(item["master"]["path"]).parent,
                    Path("assets/images/reviewed"),
                )
                self.assertEqual(
                    Path(item["originalMaster"]["path"]).parent,
                    Path("assets/images"),
                )
                self.assertNotEqual(
                    item["master"]["sha256"],
                    item["originalMaster"]["sha256"],
                )
        self.assertFalse(
            [
                item
                for item in self.visual_assets["items"]
                if item.get("clinicalReviewRequired")
            ]
        )
        for item in self.visual_assets["items"]:
            if item["id"] in NEW_MAGAZINE_IDS:
                with self.subTest(item=item["id"]):
                    self.assertIs(item["reviewPending"], True)

    def test_catalog_contains_only_local_portable_asset_paths(self) -> None:
        self.assertNotIn("http://", self.visual_assets_source)
        self.assertNotIn("https://", self.visual_assets_source)

        for item in self.visual_assets["items"]:
            records = [item["master"], *item["derivatives"]]
            if "originalMaster" in item:
                records.append(item["originalMaster"])
            for record in records:
                portable_path = Path(record["path"])
                with self.subTest(item=item["id"], path=record["path"]):
                    self.assertFalse(portable_path.is_absolute())
                    self.assertNotIn("..", portable_path.parts)
                    self.assertNotIn("\\", record["path"])
                    self.assertEqual(portable_path.parts[:2], ("assets", "images"))


if __name__ == "__main__":
    unittest.main()
