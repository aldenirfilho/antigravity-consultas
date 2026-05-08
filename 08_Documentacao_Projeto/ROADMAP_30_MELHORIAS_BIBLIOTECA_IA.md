# Roadmap — 30 melhorias futuras para a Biblioteca IA

**Data:** 2026-05-08

| Nº | Sugestão | Categoria | Prioridade | Descrição |
|---:|---|---|---|---|
| 1 | Dashboard de status da Biblioteca IA | Interface | alta | Criar painel com total de arquivos, catalogados, revisar, duplicados, temas dominantes e produção semanal. |
| 2 | Detecção automática de duplicados | Qualidade | alta | Comparar nomes, tamanhos e títulos para marcar duplicados prováveis antes da curadoria manual. |
| 3 | Fila de revisão por lote | Workflow | alta | Criar interface para revisar 20 arquivos por vez com barra de progresso e salvamento incremental. |
| 4 | Gerador de cards a partir de documentos | Card Feed | alta | Todo arquivo de alto rendimento deve poder gerar 1–5 cards para o Card Feed Médico. |
| 5 | Gerador de questões TEMI por documento | TEMI | alta | Documentos classificados como TEMI/alta relevância geram questões comentadas em JSON. |
| 6 | Mapa cerebral visual da Biblioteca | Grafo | alta | Renderizar conexões entre arquivos, temas, módulos, Banco TEMI, Card Feed e Calculadoras. |
| 7 | Página individual para cada arquivo | Navegação | média | Cada item catalogado pode ganhar uma página com resumo, tags, conexões e links. |
| 8 | Busca semântica local | Busca | média | Adicionar busca por tags, sinônimos e palavras-chave clínicas. |
| 9 | Ranking de alto rendimento TEMI | TEMI | alta | Pontuar documentos por relevância para prova, frequência em UTI e potencial de questão. |
| 10 | Botão “Gerar protocolo” | Produtividade | média | A partir de um documento, gerar prompt para criar protocolo institucional. |
| 11 | Botão “Gerar wallpaper 1080x1920” | Card Feed | média | Transformar resumo de documento em briefing para imagem vertical. |
| 12 | Integração com data/topics.json | Grafo | alta | Todo tema da Biblioteca deve poder aparecer no mapa vivo da home. |
| 13 | Normalização de nomes de arquivos | Organização | alta | Renomear usando padrão tema_subtema_titulo_ano.ext sem acentos. |
| 14 | Sistema de versão editorial | Governança | média | Marcar v1, v2, revisado, obsoleto, substituído, precisa atualização. |
| 15 | Controle de validade científica | Segurança | alta | Campo para ano, diretriz-fonte, necessidade de atualização e alerta de evidência antiga. |
| 16 | Conector Biblioteca → Calculadoras | Ferramentas | média | Arquivos com dose/cálculo alimentam backlog da Central de Calculadoras UTI. |
| 17 | Conector Biblioteca → Módulos Clínicos | Módulos | alta | Arquivos críticos alimentam módulos como Sepse, VM/SDRA, AKI/TRS e Neuro UTI. |
| 18 | Conector Biblioteca → Banco TEMI | TEMI | alta | Arquivos de prova geram questões e flashcards conectados ao tema. |
| 19 | Conector Biblioteca → Card Feed | Card Feed | alta | Documentos visuais ou algoritmos geram cards para revisão rápida. |
| 20 | Modo plantão | Interface | média | Filtro para exibir apenas documentos acionáveis à beira-leito. |
| 21 | Modo estudo TEMI | TEMI | média | Filtro para documentos com questões, flashcards e provas. |
| 22 | Modo revisão semanal | Workflow | média | Lista automática do que revisar, atualizar ou transformar em card. |
| 23 | Sistema de badges | Gamificação | baixa | Badges por tema: Vent Master, Sepsis Slayer, Nefro AKI, Neuro ICU. |
| 24 | Gerador de resumos em 3 níveis | Síntese | média | Resumo rápido, resumo plantão, resumo TEMI para cada arquivo. |
| 25 | Checklist de segurança por tema | Segurança | alta | Cada documento crítico deve ter campo de riscos, contraindicações e dupla checagem. |
| 26 | Índice por síndromes | Navegação | média | Classificar também por síndrome: choque, dispneia, coma, IRA, acidose, sangramento. |
| 27 | Índice por cenário | Navegação | média | UTI, PS, enfermaria, ambulatório, pré-prova, discussão de caso. |
| 28 | Exportação para Obsidian | Obsidian | média | Gerar Markdown com frontmatter para importar no vault. |
| 29 | Pacote de atualização mensal | Governança | média | Rotina para revisar novos arquivos, obsoletos e temas prioritários. |
| 30 | Score de utilidade clínica | Priorização | alta | Score 0–10 por impacto em plantão, risco clínico, frequência e utilidade TEMI. |

## Como priorizar

### Fazer primeiro
- Dashboard de status.
- Duplicados.
- Cards de alto rendimento.
- Questões TEMI.
- Conexão com módulos clínicos.
- Validação de segurança.

### Fazer depois
- Página individual por arquivo.
- Busca semântica.
- Exportação Obsidian.
- Sistema de badges.
- Modo revisão semanal.
