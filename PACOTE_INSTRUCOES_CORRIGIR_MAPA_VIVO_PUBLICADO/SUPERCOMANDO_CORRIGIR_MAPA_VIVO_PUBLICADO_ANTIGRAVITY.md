# SUPERCOMANDO — Corrigir falhas do Mapa Vivo publicado

Repositório: `aldenirfilho/antigravity-consultas`  
Página alvo: `https://aldenirfilho.github.io/antigravity-consultas/#mapa`

## Objetivo

Corrigir a seção `#mapa` para que o Mapa Vivo fique estável, legível, clicável, filtrável e responsivo, funcionando como cérebro visual da Enciclopédia Médica.

## Diagnóstico resumido

A página já carrega:

```html
<link rel="stylesheet" href="assets/css/graph-vivo.css" />
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="assets/js/graph.js"></script>
```

Mas o mapa ainda apresenta falhas prováveis:

1. Drawer vazio ou com comportamento estranho.
2. CSS antigo usa `#drawer[hidden] { display:block !important; }`, o que pode deixar o drawer “fantasma”.
3. JS renderiza apenas texto em SVG, dificultando clique e leitura.
4. CSS espera `.node-group`, mas versões anteriores do JS renderizavam `.node-text`.
5. Muitos nós do tipo `file` da Biblioteca IA podem poluir o grafo.
6. Falta filtro por modo: núcleo, clínico, arquivos, tudo.
7. Falta busca por nó/tema.
8. Falta fallback se D3 ou `connections.json` falharem.
9. Linhas de conexão estão muito discretas.
10. `d.type.toUpperCase()` pode quebrar se algum nó não tiver `type`.
11. Coordenadas `x/y` em porcentagem podem ser interpretadas como pixels pelo D3.
12. Mobile precisa de drawer e toolbar mais estáveis.

---

# Tarefa 1 — Backup obrigatório

Antes de alterar, criar backup lógico de:

- `index.html`
- `assets/js/graph.js`
- `assets/css/graph-vivo.css`
- `data/connections.json`

Registrar no relatório:

`08_Documentacao_Projeto/RELATORIO_CORRECAO_MAPA_VIVO_PUBLICADO.md`

---

# Tarefa 2 — Corrigir CSS do drawer e layout

Editar `assets/css/graph-vivo.css`.

## Trocar regra ruim

Remover qualquer regra assim:

```css
#drawer[hidden] {
  transform: translateX(120%);
  display: block !important;
}
```

## Substituir por

```css
#drawer[hidden] {
  display: none !important;
}
```

## Ajustar alvo de altura

Não aplicar `height:85vh` diretamente em `#mapa` se isso bagunçar a seção inteira.  
Preferir aplicar altura em `#graph`.

Adicionar/garantir:

```css
#mapa {
  position: relative;
  overflow: visible;
}

#graph {
  min-height: 760px;
  border-radius: 30px;
  position: relative;
  overflow: hidden;
}

#drawer {
  position: fixed;
  right: 18px;
  bottom: 18px;
  width: min(460px, calc(100vw - 36px));
  max-height: min(680px, calc(100vh - 36px));
  overflow: auto;
  z-index: 1000;
}
```

---

# Tarefa 3 — Refatorar `assets/js/graph.js`

Reescrever o mapa para:

## 3.1 Carregamento robusto

- Verificar se `d3` existe.
- Carregar `data/connections.json?t=Date.now()`.
- Validar `nodes` e `edges`.
- Ignorar edges órfãs.
- Se falhar, renderizar fallback HTML com cards simples.

## 3.2 Normalização dos dados

Para cada node:

```js
node.label = node.label || node.title || node.id;
node.type = node.type || "theme";
node.status = node.status || "";
node.body = node.body || node.description || "Tópico clínico da Enciclopédia.";
```

Converter coordenadas percentuais:

```js
if (typeof node.x === "number" && node.x >= 0 && node.x <= 100) node.x = (node.x / 100) * width;
if (typeof node.y === "number" && node.y >= 0 && node.y <= 100) node.y = (node.y / 100) * height;
```

## 3.3 Renderização visual

Parar de renderizar apenas `<text>`.  
Renderizar cada nó como `<g class="node-group node-TIPO">` contendo:

- `<rect class="node-card">`
- `<text class="node-label">`
- `<text class="node-sub">`

Tipos esperados:

- hub
- biblioteca
- feed
- qbank
- tool
- module
- topic
- theme
- file

## 3.4 Toolbar obrigatória

Criar toolbar dentro do `#graph` com:

- busca;
- modo `🧠 Núcleo`;
- modo `🏥 Clínico`;
- modo `📄 Arquivos`;
- modo `🌐 Tudo`;
- zoom +;
- zoom -;
- reset.

## 3.5 Filtro para arquivos

Modo padrão: `core`, ocultando `type: "file"`.

Modo arquivos:

- mostrar `biblioteca-ia`;
- mostrar `hub`;
- mostrar no máximo 18 arquivos inicialmente;
- se houver mais, informar que existem mais arquivos no catálogo da Biblioteca IA.

## 3.6 Drawer robusto

Ao clicar em nó, preencher:

- título;
- descrição;
- tipo;
- status;
- ID;
- lista de conexões;
- botão abrir conteúdo se `url && url !== "#"`.

Nunca usar `d.type.toUpperCase()` sem fallback. Usar:

```js
const type = d.type || "node";
```

## 3.7 Fallback

Se D3 ou JSON falhar, renderizar:

```html
<div class="graph-fallback">
  <h3>⚠️ Mapa Vivo em modo seguro</h3>
  <p>Erro encontrado...</p>
  <div class="graph-fallback-grid">cards dos principais nós</div>
</div>
```

---

# Tarefa 4 — Melhorar `data/connections.json`

Validar:

- todo nó tem `id`;
- todo nó tem `label`;
- todo nó tem `type`;
- todo nó tem `body`;
- todo edge tem `from`, `to`, `relation`;
- não há IDs duplicados;
- edges órfãs devem ser removidas ou ignoradas.

## Tipos recomendados

```json
{
  "hub": "Nó central do projeto",
  "biblioteca": "Biblioteca IA",
  "feed": "Card Feed",
  "qbank": "Banco TEMI",
  "tool": "Calculadoras",
  "module": "Módulo clínico",
  "topic": "Subtema",
  "theme": "Macrotema",
  "file": "Arquivo da Biblioteca"
}
```

## Relações recomendadas

- organiza
- alimenta
- gera-card
- gera-questao
- complementa-modulo
- subtema
- apoia-calculo
- revisao-visual
- alto-rendimento-temi

---

# Tarefa 5 — Conferir `index.html`

Confirmar no `<head>`:

```html
<link rel="stylesheet" href="assets/css/graph-vivo.css" />
<script src="https://d3js.org/d3.v7.min.js"></script>
```

Confirmar antes de `</body>`:

```html
<script src="assets/js/graph.js"></script>
```

Se o D3 estiver carregando no head, manter.

---

# Tarefa 6 — Melhorias visuais obrigatórias

No CSS, criar ou garantir classes:

```css
.graph-toolbar
.graph-search
.graph-actions
.graph-mode.active
.graph-canvas-wrap
.node-group
.node-card
.node-label
.node-sub
.graph-link
.graph-relation-label
.drawer-meta
.drawer-connections
.drawer-actions
.graph-fallback
.graph-fallback-grid
```

Arestas devem ser mais visíveis:

```css
.graph-link {
  stroke: rgba(62,232,255,.26);
  stroke-linecap: round;
}
```

---

# Tarefa 7 — Validação final

Testar no navegador:

1. Abrir home.
2. Ir para `#mapa`.
3. Confirmar que o loading aparece e desaparece.
4. Confirmar toolbar.
5. Confirmar nós como cards.
6. Confirmar linhas.
7. Clicar em `Portal`.
8. Clicar em `Biblioteca IA`.
9. Clicar em `AVC Agudo`.
10. Testar busca: `AVC`.
11. Testar busca: `VM`.
12. Testar modo `Arquivos`.
13. Testar modo `Tudo`.
14. Testar zoom e reset.
15. Testar mobile.
16. Ver console.
17. Ver Network para 404.
18. Validar drawer fechado sem aparecer texto fantasma.

---

# Tarefa 8 — Relatório

Criar:

`08_Documentacao_Projeto/RELATORIO_CORRECAO_MAPA_VIVO_PUBLICADO.md`

Com:

- data;
- arquivos modificados;
- bugs encontrados;
- bugs corrigidos;
- validação feita;
- pendências;
- decisão sobre arquivos `file` no mapa;
- próximos passos.

---

# Critério de sucesso

A seção `#mapa` deve funcionar como um mapa interativo legível, com filtros, busca, drawer funcional, fallback seguro e sem drawer fantasma.
