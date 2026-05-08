#!/usr/bin/env python3
"""Validador simples do Mapa Vivo 3.1.
Uso no terminal do Antigravity:
python3 scripts/validate_mapa_vivo.py data/connections.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_NODE_TYPES = {"hub", "biblioteca", "feed", "qbank", "tool", "module", "topic", "theme", "file"}
ALLOWED_EDGE_STRENGTHS = {"direct", "suggested"}
HIDDEN_STATUSES = {"oculto", "rejeitado"}


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/connections.json")
    if not path.exists():
        print(f"❌ Arquivo não encontrado: {path}")
        return 2

    data = json.loads(path.read_text(encoding="utf-8"))
    nodes = data.get("nodes") or data.get("topics") or []
    edges = data.get("edges") or data.get("connections") or []

    errors: list[str] = []
    warnings: list[str] = []
    ids: set[str] = set()

    for i, node in enumerate(nodes):
        node_id = str(node.get("id") or "").strip()
        if not node_id:
            errors.append(f"node[{i}] sem id")
            continue
        if node_id in ids:
            errors.append(f"id duplicado: {node_id}")
        ids.add(node_id)
        if not node.get("label"):
            warnings.append(f"node {node_id} sem label")
        if not node.get("body"):
            warnings.append(f"node {node_id} sem body")
        node_type = node.get("type", "theme")
        if node_type not in ALLOWED_NODE_TYPES:
            warnings.append(f"node {node_id} com type inesperado: {node_type}")

    for i, edge in enumerate(edges):
        from_id = edge.get("from") or edge.get("source")
        to_id = edge.get("to") or edge.get("target")
        if not from_id or not to_id:
            errors.append(f"edge[{i}] sem from/to")
            continue
        if from_id not in ids:
            errors.append(f"edge órfã: from={from_id} não existe")
        if to_id not in ids:
            errors.append(f"edge órfã: to={to_id} não existe")
        if not edge.get("relation"):
            warnings.append(f"edge {from_id}->{to_id} sem relation; use 'conecta'")
        strength = edge.get("strength", "direct")
        if strength not in ALLOWED_EDGE_STRENGTHS:
            warnings.append(f"edge {from_id}->{to_id} com strength inesperado: {strength}")
        if strength == "suggested" and edge.get("status", "sugerido") == "ativo":
            warnings.append(f"edge suggested {from_id}->{to_id} deveria ter status 'sugerido' até aprovação")
        if edge.get("status") in HIDDEN_STATUSES and edge.get("visible", True) is not False:
            warnings.append(f"edge {from_id}->{to_id} oculto/rejeitado deveria ter visible=false")

    print("🧠 Validação do Mapa Vivo 3.1")
    print(f"Nós: {len(nodes)} | Edges: {len(edges)}")
    if warnings:
        print("\n⚠️ Avisos:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("\n❌ Erros:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("\n✅ Sem erros críticos. Pronto para renderização.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
