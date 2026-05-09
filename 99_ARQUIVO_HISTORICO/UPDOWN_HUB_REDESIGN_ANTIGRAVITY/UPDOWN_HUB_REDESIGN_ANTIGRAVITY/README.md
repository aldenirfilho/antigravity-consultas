# UPDOWN HUB — Reorganização da página principal + aplicações extras

Este pacote foi preparado para ser inserido no repositório do projeto **Enciclomedia / UpDown**.

## Objetivo

Reorganizar a página de UpDown como um **hub médico em modo leitor**, com conexão direta entre:

```text
UPDOWN  ↔  BIBLIOTECA  ↔  IMAGENS
```

Cada artigo transformado em UpDown passa a ter três portas: **ler conteúdo didático**, **consultar biblioteca/fonte** e **ver ou gerar imagens relacionadas**.

## O que remover da página atual

Remover ou ocultar da página pública os blocos que não estão bem caracterizados:

- tópico genérico de **templates**;
- tópico de **conexão com VM**;
- qualquer bloco técnico solto sem relação clara com UpDown, Biblioteca, Imagens ou Aplicações Extras.

Esses itens podem ficar em área administrativa/privada, mas não devem competir com a navegação central.

## Estrutura do pacote

```text
01_pagina_updown/
├── updown_home_reorganizada.md
├── triangulo_updown_biblioteca_imagens.md
└── cards_modulos_updown.md

02_aplicacoes_extras/
├── hub_aplicacoes_extras.md
└── roadmap_calculadoras_uti.md

03_calculadoras/
├── calculadora_drogas_vasoativas_v2.md
├── especificacao_formula_mlh_dose.md
└── prescricoes_comuns_brasil_vasoativas.md

04_antigravity/
├── instrucoes_antigravity.md
├── checklist_implementacao.md
└── prompt_universal_refatoracao_updown.md

05_data/
└── vasoactive_drugs_brasil_presets.json
```

## Regra de ouro

A página pública deve ser limpa, prática e intuitiva. Bastidores, prompts, notas internas e sugestões de produção ficam em arquivos privados ou no chat.
