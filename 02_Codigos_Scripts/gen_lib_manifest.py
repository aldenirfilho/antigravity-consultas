import os
import json
from datetime import datetime

inbox_dir = "05_Biblioteca_IA/inbox"
output_file = "05_Biblioteca_IA/data/biblioteca_inbox_manifest_auto.json"

def generate_manifest():
    if not os.path.exists(inbox_dir):
        print(f"Erro: Diretorio {inbox_dir} nao encontrado.")
        return

    files = []
    for filename in os.listdir(inbox_dir):
        if filename.startswith('.') or filename == "README.md": continue
        
        path = os.path.join(inbox_dir, filename)
        if os.path.isfile(path):
            ext = os.path.splitext(filename)[1].lower().replace('.', '')
            size = os.path.getsize(path)
            files.append({
                "name": filename,
                "path": f"05_Biblioteca_IA/inbox/{filename}",
                "extension": ext,
                "sizeBytes": size,
                "addedAt": datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d')
            })

    manifest = {
        "updatedAt": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "totalFiles": len(files),
        "files": sorted(files, key=lambda x: x['name'])
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"Manifesto gerado com {len(files)} arquivos em {output_file}")

if __name__ == "__main__":
    generate_manifest()
