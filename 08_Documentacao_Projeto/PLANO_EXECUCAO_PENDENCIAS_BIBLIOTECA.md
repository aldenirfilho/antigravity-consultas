# Plano de Execução — Pendências Biblioteca IA

**Data:** 2026-05-08

## Pendências principais

| Nº | Pendência | Prioridade | Saída |
|---:|---|---|---|
| 1 | Revisar duplicados prováveis | Alta | `biblioteca_duplicados.json` |
| 2 | Transformar alto rendimento em cards | Alta | `cards_patch_biblioteca.json` |
| 3 | Transformar materiais TEMI em questões | Alta | `qbank_patch_biblioteca.js` |
| 4 | Conectar arquivos críticos aos módulos | Alta | patches de topics/connections |
| 5 | Validar e publicar | Alta | relatório de validação |

## Fluxo recomendado

1. Rodar detecção de duplicados.
2. Resolver ou marcar duplicados como `revisar`.
3. Selecionar candidatos a cards.
4. Selecionar candidatos a questões TEMI.
5. Criar conexões cerebrais.
6. Validar tudo.
7. Publicar.
