#!/usr/bin/env python3
"""Converte o artefato público antigo em uma ponte para o AldenirMed89.

O repositório e os arquivos-fonte permanecem intactos. A transformação acontece
somente depois que ``build_public_site.py`` monta a pasta temporária publicada
pelo GitHub Pages. Cada HTML aponta para a rota equivalente no endereço novo e
o service worker antigo deixa de servir páginas clínicas em cache.
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import quote


OLD_PATH_PREFIX = "/antigravity-consultas"
NEW_BASE_URL = "https://aldenirfilho.github.io/aldenirmed89/"
BRIDGE_MARKER = "aldenirmed89-legacy-bridge:v1"


def destination_for_html(relative: PurePosixPath) -> str:
    """Retorna a rota nova equivalente para o fallback sem JavaScript."""

    path = relative.as_posix()
    if path in {"index.html", "404.html"}:
        suffix = ""
    elif path.endswith("/index.html"):
        suffix = path[: -len("index.html")]
    else:
        suffix = path
    return NEW_BASE_URL + quote(suffix, safe="/:-._~")


def bridge_html(destination: str) -> str:
    escaped_destination = html_lib.escape(destination, quote=True)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,follow">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta http-equiv="refresh" content="0;url={escaped_destination}">
  <link rel="canonical" href="{escaped_destination}">
  <title>AldenirMed89 — novo endereço</title>
  <style>
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
    * {{ box-sizing: border-box; }}
    body {{
      min-height: 100vh; margin: 0; display: grid; place-items: center; padding: 24px;
      color: #eef8ff;
      background:
        radial-gradient(circle at 25% 18%, rgba(111, 77, 255, .28), transparent 32rem),
        radial-gradient(circle at 78% 82%, rgba(0, 219, 255, .18), transparent 28rem),
        #050713;
    }}
    main {{
      width: min(680px, 100%); padding: clamp(28px, 6vw, 56px); text-align: center;
      border: 1px solid rgba(137, 226, 255, .35); border-radius: 28px;
      background: rgba(10, 15, 37, .88); box-shadow: 0 24px 80px rgba(0, 0, 0, .45);
    }}
    .orbit {{ font-size: 2.4rem; color: #8eeaff; }}
    .eyebrow {{ color: #c8adff; font-weight: 800; letter-spacing: .15em; text-transform: uppercase; }}
    h1 {{ margin: .35em 0; font-size: clamp(2rem, 8vw, 4rem); }}
    p {{ color: #c7d7e7; line-height: 1.65; }}
    a {{
      display: inline-block; margin-top: 12px; padding: 14px 20px; border-radius: 999px;
      color: #06101b; background: #8eeaff; font-weight: 850; text-decoration: none;
    }}
    a:focus-visible {{ outline: 3px solid #d6b8ff; outline-offset: 5px; }}
  </style>
  <!-- {BRIDGE_MARKER} -->
  <script>
    (function () {{
      "use strict";
      var oldPrefix = {json.dumps(OLD_PATH_PREFIX)};
      var newBase = {json.dumps(NEW_BASE_URL)};
      var path = window.location.pathname;
      var suffix = "";
      if (path.indexOf(oldPrefix + "/") === 0) {{
        suffix = path.slice(oldPrefix.length + 1);
      }} else if (path !== oldPrefix && path !== oldPrefix + "/") {{
        suffix = path.replace(/^[/]+/, "");
      }}
      var target = newBase + suffix + window.location.search + window.location.hash;
      window.location.replace(target);
    }}());
  </script>
</head>
<body>
  <main aria-labelledby="bridge-title">
    <div class="orbit" aria-hidden="true">✦ ◌ ✦</div>
    <p class="eyebrow">Ponte de navegação orbital</p>
    <h1 id="bridge-title">AldenirMed89</h1>
    <p>O portal mudou de endereço. Você será levado automaticamente à página correspondente.</p>
    <a href="{escaped_destination}">Continuar para o AldenirMed89</a>
  </main>
</body>
</html>
"""


def retirement_service_worker() -> str:
    """Evita que instalações antigas continuem exibindo páginas em cache."""

    return f'''"use strict";

// {BRIDGE_MARKER}

const OLD_PATH_PREFIX = {json.dumps(OLD_PATH_PREFIX)};
const NEW_BASE_URL = {json.dumps(NEW_BASE_URL)};

function bridgeDestination(url) {{
  let suffix = "";
  if (url.pathname.startsWith(`${{OLD_PATH_PREFIX}}/`)) {{
    suffix = url.pathname.slice(OLD_PATH_PREFIX.length + 1);
  }}
  return `${{NEW_BASE_URL}}${{suffix}}${{url.search}}`;
}}

self.addEventListener("install", (event) => {{
  event.waitUntil(self.skipWaiting());
}});

self.addEventListener("activate", (event) => {{
  event.waitUntil(self.clients.claim());
}});

self.addEventListener("fetch", (event) => {{
  const request = event.request;
  if (request.method !== "GET" || request.mode !== "navigate") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  event.respondWith(Response.redirect(bridgeDestination(url), 302));
}});
'''


def bridge_manifest() -> str:
    payload = {
        "name": "AldenirMed89 — endereço atualizado",
        "short_name": "AldenirMed89",
        "description": "Ponte segura para o novo endereço do portal AldenirMed89.",
        "lang": "pt-BR",
        "start_url": "./",
        "scope": "./",
        "display": "standalone",
        "background_color": "#050713",
        "theme_color": "#0a0f25",
        "icons": [
            {
                "src": "assets/icons/antigravity-consultas-192.png",
                "sizes": "192x192",
                "type": "image/png",
            },
            {
                "src": "assets/icons/antigravity-consultas-512.png",
                "sizes": "512x512",
                "type": "image/png",
            },
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def validate_site_target(site: Path) -> tuple[list[Path], list[Path]]:
    """Falha antes de qualquer escrita se o alvo puder ser o repositório-fonte."""

    unresolved = site
    site = site.resolve()
    if unresolved.is_symlink():
        raise ValueError(f"Artefato público não pode ser link simbólico: {unresolved}")
    if not site.is_dir() or site == Path(site.anchor) or site.name != "site":
        raise ValueError(f"Artefato público inseguro ou inexistente: {site}")
    if (site / ".git").exists():
        raise ValueError("A ponte nunca pode ser aplicada à raiz de um repositório Git.")

    required = ("index.html", "404.html", ".nojekyll", "manifest.webmanifest", "sw.js")
    missing = [relative for relative in required if not (site / relative).is_file()]
    if missing:
        raise ValueError(
            "Artefato público incompleto; ausente(s): " + ", ".join(missing)
        )

    html_paths = sorted(site.rglob("*.html"))
    worker_paths = sorted(site.rglob("sw.js"))
    if not html_paths:
        raise ValueError("Nenhuma página HTML encontrada no artefato público.")
    unsafe = [path for path in (*html_paths, *worker_paths) if path.is_symlink()]
    if unsafe:
        raise ValueError(f"Link simbólico não permitido: {unsafe[0]}")
    return html_paths, worker_paths


def build_bridge(site: Path) -> int:
    html_paths, worker_paths = validate_site_target(site)
    site = site.resolve()

    for html_path in html_paths:
        relative = PurePosixPath(html_path.relative_to(site).as_posix())
        destination = destination_for_html(relative)
        html_path.write_text(bridge_html(destination), encoding="utf-8")

    worker_source = retirement_service_worker()
    for worker_path in worker_paths:
        worker_path.write_text(worker_source, encoding="utf-8")
    (site / "manifest.webmanifest").write_text(bridge_manifest(), encoding="utf-8")

    # O sitemap antigo é mantido para que buscadores reencontrem os endereços
    # históricos e processem o encaminhamento/canonical de cada rota.
    print(
        f"✅ Ponte AldenirMed89 aplicada a {len(html_paths)} página(s) HTML; "
        f"{len(worker_paths)} service worker(s) aposentado(s); fontes originais preservadas."
    )
    return len(html_paths)


def check_bridge(site: Path) -> tuple[int, int]:
    html_paths, worker_paths = validate_site_target(site)
    site = site.resolve()
    for html_path in html_paths:
        relative = PurePosixPath(html_path.relative_to(site).as_posix())
        expected_destination = html_lib.escape(
            destination_for_html(relative), quote=True
        )
        rendered = html_path.read_text(encoding="utf-8")
        required = (
            BRIDGE_MARKER,
            'name="robots" content="noindex,follow"',
            "window.location.replace(target)",
            f'<link rel="canonical" href="{expected_destination}">',
        )
        if any(marker not in rendered for marker in required):
            raise ValueError(f"Ponte HTML incompleta: {relative.as_posix()}")

    expected_worker = retirement_service_worker()
    for worker_path in worker_paths:
        if worker_path.read_text(encoding="utf-8") != expected_worker:
            raise ValueError(
                "Service worker antigo não foi aposentado: "
                f"{worker_path.relative_to(site).as_posix()}"
            )

    if (site / "manifest.webmanifest").read_text(encoding="utf-8") != bridge_manifest():
        raise ValueError("Manifesto legado não aponta para a identidade AldenirMed89.")
    print(
        f"✅ Ponte validada: {len(html_paths)} HTML e "
        f"{len(worker_paths)} service worker(s)."
    )
    return len(html_paths), len(worker_paths)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Converte o artefato Pages antigo em ponte para AldenirMed89."
    )
    parser.add_argument(
        "--check", action="store_true", help="Valida a ponte sem alterar arquivos."
    )
    parser.add_argument("site", type=Path, nargs="?", default=Path("site"))
    args = parser.parse_args()
    try:
        if args.check:
            check_bridge(args.site)
        else:
            build_bridge(args.site)
    except (OSError, ValueError) as exc:
        print(f"❌ Falha segura ao criar ponte: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
