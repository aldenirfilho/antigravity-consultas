#!/usr/bin/env bash
set -e

INBOX_DIR="06_Card_Feed_Medico/assets/cards/inbox"
OUT="06_Card_Feed_Medico/data/inbox.json"

mkdir -p "$(dirname "$OUT")"

python3 - <<'PY'
import json
from pathlib import Path
from datetime import date

inbox = Path("06_Card_Feed_Medico/assets/cards/inbox")
files = []
if inbox.exists():
    files = sorted([p.name for p in inbox.iterdir() if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]])

payload = {
    "description": "Lista de imagens na pasta inbox para classificação. Gerada pelo script scan_inbox.sh",
    "updatedAt": str(date.today()),
    "files": files
}

Path("06_Card_Feed_Medico/data/inbox.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(f"OK: {len(files)} imagens listadas em inbox.json")
PY
