# Pacote — Repadronização do Módulo Interativo AVC Agudo

**Data:** 2026-05-08  
**Projeto:** Enciclopédia Médica Intensiva & Medicina Interna  
**Alvo principal:** `01_Modulos_Clinicos/AVC_Agudo/avc.html`

## Objetivo

Reformatar e reorganizar o link **“Módulo Interativo”** do tópico AVC Agudo para ficar no mesmo padrão visual e editorial da Enciclopédia:

- fundo escuro institucional;
- variáveis globais de `assets/css/base.css`;
- cards glass;
- topbar e navegação coerentes;
- breadcrumbs limpos;
- responsividade iPhone/iPad/Mac;
- manutenção do motor dinâmico `avc.js`;
- preservação dos arquivos `db_*.js`.

## Como usar

1. Copie esta pasta para dentro do repositório no iCloud.
2. Abra o repositório no Antigravity.
3. Cole o conteúdo de:

```text
prompts_antigravity/00_SUPERCOMANDO_REPADRONIZAR_AVC.md
```

4. Peça ao Antigravity para executar, validar links e gerar relatório final.

## Arquivos principais do pacote

```text
prompts_antigravity/
├── 00_SUPERCOMANDO_REPADRONIZAR_AVC.md
├── 01_DIAGNOSTICO_E_META.md
├── 02_REFATORAR_AVC_HTML.md
├── 03_CRIAR_AVC_THEME_CSS.md
├── 04_COMPATIBILIZAR_AVC_JS.md
└── 05_VALIDAR_E_PUBLICAR.md

arquivos_prontos/
└── 01_Modulos_Clinicos/AVC_Agudo/
    ├── avc-theme.css
    └── avc_repadronizado_template.html

projeto/
├── PROJETO_MELHORIA_AVC_INTERATIVO.md
├── MAPA_DE_MUDANCAS.md
└── CHECKLIST_VALIDACAO_AVC.md
```

## Regra de segurança

Não apagar conteúdo clínico.  
Não mexer nos bancos `db_fundamentos.js`, `db_pratica.js`, `db_interativo.js`, `db_pesquisa.js`, `db_cross_ia.js` salvo se for apenas para corrigir caminhos de imagem.
