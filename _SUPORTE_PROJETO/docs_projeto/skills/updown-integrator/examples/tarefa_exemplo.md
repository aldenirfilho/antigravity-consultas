# Exemplo de tarefa — updown-integrator

## Cenário
Novo arquivo detectado:
- `00_INBOX_ATUALIZACAO/03_Conteudos_UpDown_MD/insuficiencia-respiratoria-aguda.md`

## Execução sugerida
1. Validar conteúdo e remover qualquer trecho interno/privado.
2. Publicar em `updown/insuficiencia-respiratoria-aguda.md` (e espelho em `public_site/updown/` se necessário no fluxo atual).
3. Criar card no manifesto UpDown com base no template.
4. Conectar com:
   - Biblioteca (protocolos de VM e oxigenoterapia).
   - Imagens (fluxograma de suporte ventilatório).
   - Questões (simulado TEMI respiratório).
5. Preservar rota antiga via `legacy_routes`, caso tenha mudado nome/caminho.
6. Validar links antes de fechar.

## Critérios de aceite
- Card criado e navegável.
- Links sem erro 404.
- Sem prompts internos publicados.
- Sem conteúdo proprietário copiado indevidamente.
