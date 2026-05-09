import json
import os
import re
from datetime import datetime

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAT_PATH = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_catalogo.json")
DUP_OUT = os.path.join(BASE_DIR, "05_Biblioteca_IA/data/biblioteca_duplicados.json")
REPORT_OUT = os.path.join(BASE_DIR, "08_Documentacao_Projeto/RELATORIO_DUPLICADOS_BIBLIOTECA.md")

with open(CAT_PATH, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

items = catalog['items']
duplicates = []
seen_titles = {}
seen_filenames = {}

# Normalizar título para comparação
def normalize(text):
    text = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
    return text

for i, item in enumerate(items):
    t_norm = normalize(item['title'])
    f_norm = normalize(item['filename'])
    
    # Check Title
    if t_norm in seen_titles:
        duplicates.append({
            "groupId": f"dup-t-{len(duplicates)+1:03d}",
            "confidence": "alta",
            "reason": "Mesmo título normalizado",
            "items": [seen_titles[t_norm], item['id']],
            "recommendedAction": "revisar"
        })
    else:
        seen_titles[t_norm] = item['id']
        
    # Check Filename (if not already caught by title)
    if f_norm in seen_filenames:
        # Avoid duplicate groups for the same pair
        if not any(item['id'] in d['items'] and seen_filenames[f_norm] in d['items'] for d in duplicates):
            duplicates.append({
                "groupId": f"dup-f-{len(duplicates)+1:03d}",
                "confidence": "alta",
                "reason": "Mesmo nome de arquivo original",
                "items": [seen_filenames[f_norm], item['id']],
                "recommendedAction": "manter-mais-recente"
            })
    else:
        seen_filenames[f_norm] = item['id']

# Save JSON
output = {
    "updatedAt": datetime.now().strftime("%Y-%m-%d"),
    "duplicates": duplicates
}
with open(DUP_OUT, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

# Generate Report
report = f"""# 📋 Relatório de Duplicados — Biblioteca IA
**Data:** {datetime.now().strftime('%Y-%m-%d')}

## Resumo
- **Total de itens analisados:** {len(items)}
- **Grupos de duplicidade encontrados:** {len(duplicates)}

## Detalhamento
"""

for dup in duplicates:
    item_names = []
    for id_ in dup['items']:
        it = next(x for x in items if x['id'] == id_)
        item_names.append(f"`{it['title']}` ({it['filename']})")
    
    report += f"""
### Grupo {dup['groupId']}
- **Confiança:** {dup['confidence']}
- **Motivo:** {dup['reason']}
- **Itens:**
  - {item_names[0]}
  - {item_names[1]}
- **Ação recomendada:** {dup['recommendedAction']}
"""

with open(REPORT_OUT, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✅ Etapa 1 completa: {len(duplicates)} grupos de duplicidade encontrados.")
