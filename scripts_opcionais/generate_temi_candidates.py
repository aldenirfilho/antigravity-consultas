import json
import os
from datetime import datetime

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAT_PATH = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_catalogo.json")
QUESTIONS_OUT = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_temi_question_candidates.json")
PATCH_OUT = os.path.join(BASE_DIR, "02_Banco_Questoes_TEMI/data/qbank_patch_biblioteca.js")

with open(CAT_PATH, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

items = catalog['items']
candidates = []

# Critérios de seleção
target_themes = ['temi-prova', 'sepse-choque', 'vm-sdra', 'nefro-aki-trs', 'infectologia', 'neuro-uti']

for item in items:
    is_candidate = False
    if item['theme'] in target_themes:
        is_candidate = True
    elif any(tag.lower() in ['temi', 'amib', 'prova', 'guideline'] for tag in item.get('tags', [])):
        is_candidate = True
        
    if is_candidate:
        q = {
            "id": f"q-lib-{item['id']}",
            "sourceFileId": item['id'],
            "theme": item['theme'],
            "difficulty": "medio",
            "stem": f"[CANDIDATO] Questão baseada em: {item['title']}. Desenvolver enunciado clínico aqui.",
            "alternatives": {
                "A": "Opção A",
                "B": "Opção B",
                "C": "Opção C",
                "D": "Opção D",
                "E": "Opção E"
            },
            "answer": "A",
            "commentary": f"Comentário a ser extraído de {item['filename']}.",
            "temiPearl": f"Pérola TEMI associada ao tema {item['theme']}.",
            "tags": ["TEMI", "UTI"] + item.get('tags', [])
        }
        candidates.append(q)

# Save Outputs
with open(QUESTIONS_OUT, 'w', encoding='utf-8') as f:
    json.dump(candidates, f, indent=2, ensure_ascii=False)

# Save JS patch
js_content = f"// Patch gerado em {datetime.now().strftime('%Y-%m-%d')}\nconst QBANK_PATCH_BIBLIOTECA = " + json.dumps(candidates, indent=2, ensure_ascii=False) + ";"
with open(PATCH_OUT, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ Etapa 3 completa: {len(candidates)} candidatos a questões gerados.")
