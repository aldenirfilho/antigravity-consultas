from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SyncGuideTests(unittest.TestCase):
    def test_sync_guide_has_web_route_and_safety_rules(self):
        markdown = (ROOT / "docs_usuario/SINCRONIZACAO_MACS_WEB.md").read_text(
            encoding="utf-8"
        )
        reader = (
            ROOT / "docs_usuario/SINCRONIZACAO_MACS_WEB/index.html"
        ).read_text(encoding="utf-8")

        self.assertIn("GitHub, branch `main`", markdown)
        self.assertIn("Não mantenha o repositório Git ativo dentro do iCloud Drive", markdown)
        self.assertIn("Não use iCloud e Obsidian Sync ao mesmo tempo", markdown)
        self.assertIn("aldenirfilho/antigravity-consultas", markdown)
        self.assertIn('data-source="../SINCRONIZACAO_MACS_WEB.md"', reader)

    def test_safe_sync_script_refuses_dirty_worktree_and_forced_merges(self):
        script = (
            ROOT / "scripts_admin/sincronizar_git_seguro.sh"
        ).read_text(encoding="utf-8")

        self.assertIn("git status --porcelain=v1", script)
        self.assertIn("git fetch --prune origin", script)
        self.assertIn("git pull --ff-only origin main", script)
        self.assertNotIn("reset --hard", script)
        self.assertNotIn("push --force", script)

    def test_guides_index_links_sync_reader(self):
        guides = (ROOT / "docs_usuario/index.html").read_text(encoding="utf-8")
        self.assertIn('href="./SINCRONIZACAO_MACS_WEB/"', guides)

    def test_readme_links_sync_reader(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "[🔄 Sincronizar Mac Air, Mac Pro e web com segurança]",
            readme,
        )

    def test_sync_reader_is_cached_and_required_by_deploy(self):
        worker = (ROOT / "sw.js").read_text(encoding="utf-8")
        workflow = (
            ROOT / ".github/workflows/deploy-seguro.yml"
        ).read_text(encoding="utf-8")

        for relative in (
            "docs_usuario/SINCRONIZACAO_MACS_WEB.md",
            "docs_usuario/SINCRONIZACAO_MACS_WEB/index.html",
        ):
            self.assertIn(f'./{relative}', worker)
            self.assertIn(f"site/{relative}", workflow)


if __name__ == "__main__":
    unittest.main()
