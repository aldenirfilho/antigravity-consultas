#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime
import shutil

"""
APLICADOR DE PATCH MAPA VIVO 4.0 — ANTIGRAVITY ENGINE
Mescla alterações do Modo Curadoria ao banco de dados oficial connections.json.
"""

def apply_patch(target_path, patch_path):
    print(f"🧠 Aplicador de Patch Mapa Vivo 4.0")
    
    if not os.path.exists(target_path):
        print(f"❌ Erro: Arquivo de destino {target_path} não encontrado.")
        sys.exit(1)
        
    if not os.path.exists(patch_path):
        print(f"❌ Erro: Arquivo de patch {patch_path} não encontrado.")
        sys.exit(1)

    # 1. Carregar Dados
    with open(target_path, 'r', encoding='utf-8') as f:
        target = json.load(f)
    
    with open(patch_path, 'r', encoding='utf-8') as f:
        patch = json.load(f)

    # 2. Backup de Segurança
    backup_path = f"{target_path}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    shutil.copy2(target_path, backup_path)
    print(f"🛡️ Backup criado: {backup_path}")

    # 3. Processar Patch (Overlay Layer)
    # Suporta formato de exportação direta do Mapa Vivo 4.0
    added_nodes = patch.get('addedNodes', [])
    updated_nodes = patch.get('updatedNodes', {})
    hidden_node_ids = patch.get('hiddenNodeIds', [])
    added_edges = patch.get('addedEdges', [])
    hidden_edge_keys = patch.get('hiddenEdgeKeys', [])
    positions = patch.get('positions', {})

    stats = {"nodes_added": 0, "nodes_updated": 0, "nodes_hidden": 0, "edges_added": 0, "edges_hidden": 0, "pos_updated": 0}

    # 3.1 Adicionar/Atualizar Nós
    node_map = {n['id']: n for n in target['nodes']}
    
    for node in added_nodes:
        if node['id'] not in node_map:
            target['nodes'].append(node)
            node_map[node['id']] = node
            stats["nodes_added"] += 1
            print(f"✅ Nó Adicionado: {node['id']}")

    for nid, p in updated_nodes.items():
        if nid in node_map:
            node_map[nid].update(p)
            stats["nodes_updated"] += 1
            print(f"📝 Nó Atualizado: {nid}")

    for nid in hidden_node_ids:
        if nid in node_map:
            node_map[nid]['visible'] = False
            node_map[nid]['status'] = 'oculto'
            stats["nodes_hidden"] += 1
            print(f"🚫 Nó Ocultado: {nid}")

    # 3.2 Atualizar Posições
    for nid, pos in positions.items():
        if nid in node_map:
            node_map[nid]['x'] = pos['x']
            node_map[nid]['y'] = pos['y']
            stats["pos_updated"] += 1

    # 3.3 Adicionar/Ocultar Edges
    edge_keys = {f"{e['from']}->{e['to']}": e for e in target['edges']}
    
    for edge in added_edges:
        key = f"{edge['from']}->{edge['to']}"
        if key not in edge_keys:
            target['edges'].append(edge)
            edge_keys[key] = edge
            stats["edges_added"] += 1
            print(f"🔗 Conexão Adicionada: {key}")

    for key in hidden_edge_keys:
        if key in edge_keys:
            edge_keys[key]['visible'] = False
            stats["edges_hidden"] += 1
            print(f"✂️ Conexão Ocultada: {key}")

    # 4. Finalização
    target['updatedAt'] = datetime.now().isoformat()
    target['version'] = "4.0"

    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(target, f, indent=2, ensure_ascii=False)

    print(f"\n✨ Patch aplicado com sucesso!")
    print(f"📊 Resumo: {stats['nodes_added']} novos, {stats['nodes_updated']} editados, {stats['nodes_hidden']} ocultos, {stats['edges_added']} links.")
    print(f"📍 Posições fixadas: {stats['pos_updated']}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python apply_mapa_vivo_patch.py <target_json> <patch_json>")
    else:
        apply_patch(sys.argv[1], sys.argv[2])
