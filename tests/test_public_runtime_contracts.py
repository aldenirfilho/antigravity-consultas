#!/usr/bin/env python3
"""Contratos focados do artefato público, Mapa Vivo e service worker raiz."""

from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts_admin" / "build_public_site.py"
HOME = ROOT / "index.html"
WORKER = ROOT / "sw.js"
CONNECTIONS = ROOT / "data" / "connections.json"
TOPICS = ROOT / "data" / "topics.json"
NEXUS_COSMOS = ROOT / "23_Cosmos_NEXUS" / "data" / "cosmos.json"


class AnchorCollector(HTMLParser):
    """Coleta destinos HTML sem depender de um navegador ou de regex frágil."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.destinations: set[str] = set()

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"id", "name"} and value:
                self.destinations.add(value)


def assigned_literal(path: Path, name: str):
    module = ast.parse(path.read_text(encoding="utf-8"))
    for statement in module.body:
        if not isinstance(statement, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == name for target in statement.targets):
            return ast.literal_eval(statement.value)
    raise AssertionError(f"Atribuição {name} não encontrada em {path}")


def quoted_const_items(source: str, name: str) -> list[str]:
    match = re.search(
        rf"const\s+{re.escape(name)}\s*=\s*(?:new\s+Set\s*\()?\[(.*?)\]\)?;",
        source,
        flags=re.DOTALL,
    )
    if not match:
        raise AssertionError(f"Array JavaScript {name} não encontrado")
    return re.findall(r'"([^"]+)"', match.group(1))


def map_groups(source: str) -> list[dict]:
    match = re.search(r"const\s+GROUPS\s*=\s*(\[.*?\]);", source, flags=re.DOTALL)
    if not match:
        raise AssertionError("Configuração GROUPS do Mapa Vivo não encontrada")
    return json.loads(match.group(1))


def json_const(source: str, name: str):
    match = re.search(
        rf"const\s+{re.escape(name)}\s*=\s*(\{{.*?\}});",
        source,
        flags=re.DOTALL,
    )
    if not match:
        raise AssertionError(f"Constante JSON {name} não encontrada")
    return json.loads(match.group(1))


def local_html_destination(url: str) -> tuple[Path, str]:
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc:
        raise AssertionError(f"URL externa não é destino local: {url}")
    relative = unquote(parsed.path)
    if not relative or relative == "/":
        relative = "index.html"
    target = ROOT / relative.lstrip("/")
    if target.is_dir() or relative.endswith("/"):
        target /= "index.html"
    return target, unquote(parsed.fragment)


class PublicRuntimeContractsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = BUILDER.read_text(encoding="utf-8")
        cls.home = HOME.read_text(encoding="utf-8")
        cls.worker = WORKER.read_text(encoding="utf-8")
        cls.connections = json.loads(CONNECTIONS.read_text(encoding="utf-8"))
        cls.topics = json.loads(TOPICS.read_text(encoding="utf-8"))
        cls.nexus_cosmos = json.loads(NEXUS_COSMOS.read_text(encoding="utf-8"))

    def test_mnemonics_route_is_required_by_the_public_builder(self) -> None:
        required = set(assigned_literal(BUILDER, "REQUIRED"))
        self.assertIn("mnemonicos", required)
        self.assertIn('href="mnemonicos/"', self.home)
        for relative in (
            "mnemonicos/index.html",
            "mnemonicos/styles.css",
            "mnemonicos/app.js",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)
            self.assertIn(f'"./{relative}"', self.worker)

    def test_connections_builder_is_byte_idempotent_when_graph_is_current(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            sandbox = Path(temporary)
            (sandbox / "scripts_admin").mkdir()
            (sandbox / "data").mkdir()
            shutil.copy2(ROOT / "scripts_admin/build_connections.py", sandbox / "scripts_admin")
            for relative in (
                "data/connections.json",
                "data/desafios.json",
                "data/mnemonicos.json",
            ):
                shutil.copy2(ROOT / relative, sandbox / relative)

            target = sandbox / "data/connections.json"
            first = subprocess.run(
                ["python3", "scripts_admin/build_connections.py"],
                cwd=sandbox,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            after_first = target.read_bytes()
            second = subprocess.run(
                ["python3", "scripts_admin/build_connections.py"],
                cwd=sandbox,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertEqual(target.read_bytes(), after_first)
            self.assertIn("Mapa Vivo já estava atual", second.stdout)

    def test_every_map_node_is_reachable_by_a_filter(self) -> None:
        groups = map_groups(self.home)
        aliases = json_const(self.home, "TYPE_ALIASES")
        group_ids = {group["id"] for group in groups}
        self.assertIn("nexus", group_ids)

        type_to_group: dict[str, str] = {}
        for group in groups:
            for node_type in group.get("types", []):
                self.assertNotIn(node_type, type_to_group, node_type)
                type_to_group[node_type] = group["id"]

        def group_of(node: dict) -> str | None:
            for group in groups:
                if any(node["id"].startswith(prefix) for prefix in group.get("idPrefixes", [])):
                    return group["id"]
            node_type = aliases.get(node.get("type"), node.get("type"))
            return type_to_group.get(node_type)

        resolved = {node["id"]: group_of(node) for node in self.connections["nodes"]}
        unresolved = sorted(node_id for node_id, group_id in resolved.items() if group_id is None)
        self.assertEqual(unresolved, [])

        counts = {group_id: 0 for group_id in group_ids}
        for group_id in resolved.values():
            counts[group_id] += 1
        self.assertTrue(all(count > 0 for count in counts.values()), counts)
        self.assertEqual(
            {resolved[node["id"]] for node in self.connections["nodes"] if node.get("type") == "channel"},
            {"estrutura"},
        )
        for node in self.connections["nodes"]:
            if node["id"].startswith("nexus-") or node.get("type") in {
                "product-release",
            }:
                self.assertEqual(resolved[node["id"]], "nexus", node["id"])

        # Protege a leitura inicial contra o salto de densidade 22 -> 36
        # observado quando todos os blocos NEXUS eram tratados como ferramentas.
        self.assertLessEqual(counts["estrutura"], 26, counts)

    def test_map_urls_and_html_anchors_resolve_to_real_destinations(self) -> None:
        expected_corrections = {
            "neuroimagem-avc": "01_Modulos_Clinicos/AVC_Agudo/avc_31_blocos.html#bloco-18",
            "trombolise-avc": "01_Modulos_Clinicos/AVC_Agudo/codigo_avc_10_minutos_dashboard_html.html#reperfusao",
            "trombectomia-avc": "01_Modulos_Clinicos/AVC_Agudo/codigo_avc_10_minutos_dashboard_html.html#reperfusao",
            "pa-avc": "01_Modulos_Clinicos/AVC_Agudo/codigo_avc_10_minutos_dashboard_html.html#pa",
            "fa-avc": "01_Modulos_Clinicos/AVC_Agudo/avc_31_blocos.html#bloco-12",
            "edema-cerebral-avc": "01_Modulos_Clinicos/AVC_Agudo/avc_31_blocos.html#bloco-13",
            "updown": "01_UpDown_Hub/index.html",
        }
        connection_nodes = {node["id"]: node for node in self.connections["nodes"]}
        topic_nodes = {node["id"]: node for node in self.topics}
        for node_id, url in expected_corrections.items():
            self.assertEqual(connection_nodes[node_id]["url"], url)
            if node_id != "updown":
                self.assertEqual(topic_nodes[node_id]["url"], url)

        anchor_cache: dict[Path, set[str]] = {}
        for collection_name, nodes in (
            ("connections", self.connections["nodes"]),
            ("topics", self.topics),
        ):
            for node in nodes:
                url = node.get("url")
                if url == "#" and node.get("status") == "planejado":
                    continue
                self.assertIsInstance(url, str, f"{collection_name}:{node['id']}")
                self.assertTrue(url, f"{collection_name}:{node['id']}")
                self.assertNotEqual(url, "#", f"{collection_name}:{node['id']}")
                target, fragment = local_html_destination(url)
                self.assertTrue(
                    target.is_file(),
                    f"{collection_name}:{node['id']} aponta para arquivo ausente: {url}",
                )
                if not fragment:
                    continue
                if target not in anchor_cache:
                    parser = AnchorCollector()
                    parser.feed(target.read_text(encoding="utf-8"))
                    anchor_cache[target] = parser.destinations
                self.assertIn(
                    fragment,
                    anchor_cache[target],
                    f"{collection_name}:{node['id']} aponta para âncora ausente: {url}",
                )

    def test_nexus_taxonomy_is_canonical_and_legacy_aliases_remain_compatible(self) -> None:
        expected_global = {
            "nexus-projeto-temi360xinfinit": "source-project",
            "nexus-projeto-biblioteca-visual": "source-project",
            "nexus-lote-temi360xinfinit-biblioteca-visual": "canonical-lot",
            "maquina-turbo-temi-360x": "product-release",
            "biblioteca-visual-cosmica": "product-release",
        }
        expected_local = {
            "source-temi360xinfinit": "source-project",
            "source-biblioteca-visual": "source-project",
            "lot-temi360xinfinit-biblioteca-visual": "canonical-lot",
            "maquina-turbo-temi-360x": "product-release",
            "biblioteca-visual-cosmica": "product-release",
        }
        retired = {"project-source", "collection", "product-candidate"}

        for nodes in (self.connections["nodes"], self.topics):
            by_id = {node["id"]: node for node in nodes}
            self.assertEqual(
                {node_id: by_id[node_id]["type"] for node_id in expected_global},
                expected_global,
            )
            self.assertFalse(retired & {node.get("type") for node in nodes})

        local_by_id = {node["id"]: node for node in self.nexus_cosmos["nodes"]}
        self.assertEqual(
            {node_id: local_by_id[node_id]["kind"] for node_id in expected_local},
            expected_local,
        )
        self.assertFalse(retired & {node.get("kind") for node in self.nexus_cosmos["nodes"]})

        self.assertEqual(
            json_const(self.home, "TYPE_ALIASES"),
            {
                "project-source": "source-project",
                "collection": "canonical-lot",
                "product-candidate": "product-release",
            },
        )

    def test_worker_cache_only_references_public_allowlist_entries(self) -> None:
        required = set(assigned_literal(BUILDER, "REQUIRED"))
        optional = set(assigned_literal(BUILDER, "OPTIONAL"))
        allowed_roots = required | optional
        cached = quoted_const_items(self.worker, "SHELL_ASSETS") + quoted_const_items(
            self.worker, "WARM_ASSETS"
        )

        missing: list[str] = []
        excluded: list[str] = []
        for asset in cached:
            relative = asset.removeprefix("./") or "index.html"
            if not (ROOT / relative).is_file():
                missing.append(relative)
            top_level = relative.split("/", 1)[0]
            if relative not in allowed_roots and top_level not in allowed_roots:
                excluded.append(relative)
        self.assertEqual(missing, [])
        self.assertEqual(excluded, [])

    def test_worker_warm_cache_stays_within_mobile_budget(self) -> None:
        warm = quoted_const_items(self.worker, "WARM_ASSETS")
        total_bytes = sum((ROOT / asset.removeprefix("./")).stat().st_size for asset in warm)
        self.assertLessEqual(total_bytes, 8 * 1024 * 1024, total_bytes)

        nexus_images = [
            asset
            for asset in warm
            if asset.startswith("./23_Cosmos_NEXUS/")
            and Path(asset).suffix.casefold() in {".jpg", ".jpeg", ".png", ".webp"}
        ]
        self.assertEqual(
            nexus_images,
            ["./23_Cosmos_NEXUS/assets/atlas/01-maquina-turbo-temi-360x.jpg"],
        )
        self.assertFalse(any("/products/" in asset and "/assets/" in asset for asset in warm))

    def test_worker_executes_network_freshness_policy_for_mutable_data(self) -> None:
        script = r"""
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(process.argv[1], 'utf8');
const listeners = new Map();
const context = {
  URL,
  console,
  self: {
    registration: { scope: 'https://example.test/antigravity-consultas/' },
    addEventListener: (name, listener) => listeners.set(name, listener),
    skipWaiting: async () => {},
    clients: { claim: async () => {} },
    location: { origin: 'https://example.test' }
  }
};
vm.createContext(context);
vm.runInContext(source, context);
const isMutable = vm.runInContext('isMutableDataPath', context);
const yes = [
  '/antigravity-consultas/15_Radar_Cientifico/data/radar.js',
  '/antigravity-consultas/15_Radar_Cientifico/data/radar-widget-feed.json',
  '/antigravity-consultas/23_Cosmos_NEXUS/data/product-catalog.json',
  '/antigravity-consultas/23_Cosmos_NEXUS/products/demo/product.manifest.json',
  '/antigravity-consultas/data/connections.json',
  '/antigravity-consultas/data/site_manifest.json'
];
const no = [
  '/antigravity-consultas/23_Cosmos_NEXUS/assets/styles.css',
  '/antigravity-consultas/23_Cosmos_NEXUS/assets/atlas/02-entrada-multifonte.jpg',
  '/antigravity-consultas/23_Cosmos_NEXUS/products/demo/assets/image.png'
];
if (!yes.every(isMutable) || no.some(isMutable)) process.exit(1);
"""
        result = subprocess.run(
            ["node", "-e", script, str(WORKER)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            'request.cache === "no-store" || isMutableDataPath(url.pathname)',
            self.worker,
        )


if __name__ == "__main__":
    unittest.main()
