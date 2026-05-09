import json
import os
from datetime import datetime

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAT_PATH = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_catalogo.json")
BRAIN_PATH = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_brain_connections.json")
TOPICS_OUT = os.path.join(BASE_DIR, "data/topics_patch_biblioteca.json")
CONN_OUT = os.path.join(BASE_DIR, "data/connections_patch_biblioteca.json")
PATCH_OUT = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_brain_connections_patch.json")

with open(CAT_PATH, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

items = catalog['items']
new_nodes = []
new_edges = []

# Mapeamento de temas para módulos
module_map = {
    "neuro-uti": "avc-agudo",
    "vm-sdra": "ventilacao-mecanica",
    "nefro-aki-trs": "calculadoras-uti",
    "temi-prova": "banco-temi",
    "sepse-choque": "card-feed"
}

for item in items:
    # Apenas arquivos críticos ou temas específicos
    if item['theme'] in module_map:
        target_module = module_map[item['theme']]
        
        # Node
        node = {
            "id": f"brain-{item['id']}",
            "label": item['title'][:40] + "...",
            "type": "file",
            "theme": item['theme'],
            "path": item['path']
        }
        new_nodes.append(node)
        
        # Edges
        new_edges.append({ "from": f"brain-{item['id']}", "to": "biblioteca-ia", "relation": "pertence-a" })
        new_edges.append({ "from": f"brain-{item['id']}", "to": item['theme'], "relation": "vinculado-a" })
        new_edges.append({ "from": f"brain-{item['id']}", "to": target_module, "relation": "complementa-modulo" })

# Save Outputs
output = {
    "updatedAt": datetime.now().strftime("%Y-%m-%d"),
    "nodes": new_nodes,
    "edges": new_edges
}

with open(PATCH_OUT, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

# Generic topics/connections patch
with open(TOPICS_OUT, 'w', encoding='utf-8') as f:
    json.dump(new_nodes, f, indent=2, ensure_ascii=False)

with open(CONN_OUT, 'w', encoding='utf-8') as f:
    json.dump(new_edges, f, indent=2, ensure_ascii=False)

print(f"✅ Etapa 4 completa: {len(new_edges)} novas conexões cerebrais planejadas.")
