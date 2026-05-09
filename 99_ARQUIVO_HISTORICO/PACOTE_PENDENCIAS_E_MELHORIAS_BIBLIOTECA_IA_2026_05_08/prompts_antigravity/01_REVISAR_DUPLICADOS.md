# 01 — Revisar duplicados da Biblioteca IA

## Objetivo

Detectar arquivos duplicados ou quase duplicados após a classificação do inbox.

## Ler

- `05_Biblioteca_IA/data/biblioteca_catalogo.json`
- `05_Biblioteca_IA/data/biblioteca_inbox_manifest_186.json`

## Critérios de duplicidade

Marcar como duplicado provável quando houver:

1. Mesmo nome original.
2. Mesmo título normalizado.
3. Mesmo tema + título muito semelhante.
4. Mesmo arquivo com extensão diferente.
5. Mesmo assunto e resumo quase igual.
6. Versões v1/v2 não identificadas.

## Saídas

Criar:

`05_Biblioteca_IA/data/biblioteca_duplicados.json`

Formato:

```json
{
  "updatedAt": "2026-05-08",
  "duplicates": [
    {
      "groupId": "dup-001",
      "confidence": "alta/media/baixa",
      "reason": "Mesmo título normalizado",
      "items": ["id-1", "id-2"],
      "recommendedAction": "manter-mais-recente | manter-ambos-com-versao | arquivar | revisar"
    }
  ]
}
```

Criar relatório:

`08_Documentacao_Projeto/RELATORIO_DUPLICADOS_BIBLIOTECA.md`

## Regra

Não apagar duplicados automaticamente. Apenas marcar e sugerir ação.
