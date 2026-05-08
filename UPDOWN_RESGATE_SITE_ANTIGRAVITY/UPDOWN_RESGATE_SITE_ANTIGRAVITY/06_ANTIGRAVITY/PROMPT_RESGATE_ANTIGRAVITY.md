# PROMPT DE RESGATE PARA ANTIGRAVITY

Você está corrigindo um site do projeto Enciclomedia/UpDown que perdeu acesso aos arquivos após uma reorganização de rotas.

## Objetivo principal

Restaurar a navegação e os links sem apagar arquivos existentes.

## Instruções obrigatórias

1. Não delete nenhum arquivo `.pdf`, `.docx`, `.md`, `.html`, `.zip`, `.png`, `.jpg`, `.webp`.
2. Não mova arquivos sem atualizar todos os links.
3. Crie uma camada de resgate com:
   - `/index.html`
   - `/updown/index.html`
   - `/biblioteca/index.html`
   - `/imagens/index.html`
   - `/apps/index.html`
4. Escaneie o repositório e gere uma lista de todos os arquivos em PDF, Word, Markdown, HTML e ZIP.
5. Recrie a Biblioteca com links diretos para esses arquivos.
6. Recrie a página UpDown com cards para os módulos #001, #002 e #003.
7. Preserve o triângulo:
   - UpDown ↔ Biblioteca ↔ Imagens.
8. Não exiba prompts privados, sugestões internas ou bastidores na página pública.
9. Se algum destino não existir, criar placeholder “em breve” sem quebrar a navegação.
10. Antes de finalizar, validar que todos os links internos apontam para arquivos existentes ou placeholders reais.

## Tarefa imediata

Use o arquivo `01_RESTAURAR_ROTAS/index_resgate.html` como base para reconstruir a home temporária. Depois gere índices públicos para Biblioteca, UpDown, Imagens e Apps usando os arquivos Markdown deste pacote.

## Critério de sucesso

O site deve permitir ao usuário acessar novamente:

- PDFs;
- Word;
- Markdown;
- HTML leitor;
- ZIPs;
- módulos UpDown;
- aplicações extras.
