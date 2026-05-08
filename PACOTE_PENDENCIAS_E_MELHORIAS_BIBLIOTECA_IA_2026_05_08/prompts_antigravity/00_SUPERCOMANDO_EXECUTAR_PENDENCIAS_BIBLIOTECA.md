# 00 — SUPERCOMANDO ANTIGRAVITY: Executar Pendências da Biblioteca IA

Você está no repositório:

`aldenirfilho/antigravity-consultas`

## Objetivo

Executar as pendências pós-classificação da Biblioteca IA:

1. Revisar duplicados.
2. Transformar materiais de alto rendimento em cards.
3. Transformar materiais TEMI em questões.
4. Conectar arquivos críticos aos módulos clínicos.
5. Validar JSON, links, preview e publicação.
6. Registrar roadmap de 30 melhorias futuras.

## Arquivos de apoio

Copiar/integrar:

- `data/pendencias_biblioteca_ia.json`
- `05_Biblioteca_IA/data/pendencias_biblioteca_ia.json`
- `data/roadmap_30_melhorias_biblioteca_ia.json`
- `08_Documentacao_Projeto/PLANO_EXECUCAO_PENDENCIAS_BIBLIOTECA.md`
- `08_Documentacao_Projeto/ROADMAP_30_MELHORIAS_BIBLIOTECA_IA.md`
- `08_Documentacao_Projeto/CHECKLIST_PENDENCIAS_BIBLIOTECA.md`

## Regras críticas

1. Não apagar arquivos.
2. Não sobrescrever catálogo sem backup lógico.
3. Não mover arquivo sem atualizar `biblioteca_catalogo.json`.
4. Se houver dúvida clínica/editorial, marcar `status: "revisar"`.
5. Trabalhar em etapas, salvando relatório após cada uma.
6. Todo patch gerado deve ser separado antes de mesclar.

## Etapa 1 — Revisar duplicados

Executar prompt:

`prompts_antigravity/01_REVISAR_DUPLICADOS.md`

Gerar:

- `05_Biblioteca_IA/data/biblioteca_duplicados.json`
- `08_Documentacao_Projeto/RELATORIO_DUPLICADOS_BIBLIOTECA.md`

## Etapa 2 — Gerar cards de alto rendimento

Executar prompt:

`prompts_antigravity/02_GERAR_CARDS_ALTO_RENDIMENTO.md`

Gerar:

- `05_Biblioteca_IA/data/biblioteca_card_candidates.json`
- `06_Card_Feed_Medico/data/cards_patch_biblioteca.json`

## Etapa 3 — Gerar questões TEMI

Executar prompt:

`prompts_antigravity/03_GERAR_QUESTOES_TEMI.md`

Gerar:

- `05_Biblioteca_IA/data/biblioteca_temi_question_candidates.json`
- `02_Banco_Questoes_TEMI/data/qbank_patch_biblioteca.js`

## Etapa 4 — Conectar arquivos críticos aos módulos

Executar prompt:

`prompts_antigravity/04_CONECTAR_ARQUIVOS_CRITICOS_MODULOS.md`

Gerar:

- `data/topics_patch_biblioteca.json`
- `data/connections_patch_biblioteca.json`
- `05_Biblioteca_IA/data/biblioteca_brain_connections_patch.json`

## Etapa 5 — Validar e publicar

Executar prompt:

`prompts_antigravity/05_VALIDAR_PUBLICAR_BIBLIOTECA.md`

Gerar:

- `08_Documentacao_Projeto/RELATORIO_VALIDACAO_BIBLIOTECA.md`

## Etapa 6 — Roadmap futuro

Integrar:

`08_Documentacao_Projeto/ROADMAP_30_MELHORIAS_BIBLIOTECA_IA.md`

e criar seção na Biblioteca IA chamada:

`🚀 Próximas melhorias`

## Critério de sucesso

- JSON válido.
- Sem IDs duplicados.
- Cards candidatos gerados.
- Questões TEMI candidatas geradas.
- Conexões cerebrais atualizadas.
- Relatórios criados.
- Biblioteca IA abre normalmente.
