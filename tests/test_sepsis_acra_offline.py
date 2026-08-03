#!/usr/bin/env python3
"""Paridade, segurança e modos da camada ACRA offline de Sepse Ultra Expert."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "01_Modulos_Clinicos" / "Sepse_Choque_Septico"
BUILDER = ROOT / "scripts_admin" / "build_sepsis_acra_bundle.py"
BUNDLE = MODULE / "data" / "acra-bundle.js"
RUNTIME = MODULE / "assets" / "acra-runtime.js"
CONTROLLER = MODULE / "assets" / "acra-controller.js"
SMOKE = ROOT / "tests" / "sepsis_acra_offline_smoke.js"


def node_binary() -> str | None:
    executable = shutil.which("node")
    if executable:
        return executable
    bundled = Path(
        "/Users/aldenirpro/.cache/codex-runtimes/"
        "codex-primary-runtime/dependencies/node/bin/node"
    )
    return str(bundled) if bundled.is_file() else None


def load_bundle() -> dict:
    script = (
        f"require({json.dumps(str(BUNDLE))});"
        "process.stdout.write(JSON.stringify(global.SEPSE_ACRA_BUNDLE));"
    )
    result = subprocess.run(
        [node_binary(), "-e", script],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return json.loads(result.stdout)


@unittest.skipUnless(node_binary(), "Node.js indisponível para validar o ACRA offline")
class SepsisAcraOfflineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = load_bundle()
        cls.runtime = RUNTIME.read_text(encoding="utf-8")
        cls.controller = CONTROLLER.read_text(encoding="utf-8")

    def test_bundle_has_exactly_ten_canonical_artifacts_in_byte_parity(self) -> None:
        paths = sorted((MODULE / "acra").glob("*.json"))
        entries = self.bundle["entries"]
        self.assertEqual(len(paths), 10)
        self.assertEqual(self.bundle["artifactCount"], 10)
        self.assertEqual(len(entries), 10)
        self.assertEqual(self.bundle["artifactSchemaVersion"], "1.0")
        self.assertEqual(
            self.bundle["schemaVersion"],
            "antigravity-sepsis-acra-bundle-v1",
        )

        canonical_artifacts = []
        for path, entry in zip(paths, entries, strict=True):
            with self.subTest(path=path.name):
                raw = path.read_bytes()
                artifact = json.loads(raw.decode("utf-8"))
                self.assertEqual(entry["source"], f"acra/{path.name}")
                self.assertEqual(entry["sha256"], hashlib.sha256(raw).hexdigest())
                self.assertEqual(entry["artifact"], artifact)
                canonical_artifacts.append(artifact)

        canonical = json.dumps(
            canonical_artifacts,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        self.assertEqual(
            self.bundle["contentSha256"],
            hashlib.sha256(canonical).hexdigest(),
        )
        self.assertEqual(
            len({entry["artifact"]["id"] for entry in entries}),
            10,
        )

    def test_builder_check_is_deterministic_and_read_only(self) -> None:
        before = hashlib.sha256(BUNDLE.read_bytes()).hexdigest()
        for _ in range(2):
            result = subprocess.run(
                ["python3", str(BUILDER), "--check"],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("10/10", result.stdout)
        self.assertEqual(hashlib.sha256(BUNDLE.read_bytes()).hexdigest(), before)

    def test_runtime_and_controller_are_csp_safe_and_have_no_network_port(self) -> None:
        source = self.runtime + "\n" + self.controller
        for forbidden in (
            "XMLHttpRequest",
            "WebSocket",
            "EventSource",
            "sendBeacon",
            "innerHTML",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)
        self.assertNotRegex(source, r"\bfetch\s*\(")
        self.assertNotRegex(source, r"\beval\s*\(")
        self.assertNotRegex(source, r"\bnew\s+Function\s*\(")
        self.assertNotRegex(source, r"\bimport\s*\(")
        self.assertIn("textContent", self.runtime)
        self.assertIn('parsed.protocol !== "https:"', self.runtime)
        self.assertIn("requiresPreview !== true", self.runtime)
        self.assertIn("connect-src 'none'", (MODULE / "index.html").read_text(encoding="utf-8"))

    def test_controller_contract_is_explicit_and_storage_is_id_only(self) -> None:
        for marker in (
            '"OFF", "PARCIAL", "AUTO"',
            '"PARCIAL"',
            "userInitiated !== true",
            "IntersectionObserver",
            "observer.disconnect",
            "unmountAll",
            "clearProgress",
            "answeredIds",
            "checkedIds",
            "visitedIds",
            "conteúdo convencional",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.controller)
        self.assertNotRegex(
            self.controller,
            r"localStorage\.(?:setItem|getItem)\([^)]*(?:patient|shock|infection|dose)",
        )

    def test_javascript_syntax_and_functional_security_smoke(self) -> None:
        for path in (BUNDLE, RUNTIME, CONTROLLER, SMOKE):
            with self.subTest(path=path.name):
                subprocess.run(
                    [node_binary(), "--check", str(path)],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
        result = subprocess.run(
            [node_binary(), str(SMOKE)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "PASS sepsis-acra-offline-smoke\n")


if __name__ == "__main__":
    unittest.main()
