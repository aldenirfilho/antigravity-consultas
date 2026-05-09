# Patch JS — Linhas visíveis no Mapa Vivo

No arquivo:

`assets/js/graph.js`

## 1. Preservar relation

Trocar:

```js
.map(e => ({ source: e.from, target: e.to }));
```

Por:

```js
.map(e => ({ source: e.from, target: e.to, relation: e.relation || "conecta" }));
```

## 2. Trocar criação das linhas

Trocar:

```js
const link = g.append("g")
  .attr("stroke", "rgba(255,255,255,0.06)")
  .attr("stroke-width", 1)
  .selectAll("line")
  .data(validLinks)
  .join("line");
```

Por:

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

## 3. Adicionar funções

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
