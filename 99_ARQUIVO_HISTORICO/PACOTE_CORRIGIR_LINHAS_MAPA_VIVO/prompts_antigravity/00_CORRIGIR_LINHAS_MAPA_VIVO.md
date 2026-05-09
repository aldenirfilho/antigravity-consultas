# SUPERCOMANDO — Corrigir linhas de conexão invisíveis do Mapa Vivo

Repositório: `aldenirfilho/antigravity-consultas`

Página alvo:

`https://aldenirfilho.github.io/antigravity-consultas/#mapa`

## Problema

As linhas de conexão do Mapa Vivo estão praticamente invisíveis.

## Causa provável

No arquivo:

`assets/js/graph.js`

as conexões estão sendo criadas com:

```js
.attr("stroke", "rgba(255,255,255,0.06)")
.attr("stroke-width", 1)
```

Esse contraste é baixo demais no fundo escuro.

Além disso, no CSS:

`assets/css/graph-vivo.css`

há regra genérica para `line` com `opacity: 0.4`, deixando as linhas ainda mais apagadas.

---

# Tarefa 1 — Corrigir `assets/js/graph.js`

Localizar o bloco das conexões:

```js
const link = g.append("g")
  .attr("stroke", "rgba(255,255,255,0.06)")
  .attr("stroke-width", 1)
  .selectAll("line")
  .data(validLinks)
  .join("line");
```

Substituir por:

```js
const link = g.append("g")
  .attr("class", "graph-links")
  .selectAll("line")
  .data(validLinks)
  .join("line")
  .attr("class", "graph-link")
  .attr("stroke", d => getLinkColor(d))
  .attr("stroke-width", d => getLinkWidth(d))
  .attr("stroke-opacity", 0.82);
```

Adicionar antes do final da função `render` ou próximo de `getNodeColor`:

```js
function getLinkColor(d) {
  const relation = d.relation || "";
  if (relation.includes("subtema")) return "rgba(62,232,255,0.70)";
  if (relation.includes("gera")) return "rgba(255,209,102,0.72)";
  if (relation.includes("alimenta")) return "rgba(78,240,161,0.70)";
  if (relation.includes("apoia")) return "rgba(169,140,255,0.72)";
  return "rgba(62,232,255,0.62)";
}

function getLinkWidth(d) {
  const relation = d.relation || "";
  if (relation.includes("subtema")) return 2.2;
  if (relation.includes("gera")) return 2.4;
  if (relation.includes("alimenta")) return 2.4;
  return 1.8;
}
```

## Observação importante

Se o `validLinks` estiver sendo criado assim:

```js
.map(e => ({ source: e.from, target: e.to }))
```

trocar para preservar a relação:

```js
.map(e => ({ source: e.from, target: e.to, relation: e.relation || "conecta" }))
```

---

# Tarefa 2 — Corrigir `assets/css/graph-vivo.css`

Adicionar ao final do arquivo:

```css
/* Correção — linhas visíveis do Mapa Vivo */
.graph-links line,
.graph-link,
#graph svg line {
  stroke-opacity: 0.82 !important;
  stroke-width: 2px;
  filter: drop-shadow(0 0 7px rgba(62,232,255,.30));
}

.graph-link {
  stroke-linecap: round;
}

#graph svg line:hover {
  stroke-opacity: 1 !important;
  stroke-width: 3px !important;
}

/* Evita que regra genérica apague as linhas */
#graph line {
  opacity: 0.9 !important;
}
```

Se existir uma regra global assim:

```css
line {
  opacity: 0.4;
}
```

trocar para:

```css
#graph line {
  opacity: 0.9;
}
```

Evitar regra global `line`, pois pode afetar outros SVGs.

---

# Tarefa 3 — Conferir se existem edges válidas

Validar:

`data/connections.json`

Checar se cada edge tem:

```json
{
  "from": "id-existente",
  "to": "id-existente",
  "relation": "tipo-de-conexao"
}
```

Se o edge não tiver `relation`, adicionar:

```json
"relation": "conecta"
```

---

# Tarefa 4 — Testar

1. Abrir a home.
2. Ir para `#mapa`.
3. Ver se as linhas aparecem.
4. Clicar em zoom +.
5. Testar no modo escuro.
6. Testar mobile.
7. Conferir console sem erro.

---

# Tarefa 5 — Relatório

Criar:

`08_Documentacao_Projeto/RELATORIO_CORRECAO_LINHAS_MAPA_VIVO.md`

Com:

- arquivo alterado;
- antes/depois do stroke;
- se as linhas ficaram visíveis;
- pendências.
