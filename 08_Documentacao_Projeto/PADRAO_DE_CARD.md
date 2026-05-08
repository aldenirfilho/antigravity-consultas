# Padrão de Card Visual — Card Feed Médico

## Todo card deve ter

```json
{
  "id": "slug-unico",
  "title": "Título didático do card",
  "theme": "id-do-tema",
  "tags": ["tag1", "tag2", "TEMI", "UTI"],
  "explanation": "Resumo clínico curto: para que serve o card, quando revisar e alerta principal.",
  "source": "ChatGPT + curadoria médica do Dr. Aldenir Rocha",
  "status": "novo",
  "imageUrl": "assets/cards/TEMA/NOME_DO_ARQUIVO.png",
  "createdAt": "2026-05-08",
  "related": ["Tema relacionado 1", "Tema relacionado 2"]
}
```

## Status de card

- `novo`
- `em-revisao`
- `favorito`
- `pendente-imagem`
- `revisar`
- `arquivado`

## Nome de arquivo recomendado

```text
tema_subtema_descricao_1080x1920.png
```

Exemplo:

```text
nefro_aki_kdigo_uti_10_passos_1080x1920.png
```
