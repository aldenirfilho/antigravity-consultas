# 🏗️ Arquitetura do Projeto

## Camadas

1. `index.html` — homepage pública e portal de navegação.
2. `temas/` — páginas clínicas principais.
3. `assets/` — CSS, JavaScript, imagens e ícones.
4. `data/` — JSONs para busca, navegação e grafo de conhecimento.
5. `components/` — blocos reutilizáveis em HTML.
6. `templates/` — modelos para novos temas.
7. `docs/` — documentação editorial, segurança e expansão.

## Fluxo de criação de tema

Material bruto → análise médica → Markdown estruturado → página HTML → JSON de metadados → conexões no grafo → revisão de segurança → publicação.

## Próxima evolução técnica

- Criar busca global.
- Renderizar cards dinamicamente a partir de `data/topics.json`.
- Renderizar grafo com SVG/Canvas.
- Criar modo escuro/claro.
- Criar modo plantão/mobile.
- Integrar atualização por IA no Antigravity.
