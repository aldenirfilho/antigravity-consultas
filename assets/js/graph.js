/**
 * MAPA VIVO 6.0 — "TEXT BRAIN" (SEM BOLAS)
 * Foco absoluto em texto e conexões limpas.
 */

async function renderGraph() {
  const container = document.getElementById('graph');
  if (!container) return;

  container.style.height = "900px";
  const width = container.clientWidth || 1200;
  const height = 900;

  let nodes = [];
  let links = [];
  try {
    const res = await fetch('data/connections.json');
    const data = await res.json();
    nodes = data.nodes;
    links = data.edges.map(e => ({ source: e.from, target: e.to, relation: e.relation }));
  } catch (e) { return; }

  container.innerHTML = `
    <div id="graph-ui" style="position:absolute; top:20px; left:20px; z-index:100; display:flex; gap:10px;">
      <button class="btn primary" onclick="zoomIn()" style="padding:10px 15px; font-size:1.2rem;">➕ Aumentar Mapa</button>
      <button class="btn primary" onclick="zoomOut()" style="padding:10px 15px; font-size:1.2rem;">➖ Diminuir Mapa</button>
      <button class="btn ghost" onclick="resetZoom()">🔄 Resetar Vista</button>
    </div>
  `;

  const svg = d3.select("#graph")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%")
    .style("background", "#050d1a")
    .attr("viewBox", `0 0 ${width} ${height}`);

  const g = svg.append("g");

  // Zoom Handler
  const zoom = d3.zoom()
    .scaleExtent([0.05, 10])
    .on("zoom", (event) => g.attr("transform", event.transform));

  svg.call(zoom);

  window.zoomIn = () => svg.transition().duration(500).call(zoom.scaleBy, 1.5);
  window.zoomOut = () => svg.transition().duration(500).call(zoom.scaleBy, 0.7);
  window.resetZoom = () => svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);

  // Simulação de Força - Distância e Repulsão Máxima
  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(250))
    .force("charge", d3.forceManyBody().strength(-3000))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(120));

  // Linhas (Conexões)
  const link = g.append("g")
    .attr("stroke", "rgba(255,255,255,0.1)")
    .attr("stroke-width", 1)
    .selectAll("line")
    .data(links)
    .join("line");

  // Nós - APENAS TEXTO (Sem círculos, sem bolas)
  const node = g.append("g")
    .selectAll(".node-group")
    .data(nodes)
    .join("g")
    .attr("class", d => `node-group node-${d.type}`)
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended))
    .on("click", (event, d) => showDetails(d));

  // Rótulo de Texto (Único elemento visível)
  node.append("text")
    .attr("text-anchor", "middle")
    .attr("fill", d => getNodeColor(d.type))
    .attr("font-size", d => (d.type === 'hub' || d.type === 'module') ? "18px" : "14px")
    .attr("font-weight", "800")
    .attr("cursor", "pointer")
    .style("text-shadow", "0 0 10px rgba(0,0,0,1), 0 0 5px rgba(255,255,255,0.2)")
    .text(d => d.label);

  simulation.on("tick", () => {
    link.attr("x1", d => d.source.x).attr("y1", d => d.source.y).attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    node.attr("transform", d => `translate(${d.x},${d.y})`);
  });

  function getNodeColor(type) {
    const colors = { hub: "#ffad4d", biblioteca: "#00d4ff", feed: "#38bdf8", qbank: "#ffc107", tool: "#4ef0a1", module: "#7c3aed", theme: "#a78bfa", file: "#94a3b8" };
    return colors[type] || "#fff";
  }

  function showDetails(d) {
    const drawer = document.getElementById('drawer');
    document.getElementById('drawerTitle').textContent = d.label;
    document.getElementById('drawerBody').innerHTML = `
      <p>${d.body || d.description || 'Conexão cerebral ativa.'}</p>
      <div class="drawer-meta">
        <span>Tipo: ${d.type}</span>
        <span>Status: ${d.status || 'ativo'}</span>
      </div>
      ${d.url && d.url !== '#' ? `<a class="btn primary" href="${d.url}">Abrir Módulo →</a>` : '<span class="btn ghost">Material em revisão</span>'}
    `;
    drawer.hidden = false;
  }

  function dragstarted(event) { if (!event.active) simulation.alphaTarget(0.3).restart(); event.subject.fx = event.subject.x; event.subject.fy = event.subject.y; }
  function dragged(event) { event.subject.fx = event.x; event.subject.fy = event.y; }
  function dragended(event) { if (!event.active) simulation.alphaTarget(0); event.subject.fx = null; event.subject.fy = null; }
}

renderGraph();
