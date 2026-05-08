# Plano técnico — Correção do Mapa Vivo

## Falhas prioritárias

1. Drawer `hidden` sendo forçado a aparecer.
2. Mapa só com texto, sem cards/nós visuais.
3. Ausência de filtros para muitos arquivos.
4. Falta de fallback quando D3 ou JSON falha.
5. Arestas pouco visíveis.
6. Risco de crash se algum node vier sem `type`.

## Melhorias desejadas

- Toolbar.
- Busca.
- Filtros.
- Cards SVG.
- Drawer com conexões.
- Fallback HTML.
- Mobile melhor.
- Validação de dados.

## Ordem segura

1. Backup.
2. CSS drawer.
3. Validação de JSON.
4. Refatoração do JS.
5. Teste local.
6. Publicação.
7. Relatório.
