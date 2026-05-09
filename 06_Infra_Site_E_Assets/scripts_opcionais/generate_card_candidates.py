import json
import os
from datetime import datetime

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAT_PATH = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_catalogo.json")
CARDS_OUT = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_card_candidates.json")
PATCH_OUT = os.path.join(BASE_DIR, "06_Card_Feed_Medico/data/cards_patch_biblioteca.json")

with open(CAT_PATH, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

items = catalog['items']
candidates = []

# Critérios de seleção
target_themes = ['sepse-choque', 'vm-sdra', 'nefro-aki-trs', 'infectologia', 'neuro-uti', 'endocrino-metabolico']
target_tags = ['uti', 'temi', 'plantão', 'protocolo', 'algoritmo', 'dose', 'emergência']

for item in items:
    is_candidate = False
    if item['theme'] in target_themes:
        is_candidate = True
    elif any(tag.lower() in target_tags for tag in item.get('tags', [])):
        is_candidate = True
        
    if is_candidate:
        card = {
            "id": f"lib-card-{item['id']}",
            "title": item['title'],
            "theme": item['theme'], # Map theme to card feed theme later if needed
            "tags": item.get('tags', []),
            "explanation": item.get('resumo', f"Material sobre {item['title']} organizado para uso rápido na UTI."),
            "source": f"Biblioteca IA ({item['filename']}) + curadoria Dr. Aldenir Rocha",
            "status": "candidato",
            "imageUrl": "pending",
            "createdAt": datetime.now().strftime("%Y-%m-%d"),
            "related": [item['id'], item['theme']]
        }
        candidates.append(card)

# Save Outputs
with open(CARDS_OUT, 'w', encoding='utf-8') as f:
    json.dump(candidates, f, indent=2, ensure_ascii=False)

with open(PATCH_OUT, 'w', encoding='utf-8') as f:
    json.dump(candidates, f, indent=2, ensure_ascii=False)

print(f"✅ Etapa 2 completa: {len(candidates)} candidatos a cards gerados.")
