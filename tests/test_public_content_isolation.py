#!/usr/bin/env python3
"""Regressões do isolamento preventivo no artefato público."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {
    "01_UpDown_Hub/content/reumatologia/les-manifestacoes/metadata.json",
    "05_Midia_E_Feed/data/recovery_manifest.json",
}


def load_builder():
    path = ROOT / "scripts_admin/build_public_site.py"
    spec = importlib.util.spec_from_file_location("content_isolation_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Não foi possível carregar o builder público.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicContentIsolationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = load_builder()

    def test_builder_excludes_exactly_two_non_homologated_files(self) -> None:
        self.assertEqual(set(self.builder.PUBLIC_BUILD_EXCLUSIONS), EXCLUDED)

    def test_copy_preserves_sources_and_adjacent_public_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            site = root / "site"
            fixtures = {
                "01_UpDown_Hub/content/reumatologia/les-manifestacoes/metadata.json":
                    '{"state":"review"}',
                "01_UpDown_Hub/content/reumatologia/les-manifestacoes/reader/metadata.json":
                    '{"state":"public"}',
                "05_Midia_E_Feed/data/recovery_manifest.json":
                    '{"internal":"inventory"}',
                "05_Midia_E_Feed/data/public.json":
                    '{"files":[]}',
            }
            for relative, payload in fixtures.items():
                source = root / relative
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text(payload, encoding="utf-8")

            for top_level in ("01_UpDown_Hub", "05_Midia_E_Feed"):
                self.builder.copy_entry(root, site, top_level, set(), set())

            for relative in EXCLUDED:
                self.assertTrue((root / relative).is_file())
                self.assertFalse((site / relative).exists())
            for relative in {
                "01_UpDown_Hub/content/reumatologia/les-manifestacoes/reader/metadata.json",
                "05_Midia_E_Feed/data/public.json",
            }:
                self.assertEqual(
                    (site / relative).read_bytes(),
                    (root / relative).read_bytes(),
                )

    def test_deploy_smoke_asserts_both_exclusions(self) -> None:
        workflow = (ROOT / ".github/workflows/deploy-seguro.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "python3 scripts_admin/editorial_gate.py --check --public-root site --json",
            workflow,
        )
        for relative in EXCLUDED:
            self.assertIn(f"test ! -e site/{relative}", workflow)

    def test_service_worker_revokes_the_previous_public_cache(self) -> None:
        worker = (ROOT / "sw.js").read_text(encoding="utf-8")
        self.assertIn('const CACHE_NAME = `${CACHE_PREFIX}v13`', worker)
        self.assertNotIn('const CACHE_NAME = `${CACHE_PREFIX}v12`', worker)
        self.assertIn(
            "key.startsWith(CACHE_PREFIX) && key !== CACHE_NAME",
            worker,
        )
        self.assertIn(".map((key) => caches.delete(key))", worker)

    def test_internal_sources_are_absent_but_adjacent_public_files_remain(self) -> None:
        for relative in EXCLUDED:
            self.assertFalse((ROOT / relative).exists())
        self.assertTrue(
            (
                ROOT
                / "01_UpDown_Hub/content/reumatologia/les-manifestacoes/reader/metadata.json"
            ).is_file()
        )
        self.assertTrue((ROOT / "05_Midia_E_Feed/data/public.json").is_file())

    def test_public_footers_have_neutral_attribution_and_review_warning(self) -> None:
        forbidden = (
            "Desenvolvido por Dr.",
            "CRM-CE 16587",
            "RQE Clínica Médica 11846",
            "Mestre Ciências da Saúde",
            "Plantonista UTI/Enfermaria",
            "Hospital Regional Norte",
            "Santa Casa de Sobral",
        )
        for relative in (
            "13_RenalDose_Antimicrobianos/index.html",
            "14_SAPS3_Calculator/index.html",
        ):
            source = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(
                "Idealização e edição da plataforma: Aldenir Rocha de Oliveira Filho.",
                source,
            )
            self.assertIn("Conteúdo educacional em revisão.", source)
            for claim in forbidden:
                self.assertNotIn(claim, source)

    def test_registry_has_one_unique_protective_release(self) -> None:
        registry = json.loads(
            (ROOT / "data/editorial/registry.json").read_text(encoding="utf-8")
        )
        releases = [
            item
            for item in registry["items"]
            if item["id"] == "release-isolamento-conteudo-nao-homologado-2026-07-25"
        ]
        self.assertEqual(len(releases), 1)
        self.assertEqual(
            set(releases[0]["paths"]),
            {
                "13_RenalDose_Antimicrobianos/index.html",
                "14_SAPS3_Calculator/index.html",
            },
        )
        registered = [
            path
            for item in registry["items"]
            for path in item["paths"]
        ]
        self.assertEqual(len(registered), len(set(registered)))


if __name__ == "__main__":
    unittest.main()
