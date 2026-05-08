/**
 * MAPA VIVO 8.0 — "ULTIMATE TEXT BRAIN"
 * Estabilização Final e Foco Absoluto em Texto.
 */

const CONFIG = {
  HEIGHT: 800,
  FORCE_STRENGTH: -3000,
  LINK_DIST: 250,
  COLLIDE_RAD: 130
};

async function initGraph() {
  const container = document.getElementById('graph');
  if (!container) return;

  // Limpar e mostrar loading
  container.innerHTML = '<div id="graph-loading" style="color:#64748b; padding:40px; font-family:Syne; text-align:center;">🧠 Sincronizando Mapa Vivo...</div>';

  try {
    if (typeof d3 === 'undefined') throw new Error("D3.js não carregado.");

    const res = await fetch('data/connections.json');
    if (!res.ok) throw new Error("Não foi possível carregar data/connections.json");
    const data = await res.json();

    render(data, container);
  } catch (err) {
    container.innerHTML = `
      <div style="color:#ff4b4b; padding:40px; text-align:center; font-family:Syne;">
        <p>⚠️ Erro ao carregar o Mapa: ${err.message}</p>
        <button class="btn ghost" onclick="location.reload()" style="margin-top:20px">Tentar Novamente 🔄</button>
      </div>
    `;
  }
}

function render(data, container) {
  const width = container.clientWidth || 1000;
  const height = CONFIG.HEIGHT;

  // Remover loading
  container.innerHTML = `
    <div id="graph-ui" style="position:absolute; top:20px; left:20px; z-index:100; display:flex; gap:10px; pointer-events:none;">
      <button class="btn primary" onclick="gZoom(1.5)" style="pointer-events:auto; font-size:16px;">➕ Ampliar</button>
      <button class="btn primary" onclick="gZoom(0.6)" style="pointer-events:auto; font-size:16px;">➖ Reduzir</button>
      <button class="btn ghost" onclick="gReset()" style="pointer-events:auto; font-size:16px;">🔄 Reset</button>
    </div>
  `;

  const svg = d3.select(container)
    .append("svg")
    .attr("width", "100%")
    .attr("height", height)
    .attr("viewBox", `0 0 ${width} ${height}`)
    .style("background", "#050d1a");

  const g = svg.append("g");

  const zoom = d3.zoom()
    .scaleExtent([0.01, 10])
    .on("zoom", (event) => g.attr("transform", event.transform));

  svg.call(zoom);

  // Globais para os botões
  window.gZoom = (scale) => svg.transition().duration(500).call(zoom.scaleBy, scale);
  window.gReset = () => svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);

  // Validação de links (Fail-safe para não crashar se um nó sumir)
  const nodeIds = new Set(data.nodes.map(d => d.id));
  const validLinks = data.edges
    .filter(e => nodeIds.has(e.from) && nodeIds.has(e.to))
    .map(e => ({ source: e.from, target: e.to }));

  const simulation = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(validLinks).id(d => d.id).distance(CONFIG.LINK_DIST))
    .force("charge", d3.forceManyBody().strength(CONFIG.FORCE_STRENGTH))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(CONFIG.COLLIDE_RAD));

  // Conexões (Linhas finas)
  const link = g.append("g")
    .attr("stroke", "rgba(255,255,255,0.06)")
    .attr("stroke-width", 1)
    .selectAll("line")
    .data(validLinks)
    .join("line");

  // Rótulos (Apenas Texto - Sem Bolas!)
  const node = g.append("g")
    .selectAll(".node-text")
    .data(data.nodes)
    .join("text")
    .attr("class", "node-text")
    .attr("text-anchor", "middle")
    .attr("fill", d => getNodeColor(d.type))
    .attr("font-size", d => (d.type === 'hub' || d.type === 'module') ? "24px" : "16px")
    .attr("font-weight", "800")
    .attr("cursor", "pointer")
    .style("text-shadow", "0 0 10px #000")
    .text(d => d.label)
    .call(d3.drag()
      .on("start", (event, d) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x; d.fy = d.y;
      })
      .on("drag", (event, d) => {
        d.fx = event.x; d.fy = event.y;
      })
      .on("end", (event, d) => {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null; d.fy = null;
      }))
    .on("click", (event, d) => {
      const drawer = document.getElementById('drawer');
      document.getElementById('drawerTitle').textContent = d.label;
      document.getElementById('drawerBody').innerHTML = `
        <p>${d.body || d.description || 'Tópico clínico da Enciclopédia.'}</p>
        <div class="drawer-meta">
          <span>TIPO: ${d.type.toUpperCase()}</span>
          <span>ID: ${d.id}</span>
        </div>
        ${d.url && d.url !== '#' ? `<a class="btn primary" href="${d.url}">Abrir Conteúdo →</a>` : ''}
      `;
      drawer.hidden = false;
    });

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node
      .attr("x", d => d.x)
      .attr("y", d => d.y);
  });

  function getNodeColor(type) {
    const colors = { hub: "#ffad4d", biblioteca: "#00d4ff", feed: "#38bdf8", qbank: "#ffc107", tool: "#4ef0a1", module: "#7c3aed", theme: "#a78bfa", file: "#94a3b8" };
    return colors[type] || "#fff";
  }
}

// Iniciar após carregar tudo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initGraph);
} else {
  initGraph();
}
