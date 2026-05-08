# Relatório — Correção das Linhas do Mapa Vivo

## Problema

As linhas de conexão estavam pouco visíveis no fundo escuro.

## Causa

- Stroke muito transparente.
- Espessura muito fina.
- CSS com opacidade baixa.
- Possível regra global `line` afetando o SVG.

## Arquivos alterados

- `assets/js/graph.js`
- `assets/css/graph-vivo.css`

## Validação

- [ ] Linhas aparecem.
- [ ] Linhas têm contraste adequado.
- [ ] Hover destaca linhas.
- [ ] Zoom mantém linhas visíveis.
- [ ] Mobile ok.
- [ ] Console sem erro.
