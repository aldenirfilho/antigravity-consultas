# 02 — Gerar cards de alto rendimento a partir da Biblioteca IA

## Objetivo

Identificar documentos de alto rendimento e gerar candidatos a cards para o Card Feed Médico.

## Ler

- `05_Biblioteca_IA/data/biblioteca_catalogo.json`
- `06_Card_Feed_Medico/data/cards.json`
- `06_Card_Feed_Medico/data/themes.json`

## Critérios de alto rendimento

Selecionar arquivos com:

- `priority: "alta-uti"`
- `priority: "temi"`
- tags contendo `UTI`, `TEMI`, `plantão`, `protocolo`, `algoritmo`, `dose`, `emergência`
- clinicalUse preenchido
- safetyNotes relevante
- temas: sepse, choque, VM/SDRA, AKI/TRS, infectologia, neuro UTI, endocrino/metabólico

## Saídas

Criar:

`05_Biblioteca_IA/data/biblioteca_card_candidates.json`

e:

`06_Card_Feed_Medico/data/cards_patch_biblioteca.json`

## Modelo de card

```json
{
  "id": "biblioteca-card-slug",
  "title": "Título do card",
  "theme": "tema-card-feed",
  "tags": ["UTI", "TEMI"],
  "explanation": "Resumo de uso rápido.",
  "source": "Biblioteca IA + curadoria Dr. Aldenir Rocha",
  "status": "candidato",
  "imageUrl": "",
  "createdAt": "2026-05-08",
  "related": ["arquivo-origem", "tema"]
}
```

## Regra

Não criar imagem ainda. Gerar apenas candidatos e prompts de imagem quando aplicável.
