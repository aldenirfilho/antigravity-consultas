import json
import os
import sys
from datetime import datetime

def apply_patch(patch_path, target_path):
    print(f"🚀 Iniciando aplicação de patch: {patch_path}")
    
    if not os.path.exists(patch_path):
        print(f"❌ Erro: Arquivo de patch não encontrado: {patch_path}")
        return False
    
    if not os.path.exists(target_path):
        print(f"❌ Erro: Arquivo de destino não encontrado: {target_path}")
        return False

    with open(patch_path, 'r') as f:
        patch = json.load(f)
    
    with open(target_path, 'r') as f:
        target = json.load(f)

    ops = patch.get('operations', [])
    if not ops and 'new_edges' in patch:
        # Formato simplificado do export do mapa
        for edge in patch['new_edges']:
            ops.append({'op': 'addSuggestedEdge', 'edge': edge})

    print(f"📦 Operações encontradas: {len(ops)}")
    
    nodes_added = 0
    edges_added = 0
    
    for op_data in ops:
        op = op_data.get('op')
        
        if op == 'addNode':
            node = op_data.get('node')
            if node and node['id'] not in [n['id'] for n in target['nodes']]:
                target['nodes'].append(node)
                nodes_added += 1
                print(f"✅ Nó adicionado: {node['id']}")
        
        elif op == 'addSuggestedEdge' or op == 'addDirectEdge':
            edge = op_data.get('edge')
            # Garantir IDs corretos se vierem de template antigo
            if edge.get('to') == 'aki-trs': edge['to'] = 'nefro-aki-trs'
            
            exists = any(e['from'] == edge['from'] and e['to'] == edge['to'] for e in target['edges'])
            if not exists:
                target['edges'].append(edge)
                edges_added += 1
                print(f"🔗 Conexão adicionada: {edge['from']} -> {edge['to']}")

    target['updatedAt'] = datetime.now().strftime("%Y-%m-%d")
    
    with open(target_path, 'w') as f:
        json.dump(target, f, indent=2, ensure_ascii=False)
    
    print(f"\n✨ Patch aplicado com sucesso!")
    print(f"📊 Resumo: {nodes_added} nós e {edges_added} conexões.")
    return True

if __name__ == "__main__":
    p_path = sys.argv[1] if len(sys.argv) > 1 else "TEMPLATE_PATCH_MAPA_VIVO_ADMIN.json"
    t_path = "data/connections.json"
    apply_patch(p_path, t_path)
