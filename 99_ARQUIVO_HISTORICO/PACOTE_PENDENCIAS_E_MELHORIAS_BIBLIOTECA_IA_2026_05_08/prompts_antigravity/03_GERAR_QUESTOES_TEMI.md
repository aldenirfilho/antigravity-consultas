# 03 — Gerar questões TEMI a partir da Biblioteca IA

## Objetivo

Transformar materiais classificados como TEMI ou alta relevância em candidatos a questões comentadas.

## Ler

- `05_Biblioteca_IA/data/biblioteca_catalogo.json`
- `02_Banco_Questoes_TEMI/data/hub_qbanks.js`

## Selecionar arquivos

Critérios:

- theme: `temi-prova`
- priority: `temi`
- tags contendo TEMI, AMIB, prova, UTI, protocolo, guideline, trial
- temas de alto rendimento: VM/SDRA, sepse/choque, AKI/TRS, neuro UTI, infectologia, endocrino/metabólico

## Saídas

Criar:

`05_Biblioteca_IA/data/biblioteca_temi_question_candidates.json`

e:

`02_Banco_Questoes_TEMI/data/qbank_patch_biblioteca.js`

## Modelo de questão

```json
{
  "id": "q-biblioteca-slug-001",
  "sourceFileId": "arquivo-origem",
  "theme": "vm-sdra",
  "difficulty": "facil|medio|hard|expert",
  "stem": "Enunciado clínico...",
  "alternatives": {
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "...",
    "E": "..."
  },
  "answer": "A",
  "commentary": "Comentário explicativo.",
  "temiPearl": "Pérola TEMI.",
  "tags": ["TEMI", "UTI"]
}
```

## Regra

Gerar candidatos. Não mesclar no banco principal sem revisão.
