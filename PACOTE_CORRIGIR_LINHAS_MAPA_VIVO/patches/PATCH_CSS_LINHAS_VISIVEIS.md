# Patch CSS — Linhas visíveis no Mapa Vivo

Adicionar ao final de:

`assets/css/graph-vivo.css`

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

#graph line {
  opacity: 0.9 !important;
}
```

## Se existir regra global

Trocar:

```css
line {
  stroke-dasharray: 4;
  animation: dash 20s linear infinite;
  opacity: 0.4;
}
```

Por:

```css
#graph line {
  stroke-dasharray: 4;
  animation: dash 20s linear infinite;
  opacity: 0.9;
}
```
