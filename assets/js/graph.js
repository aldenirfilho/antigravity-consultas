/**
 * MAPA VIVO 7.0 — "ROBUST TEXT BRAIN"
 * Estabilidade total e foco em texto.
 */

function initGraph() {
  const container = document.getElementById('graph');
  if (!container) return;

  // Garantir altura mínima
  container.style.minHeight = "600px";
  container.style.height = "85vh"; // Altura dinâmica baseada na tela
  
  const width = container.clientWidth || 1200;
  const height = container.clientHeight || 800;

  container.innerHTML = `<div style="color:#fff; padding:20px; font-family:Syne;">🧠 Carregando conexões neurais...</div>`;

  if (typeof d3 === 'undefined') {
    container.innerHTML = `<div style="color:#ff4b4b; padding:20px;">⚠️ Erro: Biblioteca D3 não carregada. Verifique sua conexão ou o link no index.html.</div>`;
    return;
  }

  fetch('data/connections.json')
    .then(res => res.json())
    .then(data => {
      render(data, container, width, height);
    })
    .catch(err => {
      container.innerHTML = `<div style="color:#ff4b4b; padding:20px;">⚠️ Erro ao carregar conexões: ${err.message}</div>`;
    });
}

function render(data, container, width, height) {
  const nodes = data.nodes;
  const links = data.edges.map(e => ({ source: e.from, target: e.to, relation: e.relation }));

  container.innerHTML = `
    <div id="graph-ui" style="position:absolute; top:20px; left:20px; z-index:100; display:flex; gap:10px; pointer-events:none;">
      <button class="btn primary" onclick="g_zoomIn()" style="pointer-events:auto; font-size:14px; padding:8px 15px;">➕ Aumentar</button>
      <button class="btn primary" onclick="g_zoomOut()" style="pointer-events:auto; font-size:14px; padding:8px 15px;">➖ Diminuir</button>
      <button class="btn ghost" onclick="g_reset()" style="pointer-events:auto; font-size:14px; padding:8px 15px;">🔄 Reset</button>
    </div>
  `;

  const svg = d3.select(container)
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .style("background", "#050d1a");

  const g = svg.append("g");

  const zoom = d3.zoom()
    .scaleExtent([0.02, 10])
    .on("zoom", (event) => g.attr("transform", event.transform));

  svg.call(zoom);

  // Expor funções de zoom globalmente
  window.g_zoomIn = () => svg.transition().duration(500).call(zoom.scaleBy, 1.6);
  window.g_zoomOut = () => svg.transition().duration(500).call(zoom.scaleBy, 0.6);
  window.g_reset = () => svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);

  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(220))
    .force("charge", d3.forceManyBody().strength(-2500))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(100));

  const link = g.append("g")
    .attr("stroke", "rgba(255,255,255,0.1)")
    .selectAll("line")
    .data(links)
    .join("line");

  const node = g.append("g")
    .selectAll(".node-group")
    .data(nodes)
    .join("g")
    .attr("class", d => `node-group node-${d.type}`)
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
        <p>${d.body || d.description || 'Conexão ativa.'}</p>
        <div class="drawer-meta">
          <span>Tipo: ${d.type}</span>
          <span>ID: ${d.id}</span>
        </div>
        ${d.url && d.url !== '#' ? `<a class="btn primary" href="${d.url}">Abrir →</a>` : ''}
      `;
      drawer.hidden = false;
    });

  // TEXTO É O ÚNICO ELEMENTO (Fim das bolas!)
  node.append("text")
    .attr("text-anchor", "middle")
    .attr("fill", d => getNodeColor(d.type))
    .attr("font-size", d => (d.type === 'hub' || d.type === 'module') ? "22px" : "16px")
    .attr("font-weight", "800")
    .style("text-shadow", "0 2px 10px rgba(0,0,0,1)")
    .text(d => d.label);

  simulation.on("tick", () => {
    link.attr("x1", d => d.source.x).attr("y1", d => d.source.y).attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    node.attr("transform", d => `translate(${d.x},${d.y})`);
  });

  function getNodeColor(type) {
    const colors = { hub: "#ffad4d", biblioteca: "#00d4ff", feed: "#38bdf8", qbank: "#ffc107", tool: "#4ef0a1", module: "#7c3aed", theme: "#64748b", file: "#94a3b8" };
    return colors[type] || "#fff";
  }
}

// Inicializar quando o DOM e D3 estiverem prontos
document.addEventListener('DOMContentLoaded', () => {
  // Pequeno delay para garantir que d3 injetado no final do body seja lido
  setTimeout(initGraph, 500);
});
