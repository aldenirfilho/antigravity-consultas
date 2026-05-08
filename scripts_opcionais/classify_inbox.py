import os
import json
import re
from datetime import datetime

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INBOX_DIR = os.path.join(BASE_DIR, "05_Biblioteca_IA/inbox")
TAX_PATH = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_taxonomia_temas.json")
CAT_OUT = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_catalogo.json")
BRAIN_OUT = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_brain_connections.json")

# Carregar taxonomia
with open(TAX_PATH, 'r', encoding='utf-8') as f:
    taxonomy = json.load(f)

themes = taxonomy['themes']

# Listar arquivos do inbox
files = [f for f in os.listdir(INBOX_DIR) if f not in ['.DS_Store', 'README.md'] and os.path.isfile(os.path.join(INBOX_DIR, f))]

print(f"📂 Total de arquivos no inbox: {len(files)}")

def get_type(name):
    ext = os.path.splitext(name)[1].lower().replace('.', '')
    if ext in ['pdf']: return 'pdf'
    if ext in ['docx', 'doc']: return 'word'
    if ext in ['html', 'htm']: return 'html'
    if ext in ['md', 'txt']: return 'text'
    if ext in ['csv', 'xlsx']: return 'data'
    if ext in ['png', 'jpg', 'jpeg', 'webp']: return 'image'
    return 'outro'

def classify(filename):
    clean_name = re.sub(r'[_.-]', ' ', filename).lower()
    best_theme = None
    best_score = 0
    
    for theme in themes:
        if theme['id'] == 'inbox-revisar': continue
        score = 0
        for kw in theme['keywords']:
            if kw.lower() in clean_name:
                score += len(kw)
        
        if score > best_score:
            best_score = score
            best_theme = theme
            
    # Score de corte: pelo menos 3 caracteres batendo
    if best_score >= 3:
        return best_theme
    return next(t for t in themes if t['id'] == 'inbox-revisar')

def to_slug(name):
    name_no_ext = os.path.splitext(name)[0]
    slug = re.sub(r'[^a-zA-Z0-9]', '-', name_no_ext).lower()
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug[:80]

def to_title(name):
    name_no_ext = os.path.splitext(name)[0]
    title = re.sub(r'[_.-]+', ' ', name_no_ext)
    return title.title().strip()

items = []
nodes = [
    { "id": "biblioteca-ia", "label": "📚 Biblioteca IA", "type": "module", "theme": "projeto", "path": "05_Biblioteca_IA/index.html" }
]
edges = []
stats = {}

for file in files:
    theme = classify(file)
    tipo = get_type(file)
    slug = to_slug(file)
    title = to_title(file)
    theme_id = theme['id']
    
    stats[theme_id] = stats.get(theme_id, 0) + 1
    
    items.append({
        "id": slug,
        "title": title,
        "filename": file,
        "theme": theme_id,
        "tipo": tipo,
        "tags": [theme_id, tipo],
        "status": "revisar" if theme_id == 'inbox-revisar' else "catalogado",
        "path": "inbox/" + file,
        "resumo": "",
        "ia_origem": "Auto-classificado",
        "data": "2026-05",
        "createdAt": datetime.now().isoformat()
    })
    
    # Brain node
    nodes.append({
        "id": slug,
        "label": (theme['emoji'] + ' ' if theme else '📥 ') + title[:50],
        "type": "file",
        "theme": theme_id,
        "path": "inbox/" + file
    })
    
    # Brain edges
    edges.append({ "from": slug, "to": "biblioteca-ia", "relation": "pertence-a" })
    edges.append({ "from": slug, "to": theme_id, "relation": "classificado-em" })
    
    # Extra connections
    if theme_id == 'temi-prova' or 'temi' in file.lower():
        edges.append({ "from": slug, "to": "banco-temi", "relation": "gera-questoes" })
    if theme_id == 'farmaco-doses' or any(kw in file.lower() for kw in ['dose', 'calculo', 'dilu']):
        edges.append({ "from": slug, "to": "calculadoras-uti", "relation": "apoia-calculo" })

# Add theme nodes
for theme in themes:
    nodes.append({
        "id": theme['id'],
        "label": theme['emoji'] + ' ' + theme['label'],
        "type": "theme",
        "theme": theme['id'],
        "path": theme['folder']
    })

# Save catalog
catalog = {
    "updatedAt": datetime.now().strftime("%Y-%m-%d"),
    "project": "Biblioteca IA — Enciclopédia Médica Intensiva",
    "totalFiles": len(items),
    "stats": stats,
    "items": items
}
with open(CAT_OUT, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

# Save brain
brain = {
    "updatedAt": datetime.now().strftime("%Y-%m-%d"),
    "nodes": nodes,
    "edges": edges
}
with open(BRAIN_OUT, 'w', encoding='utf-8') as f:
    json.dump(brain, f, indent=2, ensure_ascii=False)

print(f"\n✅ Catálogo gerado: {len(items)} arquivos")
print(f"📊 Classificação por tema:")
sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
for theme_id, count in sorted_stats:
    t = next((th for th in themes if th['id'] == theme_id), None)
    emoji = t['emoji'] if t else '📥'
    print(f"   {emoji} {theme_id}: {count}")

print(f"\n🧠 Brain: {len(nodes)} nós, {len(edges)} edges")
print(f"📄 Salvos em:")
print(f"   {CAT_OUT}")
print(f"   {BRAIN_OUT}")
