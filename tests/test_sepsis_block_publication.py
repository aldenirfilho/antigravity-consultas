import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "01_Modulos_Clinicos" / "Infectologia_Critica"


class SepsisBlockPublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((MODULE / "module.manifest.json").read_text(encoding="utf-8"))
        cls.html = (MODULE / "index.html").read_text(encoding="utf-8")
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_manifest_records_only_the_published_sepsis_scope(self):
        self.assertEqual(self.manifest["status"], "em-revisao-medica")
        self.assertTrue(self.manifest["publication"]["clinicalReviewOngoing"])
        blocks = {
            block["id"]: block
            for block in self.manifest["publication"]["publishedBlocks"]
        }
        self.assertEqual(set(blocks), {"sepse"})
        sepse = blocks["sepse"]
        self.assertEqual(sepse["status"], "publicado")
        self.assertEqual(sepse["publishedAt"], "2026-08-04")
        self.assertEqual(sepse["entryAnchor"], "#sepse-publicada")
        self.assertEqual(
            set(sepse["includes"]),
            {
                "reconhecimento e primeira hora do choque séptico",
                "fluxo de sepse e controle do foco",
                "mimetizadores inflamatórios",
                "qSOFA contextual",
            },
        )
        source_urls = {source["url"] for source in sepse["sources"]}
        self.assertIn("https://doi.org/10.1007/s00134-026-08361-1", source_urls)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/26903338/", source_urls)
        self.assertIn("https://doi.org/10.1007/s00134-026-08410-9", source_urls)

    def test_public_page_explains_utility_use_and_result(self):
        for marker in (
            'id="sepse-publicada"',
            "Bloco de sepse publicado · 04/08/2026",
            "Demais temas · revisão médica em andamento",
            "1 · Reconhecer",
            "2 · Agir",
            "3 · Conferir limites",
            "Resultado entregue:",
            'href="#emergencias"',
            'href="#fluxos"',
            'href="#ferramentas"',
            "Surviving Sepsis Campaign 2026",
            "Correção editorial da SSC 2026",
        ):
            self.assertIn(marker, self.html)

    def test_home_route_remains_stable(self):
        stable_route = 'href="01_Modulos_Clinicos/Infectologia_Critica/index.html"'
        hash_route = 'href="01_Modulos_Clinicos/Infectologia_Critica/index.html#sepse-publicada"'
        self.assertIn(stable_route, self.home)
        self.assertNotIn(hash_route, self.home)


if __name__ == "__main__":
    unittest.main()
