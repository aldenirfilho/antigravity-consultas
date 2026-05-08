# Patch mínimo no `index.html`

Use se a seção do mapa estiver incompleta.

## Head

```html
<link rel="stylesheet" href="assets/css/graph-vivo.css" />
<script src="https://d3js.org/d3.v7.min.js"></script>
```

## Seção do mapa

```html
<section id="mapa" class="section mapa-vivo-section">
  <div class="section-head">
    <p class="eyebrow">Mapa Vivo</p>
    <h2>🧠 Cérebro visual da Enciclopédia</h2>
    <p>Conecte módulos, arquivos, cards, questões TEMI e ferramentas clínicas.</p>
  </div>
  <div id="graph"></div>
</section>
```

## Antes de `</body>`

```html
<script src="assets/js/graph.js"></script>
```
