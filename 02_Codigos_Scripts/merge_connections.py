import json
import os
from datetime import datetime

def merge_connections():
    root_path = "/Users/aldenirfilho/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian/Antigravity_Consultas"
    main_conn_path = os.path.join(root_path, "data/connections.json")
    bib_conn_path = os.path.join(root_path, "05_Biblioteca_IA/data/biblioteca_brain_connections.json")
    output_path = main_conn_path

    if not os.path.exists(main_conn_path):
        print(f"Erro: {main_conn_path} não encontrado.")
        return

    with open(main_conn_path, 'r', encoding='utf-8') as f:
        main_data = json.load(f)

    if os.path.exists(bib_conn_path):
        with open(bib_conn_path, 'r', encoding='utf-8') as f:
            bib_data = json.load(f)
        
        # Mapa de IDs existentes no principal para evitar duplicatas
        existing_nodes = {n['id']: n for n in main_data.get('nodes', [])}
        
        # Adicionar novos nós da biblioteca
        nodes_added = 0
        for node in bib_data.get('nodes', []):
            if node['id'] not in existing_nodes:
                # Normalizar campos se necessário
                if 'body' not in node:
                    node['body'] = f"Arquivo da Biblioteca: {node.get('label', 'Sem título')}"
                if 'url' not in node:
                    node['url'] = "05_Biblioteca_IA/index.html"
                if 'status' not in node:
                    node['status'] = "ativo"
                
                main_data['nodes'].append(node)
                nodes_added += 1
            else:
                # Opcional: atualizar metadados se o do principal estiver incompleto
                pass

        # Adicionar novas arestas (edges/links)
        existing_edges = set()
        for e in main_data.get('edges', []):
            existing_edges.add(f"{e.get('from')}->{e.get('to')}")
            # Compatibilidade com source/target se existir
            if 'source' in e and 'target' in e:
                existing_edges.add(f"{e['source']}->{e['target']}")

        edges_added = 0
        for edge in bib_data.get('edges', []):
            # Normalizar de/para ou source/target
            u = edge.get('from') or edge.get('source')
            v = edge.get('to') or edge.get('target')
            
            if u and v:
                key = f"{u}->{v}"
                if key not in existing_edges:
                    # Garantir formato canonical {from, to, relation}
                    new_edge = {
                        "from": u,
                        "to": v,
                        "relation": edge.get('relation') or "conecta"
                    }
                    main_data['edges'].append(new_edge)
                    existing_edges.add(key)
                    edges_added += 1

        print(f"Nós adicionados: {nodes_added}")
        print(f"Conexões adicionadas: {edges_added}")

    # Atualizar timestamp
    main_data['updatedAt'] = datetime.now().isoformat()
    main_data['version'] = "4.2-unified"

    # Backup antes de salvar
    backup_path = main_conn_path + f".{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    with open(main_conn_path, 'r', encoding='utf-8') as f:
        original = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original)

    # Salvar unificado
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, indent=2, ensure_ascii=False)

    print(f"Sucesso! Mapa Vivo unificado em {output_path}")

if __name__ == "__main__":
    merge_connections()
