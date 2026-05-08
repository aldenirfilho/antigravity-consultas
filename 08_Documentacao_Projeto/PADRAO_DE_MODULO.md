# Padrão de Módulo Clínico

## Estrutura mínima

Cada novo módulo clínico deve conter:

1. Hero com título, objetivo e botões principais.
2. Breadcrumb para voltar à home.
3. Resumo executivo.
4. Fisiopatologia essencial.
5. Diagnóstico e critérios.
6. Conduta inicial.
7. Manejo em UTI.
8. Complicações.
9. Prescrição/doses quando aplicável.
10. Checklist beira-leito.
11. Pontos TEMI.
12. Cards/wallpapers relacionados.
13. Questões relacionadas.
14. Referências.
15. Links para temas correlatos.

## Campos no catálogo

```json
{
  "id": "slug-do-modulo",
  "title": "Título",
  "path": "caminho/relativo.html",
  "status": "ativo",
  "type": "hub clínico",
  "theme": "tema-principal",
  "caption": "Legenda curta",
  "related": ["tema-1", "tema-2"]
}
```
