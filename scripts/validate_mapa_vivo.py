#!/usr/bin/env python3
import json
import sys
import os

"""
VALIDADOR MAPA VIVO 4.0 — ANTIGRAVITY ENGINE
Verifica integridade de nós, conexões e conformidade com o Modo Curadoria.
"""

def validate_mapa(file_path):
    print(f"🧠 Validando Mapa Vivo 4.0: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado.")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"❌ Erro de sintaxe JSON: {e}")
            return False

    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    
    node_ids = set()
    errors = []
    warnings = []

    # 1. Validar Nós
    for n in nodes:
        nid = n.get('id')
        if not nid:
            errors.append(f"Nó sem ID encontrado.")
            continue
        
        if nid in node_ids:
            errors.append(f"ID duplicado: {nid}")
        node_ids.add(nid)

        if not n.get('label'):
            warnings.append(f"Nó {nid} sem label (usará ID).")
        
        if not n.get('type'):
            warnings.append(f"Nó {nid} sem tipo (default: theme).")

    # 2. Validar Conexões
    for i, e in enumerate(edges):
        source = e.get('from')
        target = e.get('to')

        if not source or not target:
            errors.append(f"Conexão #{i} incompleta (from/to ausente).")
            continue

        if source not in node_ids:
            errors.append(f"Conexão #{i} aponta para origem inexistente: {source}")
        
        if target not in node_ids:
            errors.append(f"Conexão #{i} aponta para destino inexistente: {target}")

        strength = e.get('strength') or e.get('status') or e.get('style')
        if not strength:
            warnings.append(f"Conexão {source}->{target} sem definição de força/estilo.")

    # 3. Resultado
    print(f"📊 Estatísticas: {len(nodes)} nós, {len(edges)} conexões.")
    
    if warnings:
        print(f"\n⚠️ Avisos ({len(warnings)}):")
        for w in warnings[:10]: print(f"  - {w}")
        if len(warnings) > 10: print(f"  ... e mais {len(warnings)-10} avisos.")

    if errors:
        print(f"\n❌ ERROS ({len(errors)}):")
        for e in errors: print(f"  - {e}")
        return False
    
    print("\n✅ Validação concluída com sucesso!")
    return True

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/connections.json"
    if not validate_mapa(path):
        sys.exit(1)
