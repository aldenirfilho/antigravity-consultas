#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "01_Modulos_Clinicos" / "Sepse_Choque"


class SepseChoque2026Tests(unittest.TestCase):
    def test_module_is_self_contained_and_safely_linked(self) -> None:
        html = (MODULE / "index.html").read_text(encoding="utf-8")
        self.assertIn("Surviving Sepsis Campaign 2026", html)
        self.assertIn("até 3 h", html)
        self.assertIn("Noradrenalina é primeira linha", html)
        self.assertIn("controle precoce", html)
        self.assertIn("De-resuscitation", html)
        self.assertIn("connect-src 'none'", html)
        self.assertNotRegex(html, r"\b(?:prontu[aá]rio|paciente)\s*[:#]\s*[A-Z0-9.-]{4,}")
        self.assertEqual(html.count('<script>'), 1)

    def test_manifest_declares_sources_privacy_and_publication(self) -> None:
        manifest = json.loads((MODULE / "module.manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "ativo-educacional")
        self.assertEqual(manifest["publication"]["mode"], "public-educational")
        self.assertFalse(manifest["privacy"]["networkRuntime"])
        self.assertFalse(manifest["privacy"]["patientData"])
        self.assertGreaterEqual(len(manifest["sources"]), 4)
        for source in manifest["sources"]:
            self.assertTrue(source["url"].startswith("https://"))

    def test_home_and_catalogs_expose_canonical_route(self) -> None:
        route = "01_Modulos_Clinicos/Sepse_Choque/index.html"
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        site = json.loads((ROOT / "data/site_manifest.json").read_text(encoding="utf-8"))
        topics = json.loads((ROOT / "data/topics.json").read_text(encoding="utf-8"))
        navigation = json.loads((ROOT / "data/navigation.json").read_text(encoding="utf-8"))
        updown = json.loads((ROOT / "01_UpDown_Hub/registry.json").read_text(encoding="utf-8"))
        self.assertIn(f'href="{route}"', home)
        self.assertEqual(site["canonicalRoutes"]["sepse_choque_2026"], route)
        self.assertTrue(any(item.get("path") == route for item in site["modules"]))
        self.assertTrue(any(item.get("url") == route for item in topics))
        self.assertTrue(any(item.get("url") == route for item in navigation["main"]))
        self.assertTrue(any(item.get("id") == "updown-010-sepse-choque-2026" for item in updown["documents"]))

    def test_content_keeps_core_2026_decision_nuance(self) -> None:
        html = (MODULE / "index.html").read_text(encoding="utf-8")
        required = [
            "provável/definida",
            "apenas possível",
            "30 mL/kg",
            "medida dinâmica",
            "vasopressina",
            "infusão prolongada",
            "Vitamina C IV",
            "pós-sepse",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, html)


if __name__ == "__main__":
    unittest.main()
