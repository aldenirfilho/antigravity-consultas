# 00 — SUPERCOMANDO PARA O ANTIGRAVITY RENDERIZAR TUDO

Você está no repositório GitHub Pages:

`aldenirfilho/antigravity-consultas`

## Objetivo

Integrar o pacote `PACOTE_ANTIGRAVITY_ORGANIZACAO_ENCICLOPEDIA_2026_05_08` ao projeto principal, renderizar o catálogo, organizar cards, atualizar dados e validar links, sem apagar nenhum arquivo.

## Regras críticas

1. Não apagar arquivos.
2. Não mover arquivos ativos sem atualizar links relativos.
3. Preservar GitHub Pages funcionando.
4. Preservar:
   - `index.html`
   - `01_Modulos_Clinicos/AVC_Agudo/avc.html`
   - `02_Banco_Questoes_TEMI/index.html`
   - `03_Calculadoras_UTI/index.html`
   - `05_Biblioteca_IA/index.html`
   - `06_Card_Feed_Medico/index.html`
5. Criar backup lógico antes de qualquer mudança estrutural.
6. Todo novo arquivo deve ter caminho relativo válido.

## Tarefas

### 1. Copiar arquivos do pacote

Copie para a raiz do repositório:

- `CATALOGO_PROJETO.md`
- `data/catalogo.json`
- pasta `08_Documentacao_Projeto/`
- pasta `prompts_antigravity/`
- pasta `scripts_opcionais/`

### 2. Integrar catálogo na home

Atualize `index.html` para incluir uma seção:

`📦 Catálogo do Projeto`

A seção deve carregar `data/catalogo.json` e renderizar cards com:

- título;
- status;
- tipo;
- tema;
- legenda;
- botão “Abrir” quando houver `path`.

### 3. Atualizar Card Feed

Compare:

- `06_Card_Feed_Medico/data/cards.json`
- `PACOTE.../06_Card_Feed_Medico/data/cards_patch_sugerido.json`

Mescle os cards sem duplicar IDs.

### 4. Classificar Inbox

Use:

- `06_Card_Feed_Medico/data/inbox.json`
- `PACOTE.../06_Card_Feed_Medico/data/inbox_classificacao_modelo.json`

Para cada imagem em inbox:

1. Abrir/visualizar.
2. Identificar tema.
3. Renomear em snake_case.
4. Mover para pasta correta.
5. Atualizar `cards.json`.
6. Remover de `inbox.json` se classificada.
7. Manter em inbox se dúvida.

### 5. Atualizar mapa vivo

Atualize:

- `data/topics.json`
- `data/connections.json`

Incluindo pelo menos:

- AKI/TRS;
- VM/SDRA;
- Diabetes/Família;
- Card Feed;
- Biblioteca IA;
- Calculadoras UTI.

### 6. Gerar relatório final

Crie/atualize:

`08_Documentacao_Projeto/RELATORIO_ORGANIZACAO.md`

Incluindo:

- arquivos criados;
- arquivos alterados;
- imagens classificadas;
- links testados;
- pendências.

## Critério de sucesso

O projeto deve abrir corretamente em GitHub Pages e exibir:

- Home;
- Catálogo;
- AVC Agudo;
- Banco TEMI;
- Calculadoras UTI;
- Biblioteca IA;
- Card Feed;
- Mapa vivo;
- Cards classificados.
