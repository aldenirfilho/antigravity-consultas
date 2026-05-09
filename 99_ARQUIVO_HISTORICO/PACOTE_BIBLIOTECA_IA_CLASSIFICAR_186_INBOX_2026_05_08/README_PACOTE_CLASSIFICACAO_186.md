# Pacote Antigravity — Classificação de 186 arquivos do Inbox da Biblioteca IA

**Data:** 2026-05-08  
**Projeto:** Enciclopédia Médica Intensiva & Medicina Interna  
**Alvo:** `05_Biblioteca_IA/inbox/`

## Objetivo

Este pacote entrega os comandos, schemas e arquivos-base para o Antigravity:

- escanear 186 arquivos do inbox;
- criar fila de triagem manual;
- classificar por tema;
- catalogar metadados;
- organizar em pastas;
- criar conexão cerebral/grafo semântico;
- atualizar a Biblioteca IA.

## Como usar

1. Descompacte este ZIP.
2. Copie a pasta para dentro do repositório local no iCloud.
3. Abra o projeto no Antigravity.
4. Cole o conteúdo de:

```text
prompts_antigravity/00_SUPERCOMANDO_CLASSIFICAR_186_BIBLIOTECA.md
```

5. Peça para executar em lotes de 20 arquivos.

## Arquivos principais

```text
data/
├── biblioteca_taxonomia_temas.json
├── biblioteca_inbox_manifest_186.json
├── biblioteca_catalogo_base.json
├── biblioteca_item_schema.json
├── biblioteca_brain_connections.json
└── matriz_classificacao_biblioteca.csv

05_Biblioteca_IA/data/
├── biblioteca_taxonomia_temas.json
├── biblioteca_inbox_manifest_186.json
├── biblioteca_catalogo.json
└── biblioteca_brain_connections.json

prompts_antigravity/
├── 00_SUPERCOMANDO_CLASSIFICAR_186_BIBLIOTECA.md
├── 01_ESCANEAR_INBOX.md
├── 02_CRIAR_PASTAS_TEMAS.md
├── 03_INTERFACE_MANUAL_CLASSIFICACAO.md
├── 04_CLASSIFICAR_LOTE_20.md
├── 05_CONEXAO_CEREBRAL.md
└── 06_VALIDAR_JSON_LINKS.md
```

## Observação importante

GitHub Pages é estático. Ele não grava sozinho no repositório.  
Por isso o fluxo recomendado é:

- usar interface para visualizar/copiar/exportar JSON;
- usar o Antigravity para mesclar o JSON no repositório;
- validar e publicar.
