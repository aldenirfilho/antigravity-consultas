# Projeto — Mapa Vivo 2.0

## Diagnóstico

O mapa vivo atual já existe, mas ainda está limitado:

- `data/topics.json` está centrado em AVC e poucos subtemas.
- `data/connections.json` tem poucos nós.
- `assets/js/graph.js` renderiza botões/nós, mas não desenha as arestas do grafo.
- O mapa ainda não conecta Biblioteca IA, Card Feed, Banco TEMI, Calculadoras e macrotemas de UTI.

## Objetivo

Criar um mapa visual que funcione como o cérebro da Enciclopédia:

```text
Portal
├── Biblioteca IA
│   ├── gera cards
│   ├── gera questões
│   └── alimenta módulos
├── Card Feed
├── Banco TEMI
├── Calculadoras UTI
└── Módulos clínicos
    ├── AVC Agudo
    ├── VM/SDRA
    ├── Sepse/Choque
    ├── AKI/TRS
    ├── Infectologia
    └── Endócrino/Metabólico
```

## Regras

- Nós ativos devem ter link.
- Nós planejados podem ter `url: "#"` e status `planejado`.
- Toda conexão deve ter `relation`.
- O mapa deve ser navegável, visual e seguro para expansão.
