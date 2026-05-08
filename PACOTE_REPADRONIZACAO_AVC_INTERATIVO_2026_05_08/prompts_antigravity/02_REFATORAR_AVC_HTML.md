# 02 — Refatorar AVC HTML

Refatore:

`01_Modulos_Clinicos/AVC_Agudo/avc.html`

## Obrigatório

Adicionar no head:

```html
<link rel="stylesheet" href="../../assets/css/base.css" />
<link rel="stylesheet" href="avc-theme.css" />
```

Manter:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

por enquanto, pois `avc.js` ainda injeta classes Tailwind.

## Estrutura final esperada

```html
<body class="avc-page">
  <header class="topbar avc-topbar">...</header>

  <nav class="avc-breadcrumb">...</nav>

  <div id="overlay" class="avc-overlay hidden"></div>

  <div class="avc-layout">
    <aside id="sidebar" class="avc-sidebar">
      <nav>
        <p class="avc-sidebar-title">Navegação rápida</p>
        <ul id="sidebar-nav"></ul>
        <div class="avc-tip">...</div>
      </nav>
    </aside>

    <main class="avc-main">
      <section class="avc-hero glass">...</section>
      <section class="avc-actions-panel glass">...</section>
      <div id="dynamic-content" class="avc-dynamic-content"></div>
      <footer class="footer avc-footer">...</footer>
    </main>
  </div>

  scripts...
</body>
```

## Preservar IDs

- `menuBtn`
- `sidebar`
- `overlay`
- `sidebar-nav`
- `themeToggle`
- `dynamic-content`

## Botões obrigatórios

- Home
- Material Extenso
- Galeria
- Dashboard
- Banco TEMI
- Calculadoras UTI
- Card Feed

## Não remover scripts

- `db_fundamentos.js`
- `db_pratica.js`
- `db_interativo.js`
- `db_pesquisa.js`
- `db_cross_ia.js`
- `avc.js`
