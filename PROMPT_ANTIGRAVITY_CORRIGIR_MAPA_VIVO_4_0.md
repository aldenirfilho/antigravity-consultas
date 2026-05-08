# PROMPT DIRETO PARA O ANTIGRAVITY — CORRIGIR MAPA VIVO 4.0

Você deve corrigir definitivamente o **Mapa Vivo** do projeto `antigravity-consultas`. O mapa está subutilizado e apresenta falhas de inclusão/exclusão/curadoria, linhas tracejadas pouco visíveis e comportamento instável. Aplique as correções abaixo como tarefa de engenharia, com backup e sem quebrar a homepage.

## 1. Objetivo final
Transformar o Mapa Vivo em um componente funcional de navegação + curadoria, com:
- inclusão real de itens;
- ocultação/exclusão segura;
- edição de itens;
- conexões diretas com linha contínua;
- conexões sugeridas com linha tracejada visível;
- persistência local imediata;
- exportação/importação de patch JSON;
- aplicação posterior do patch no `data/connections.json`;
- funcionamento em GitHub Pages, homepage e páginas internas.

## 2. Diagnóstico provável das falhas atuais
Corrija estes pontos obrigatoriamente:

### Falha A — Novo item entra, mas fica invisível
O modo padrão `core/núcleo` esconde tipos `theme` e `topic`. Assim, quando o usuário adiciona um tema clínico, ele pode ser criado em memória mas não aparece.

**Correção:**
- após adicionar novo nó, mudar automaticamente para modo `all`; OU
- garantir que o novo nó fique visível em qualquer modo por 10 segundos com classe `.is-new`; OU
- criar opção `showRecentlyAdded=true`.

Critério: ao adicionar `Lúpus na UTI`, ele deve aparecer imediatamente no mapa, sem o usuário trocar filtro.

### Falha B — Inclusão/exclusão não persiste
O sistema atual altera `state.nodes/state.edges`, mas após refresh perde alterações se o patch não for aplicado manualmente.

**Correção:**
Criar camada `localOverlay` persistida em `localStorage`, por exemplo:
- chave: `mapaVivo.overlay.v4`
- contém: `addedNodes`, `updatedNodes`, `hiddenNodeIds`, `addedEdges`, `updatedEdges`, `hiddenEdgeKeys`, `positions`, `rejectedSuggestions`.

No carregamento:
1. carregar `data/connections.json`;
2. normalizar;
3. aplicar overlay local;
4. renderizar.

Adicionar botões:
- `Salvar localmente`;
- `Exportar patch JSON`;
- `Importar patch JSON`;
- `Limpar alterações locais`;
- `Aplicar patch ao JSON` somente se estiver em ambiente local/dev ou por script separado.

Critério: se adicionar/ocultar item e der refresh, a alteração continua visível localmente.

### Falha C — Excluir item com campo vazio vira `node`
A função `slugify('')` retorna `node`, causando erro confuso.

**Correção:**
- criar `safeSlugify(text)` que retorna string vazia se input vazio;
- antes de ocultar, validar: se não houver ID digitado nem nó selecionado, mostrar mensagem clara: `Selecione um nó ou informe o ID`.

Critério: botão excluir nunca deve tentar ocultar `node` automaticamente.

### Falha D — Linha tracejada invisível/fraca
O mapa deve mostrar claramente:
- direta = linha contínua azul/ciano;
- sugerida = linha tracejada amarelo/laranja;
- rejeitada/oculta = não aparece.

**Correções CSS/SVG obrigatórias:**
- usar `path` em vez de `line` para links, permitindo curva leve e melhor visibilidade;
- classe `.edge--direct` e `.edge--suggested`;
- `stroke-dasharray: 10 7 !important` para sugeridas;
- `stroke-width: 3px` sugerida e `3.5px` direta;
- `vector-effect: non-scaling-stroke`;
- `pointer-events: stroke`;
- camada de links abaixo dos nós e labels acima;
- impedir CSS global de sobrescrever stroke usando seletor específico `#mapaVivoRoot .edge--suggested`.

Critério: com zoom normal, as tracejadas devem ser claramente visíveis.

### Falha E — Normalização estreita das conexões sugeridas
Hoje pode só reconhecer `strength === suggested`. Corrija para aceitar variações.

**Correção:**
Normalizar conexão como sugerida se qualquer campo indicar sugestão:
- `strength: suggested`;
- `status: sugerido`;
- `type: suggested`;
- `suggested: true`;
- `isSuggested: true`.

Normalizar direta se:
- `strength: direct`;
- `status: ativo` sem flag de sugestão.

Critério: qualquer conexão sugerida do JSON aparece tracejada.

### Falha F — Caminho do JSON quebrando em páginas internas
`DATA_URL = "data/connections.json"` quebra se o componente for usado dentro de subpastas.

**Correção:**
Criar resolução robusta:
1. usar atributo HTML: `<div id="mapaVivoRoot" data-graph-src="/antigravity-consultas/data/connections.json"></div>`;
2. fallback: `./data/connections.json`;
3. fallback: `../data/connections.json`;
4. fallback: `/antigravity-consultas/data/connections.json`.

Critério: mapa carrega na homepage e em páginas internas.

### Falha G — D3 via CDN pode não carregar
Se D3 falhar, o mapa não pode virar só uma mensagem inútil.

**Correção:**
- incluir `assets/vendor/d3.v7.min.js` local; OU
- manter CDN com fallback local;
- se D3 não carregar, renderizar lista navegável dos nós e links como fallback funcional.

Critério: sem internet/CDN, pelo menos uma lista clicável aparece.

### Falha H — Busca deixa mapa pobre
Ao buscar um termo, só aparecem nós cujo texto bate. Isso corta vizinhos e deixa mapa subutilizado.

**Correção:**
Quando buscar um nó, incluir também:
- vizinhos diretos;
- hub central;
- conexões entre eles;
- destacar match com classe `.is-match`.

Critério: busca por `sepse` mostra `sepse` + hub + temas relacionados.

### Falha I — Drag/posição não persiste
O usuário arrasta nós, mas ao re-renderizar perde layout.

**Correção:**
- salvar posições em `localStorage` no fim do drag;
- exportar posições dentro do patch;
- adicionar botão `Fixar layout` e `Resetar layout`.

Critério: se arrastar nó e atualizar página, ele permanece na posição.

### Falha J — Modo arquivos limita demais
`MAX_FILE_NODES = 18` subutiliza o mapa.

**Correção:**
- criar controle `Mostrar +20 arquivos`;
- criar agrupamento por tema/tag;
- permitir alternar `compacto`, `expandido`, `todos`.

Critério: usuário consegue expandir arquivos sem editar código.

## 3. Arquitetura solicitada
Refatorar em arquivos separados:

```txt
assets/js/mapa-vivo/
  mapa-vivo-core.js
  mapa-vivo-data.js
  mapa-vivo-render-d3.js
  mapa-vivo-admin.js
  mapa-vivo-overlay.js
  mapa-vivo-patch.js
assets/css/mapa-vivo.css
data/connections.json
scripts/apply_mapa_vivo_patch.py
scripts/validate_mapa_vivo.py
```

Se preferir manter um arquivo só por simplicidade, tudo bem, mas as funções devem ficar separadas internamente por blocos e com comentários.

## 4. Modelo de dados obrigatório
Cada nó deve suportar:

```json
{
  "id": "lupus-uti",
  "label": "🦋 Lúpus na UTI",
  "type": "theme",
  "status": "ativo",
  "body": "Abordagem clínica do lúpus em paciente crítico.",
  "url": "temas/lupus-uti/index.html",
  "tags": ["uti", "reumatologia", "nefrologia", "temi"],
  "visible": true,
  "x": 500,
  "y": 300
}
```

Cada conexão deve suportar:

```json
{
  "from": "lupus-uti",
  "to": "saaf-uti",
  "relation": "associacao-clinica",
  "strength": "suggested",
  "status": "sugerido",
  "visible": true,
  "reason": "Associação entre LES e SAAF em trombose/catástrofe antifosfolípide."
}
```

## 5. Funções obrigatórias
Implementar ou corrigir:

```js
loadGraphDataWithFallback()
normalizeNode(rawNode)
normalizeEdge(rawEdge)
applyLocalOverlay(baseGraph, overlay)
saveLocalOverlay(overlay)
addNode(node)
updateNode(id, patch)
hideNode(id, reason)
addEdge(edge)
hideEdge(from, to, reason)
approveSuggestedEdge(from, to)
rejectSuggestedEdge(from, to)
exportPatch()
importPatch(fileOrText)
applyPatchToGraph(baseGraph, patch)
saveNodePosition(id, x, y)
renderGraph()
renderFallbackList()
```

## 6. Interface obrigatória
Adicionar no painel de curadoria:

- Campo ID/slug;
- Campo título;
- Campo descrição;
- Campo URL;
- Campo tags;
- Tipo/status;
- Botão `Adicionar tema`;
- Botão `Atualizar selecionado`;
- Botão `Ocultar selecionado`;
- Botão `Conectar selecionado → outro ID`;
- Botão `Criar conexão sugerida tracejada`;
- Botão `Aprovar sugestão`;
- Botão `Rejeitar sugestão`;
- Botão `Salvar localmente`;
- Botão `Exportar patch JSON`;
- Botão `Importar patch JSON`;
- Botão `Limpar alterações locais`;
- Botão `Debug estado atual`.

## 7. Debug obrigatório
Adicionar painel de debug opcional mostrando:

```txt
Nós totais
Nós visíveis
Conexões totais
Conexões visíveis
Overlay local ativo: sim/não
Patch pendente: número de operações
Fonte do JSON carregado
D3 carregado: sim/não
Último erro
```

Adicionar `window.MapaVivoDebug` com:

```js
window.MapaVivoDebug = {
  getState,
  getOverlay,
  clearOverlay,
  exportPatch,
  forceModeAll,
  listHiddenNodes,
  listSuggestedEdges
}
```

## 8. Script para aplicar patch
Criar `scripts/apply_mapa_vivo_patch.py` que:
- recebe `data/connections.json` e um patch JSON;
- aplica `addNode`, `updateNode`, `hideNode`, `addEdge`, `hideEdge`, `approveSuggestedEdge`, `rejectSuggestedEdge`, `positionNode`;
- remove duplicidades;
- valida que toda edge aponta para nós existentes;
- salva backup antes de sobrescrever.

Comando esperado:

```bash
python scripts/apply_mapa_vivo_patch.py data/connections.json patches/meu_patch.json
```

## 9. Testes manuais obrigatórios
Depois de aplicar, teste exatamente:

1. Abrir homepage.
2. Ver se mapa carrega sem erro no console.
3. Adicionar nó:
   - id: `teste-mapa-vivo`
   - título: `🧪 Teste Mapa Vivo`
   - tipo: `theme`
   - tags: `teste,uti,temi`
4. Confirmar que aparece imediatamente.
5. Conectar `teste-mapa-vivo` ao `portal` como direta.
6. Confirmar linha contínua visível.
7. Conectar `teste-mapa-vivo` a outro nó como sugerida.
8. Confirmar linha tracejada visível.
9. Atualizar página.
10. Confirmar que o nó e conexões persistem via localStorage.
11. Ocultar o nó.
12. Atualizar página.
13. Confirmar que continua oculto.
14. Exportar patch.
15. Rodar validador.
16. Aplicar patch com script.
17. Limpar localStorage.
18. Reabrir página.
19. Confirmar que alterações continuam vindas do JSON final.

## 10. Critério de aceite final
Só considere concluído se:
- adicionar item aparece imediatamente;
- ocultar item funciona sem refresh e persiste após refresh;
- linha tracejada é visualmente óbvia;
- linha contínua é visualmente óbvia;
- busca mostra vizinhos;
- layout não reseta após arrastar;
- mapa funciona na homepage e subpáginas;
- fallback funcional aparece se D3 ou JSON falharem;
- patch exportado pode ser aplicado no JSON por script;
- console do navegador não mostra erro crítico.

## 11. Commit sugerido
Use branch:

```txt
fix/mapa-vivo-4-curadoria-persistente
```

Commit:

```txt
fix: tornar Mapa Vivo persistente, curável e robusto em GitHub Pages
```

PR description:

```md
Corrige o Mapa Vivo com curadoria funcional, persistência local, overlay, patch JSON, linhas tracejadas visíveis, fallback de D3/JSON, busca com vizinhos e layout persistente. Inclui scripts de validação e aplicação de patch.
```
