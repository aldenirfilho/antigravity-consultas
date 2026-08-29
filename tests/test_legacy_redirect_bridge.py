import importlib.util
import tempfile
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts_admin" / "build_legacy_redirect_site.py"
SPEC = importlib.util.spec_from_file_location("legacy_redirect_bridge", SCRIPT_PATH)
assert SPEC and SPEC.loader
BRIDGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BRIDGE)


class LegacyRedirectBridgeTests(unittest.TestCase):
    def test_destination_preserves_equivalent_route(self):
        cases = {
            "index.html": "https://aldenirfilho.github.io/aldenirmed89/",
            "404.html": "https://aldenirfilho.github.io/aldenirmed89/",
            "01_Modulos_Clinicos/Pneumologia_Critica/index.html": (
                "https://aldenirfilho.github.io/aldenirmed89/"
                "01_Modulos_Clinicos/Pneumologia_Critica/"
            ),
            "docs/página clínica.html": (
                "https://aldenirfilho.github.io/aldenirmed89/"
                "docs/p%C3%A1gina%20cl%C3%ADnica.html"
            ),
        }
        for relative, expected in cases.items():
            with self.subTest(relative=relative):
                self.assertEqual(
                    BRIDGE.destination_for_html(PurePosixPath(relative)), expected
                )

    def test_build_rewrites_only_public_runtime_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            site = Path(temp_dir) / "site"
            nested = site / "01_Modulos_Clinicos" / "Pneumologia_Critica"
            nested.mkdir(parents=True)
            (site / "index.html").write_text("conteúdo clínico antigo", encoding="utf-8")
            (site / "404.html").write_text("página antiga", encoding="utf-8")
            (nested / "index.html").write_text("DPOC antiga", encoding="utf-8")
            (site / "sw.js").write_text("cache antigo", encoding="utf-8")
            (site / "manifest.webmanifest").write_text("{}", encoding="utf-8")
            (site / ".nojekyll").touch()
            scoped_worker = nested / "sw.js"
            scoped_worker.write_text("cache clínico antigo", encoding="utf-8")
            asset = site / "assets" / "imagem.png"
            asset.parent.mkdir()
            asset.write_bytes(b"imagem-preservada")

            count = BRIDGE.build_bridge(site)

            self.assertEqual(count, 3)
            self.assertEqual(asset.read_bytes(), b"imagem-preservada")
            for html_path in (site / "index.html", site / "404.html", nested / "index.html"):
                rendered = html_path.read_text(encoding="utf-8")
                self.assertIn(BRIDGE.BRIDGE_MARKER, rendered)
                self.assertIn('name="robots" content="noindex,follow"', rendered)
                self.assertIn("window.location.replace(target)", rendered)
                self.assertNotIn("conteúdo clínico antigo", rendered)
                self.assertNotIn("DPOC antiga", rendered)

            nested_html = (nested / "index.html").read_text(encoding="utf-8")
            self.assertIn(
                "https://aldenirfilho.github.io/aldenirmed89/"
                "01_Modulos_Clinicos/Pneumologia_Critica/",
                nested_html,
            )

            for worker_path in (site / "sw.js", scoped_worker):
                worker = worker_path.read_text(encoding="utf-8")
                self.assertIn(BRIDGE.BRIDGE_MARKER, worker)
                self.assertIn("Response.redirect", worker)
                self.assertIn(BRIDGE.NEW_BASE_URL, worker)
                self.assertNotIn("caches.delete", worker)

            manifest = (site / "manifest.webmanifest").read_text(encoding="utf-8")
            self.assertIn('"short_name": "AldenirMed89"', manifest)
            self.assertEqual(BRIDGE.check_bridge(site), (3, 2))

            first_snapshot = {
                path.relative_to(site).as_posix(): path.read_bytes()
                for path in site.rglob("*")
                if path.is_file()
            }
            self.assertEqual(BRIDGE.build_bridge(site), 3)
            second_snapshot = {
                path.relative_to(site).as_posix(): path.read_bytes()
                for path in site.rglob("*")
                if path.is_file()
            }
            self.assertEqual(first_snapshot, second_snapshot)

    def test_refuses_repository_root_without_touching_html(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = Path(temp_dir) / "site"
            repository.mkdir()
            (repository / ".git").mkdir()
            original = repository / "index.html"
            original.write_text("fonte que deve permanecer", encoding="utf-8")
            (repository / "404.html").write_text("404", encoding="utf-8")
            (repository / ".nojekyll").touch()
            (repository / "manifest.webmanifest").write_text("{}", encoding="utf-8")
            (repository / "sw.js").write_text("worker", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "raiz de um repositório Git"):
                BRIDGE.build_bridge(repository)

            self.assertEqual(original.read_text(encoding="utf-8"), "fonte que deve permanecer")

    def test_workflow_applies_bridge_before_final_security_checks(self):
        workflow = (ROOT / ".github" / "workflows" / "deploy-seguro.yml").read_text(
            encoding="utf-8"
        )
        build_position = workflow.index("python3 scripts_admin/build_public_site.py . site")
        bridge_position = workflow.index(
            "python3 scripts_admin/build_legacy_redirect_site.py site"
        )
        public_content_gate_position = workflow.index(
            "python3 scripts_admin/editorial_gate.py --check --public-root site --json"
        )
        bridge_check_position = workflow.index(
            "python3 scripts_admin/build_legacy_redirect_site.py --check site"
        )
        final_guard_position = workflow.index(
            "python3 scripts_admin/publication_guard.py check-site site",
            bridge_position,
        )
        upload_position = workflow.index("name: Upload Pages artifact")
        self.assertLess(build_position, bridge_position)
        self.assertLess(public_content_gate_position, bridge_position)
        self.assertLess(bridge_position, bridge_check_position)
        self.assertLess(bridge_check_position, final_guard_position)
        self.assertLess(final_guard_position, upload_position)


if __name__ == "__main__":
    unittest.main()
