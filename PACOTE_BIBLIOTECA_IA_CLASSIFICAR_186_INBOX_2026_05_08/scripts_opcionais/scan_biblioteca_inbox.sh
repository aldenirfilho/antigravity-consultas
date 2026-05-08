#!/usr/bin/env bash
set -e

INBOX_DIR="05_Biblioteca_IA/inbox"
OUT="05_Biblioteca_IA/data/biblioteca_inbox_manifest_186.json"

mkdir -p "05_Biblioteca_IA/data"

python3 - <<'PY'
import json
from pathlib import Path
from datetime import date

inbox = Path("05_Biblioteca_IA/inbox")
files = []
if inbox.exists():
    files = sorted([p for p in inbox.iterdir() if p.is_file()])

items = []
for i, p in enumerate(files, start=1):
    ext = p.suffix.lower().replace(".", "") or "outro"
    items.append({
        "seq": i,
        "id": f"inbox-{i:03d}",
        "originalFilename": p.name,
        "currentPath": str(p).replace("\\", "/"),
        "suggestedTheme": "inbox-revisar",
        "finalTheme": "",
        "newFilename": "",
        "title": "",
        "type": ext,
        "status": "inbox",
        "priority": "revisar",
        "tags": [],
        "summary": "",
        "clinicalUse": "",
        "temiRelevance": "",
        "safetyNotes": "",
        "relatedTopics": [],
        "brainConnections": [],
        "reviewedBy": "Dr. Aldenir Rocha",
        "reviewDate": "",
        "notes": "Abrir manualmente na interface, classificar por tema, preencher metadados e mover para pasta final."
    })

payload = {
    "updatedAt": str(date.today()),
    "description": "Manifesto gerado automaticamente a partir da pasta inbox.",
    "totalExpected": 186,
    "totalFound": len(items),
    "sourceFolder": "05_Biblioteca_IA/inbox/",
    "items": items
}

Path("05_Biblioteca_IA/data/biblioteca_inbox_manifest_186.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(f"OK: {len(items)} arquivos listados.")
if len(items) != 186:
    print(f"⚠️ Atenção: esperado 186, encontrado {len(items)}.")
PY
