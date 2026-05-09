# 05 — Validar e publicar Biblioteca IA

## Objetivo

Validar integridade após catalogação, cards, questões e conexões.

## Validar JSON

- `05_Biblioteca_IA/data/biblioteca_catalogo.json`
- `05_Biblioteca_IA/data/biblioteca_brain_connections.json`
- `05_Biblioteca_IA/data/biblioteca_duplicados.json`
- `05_Biblioteca_IA/data/biblioteca_card_candidates.json`
- `05_Biblioteca_IA/data/biblioteca_temi_question_candidates.json`

## Verificações

- IDs duplicados.
- Status inválido.
- Theme inexistente.
- Caminho inexistente.
- Arquivo sem resumo.
- Arquivo sem tags.
- Arquivo crítico sem safetyNotes.
- Arquivo TEMI sem relação com Banco TEMI.
- Arquivo dose/cálculo sem relação com Calculadoras UTI.
- Arquivo visual sem relação com Card Feed.

## Validar interface

- Biblioteca abre.
- Busca funciona.
- Filtros funcionam.
- Cards aparecem.
- Preview abre.
- Estatísticas atualizam.
- Seção mapa cerebral aparece.

## Saída

Criar:

`08_Documentacao_Projeto/RELATORIO_VALIDACAO_BIBLIOTECA.md`
