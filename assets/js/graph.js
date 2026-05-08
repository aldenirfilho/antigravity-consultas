/**
 * MAPA VIVO 4.0 — MOTOR D3.JS "BIG BRAIN"
 * Ultra-resolução, Zoom e Organização Espacial
 */

async function renderGraph() {
  const container = document.getElementById('graph');
  if (!container) return;

  const width = container.clientWidth || 1000;
  const height = 850; // Aumentado para mais espaço

  let nodes = [];
  let links = [];
  try {
    const res = await fetch('data/connections.json');
    const data = await res.json();
    nodes = data.nodes;
    links = data.edges.map(e => ({ source: e.from, target: e.to, relation: e.relation }));
  } catch (e) { return; }

  container.innerHTML = '';
  const svg = d3.select("#graph")
    .append("svg")
    .attr("width", "100%")
    .attr("height", height)
    .attr("viewBox", `0 0 ${width} ${height}`)
    .style("background", "#050d1a");

  const g = svg.append("g");

  // Configuração do Zoom
  const zoom = d3.zoom()
    .scaleExtent([0.1, 5])
    .on("zoom", (event) => g.attr("transform", event.transform));

  svg.call(zoom);

  // Simulação com Repulsão Forte (Evita sobreposição)
  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(150))
    .force("charge", d3.forceManyBody().strength(-1200)) // Repulsão muito maior
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(65)); // Raio de colisão maior

  // Linhas
  const link = g.append("g")
    .attr("stroke", "rgba(255,255,255,0.08)")
    .attr("stroke-width", 1.5)
    .selectAll("line")
    .data(links)
    .join("line");

  // Grupos de Nós
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

  // Ícones (Bolas Coloridas) — Tamanho Aumentado
  node.append("circle")
    .attr("r", d => (d.type === 'hub' || d.type === 'module') ? 35 : 22)
    .attr("fill", d => getNodeColor(d.type))
    .attr("stroke", "rgba(255,255,255,0.2)")
    .attr("stroke-width", 2);

  // Labels — Texto mais legível e centralizado
  node.append("text")
    .attr("dy", d => (d.type === 'hub' || d.type === 'module') ? 5 : 4)
    .attr("text-anchor", "middle")
    .attr("fill", "#fff")
    .attr("font-size", d => (d.type === 'hub' || d.type === 'module') ? "14px" : "11px")
    .attr("font-weight", "bold")
    .style("pointer-events", "none")
    .text(d => d.label.split(' ')[0]); // Emoji ou primeira palavra

  node.append("text")
    .attr("dy", d => (d.type === 'hub' || d.type === 'module') ? 55 : 42)
    .attr("text-anchor", "middle")
    .attr("fill", "rgba(255,255,255,0.8)")
    .attr("font-size", "12px")
    .style("pointer-events", "none")
    .text(d => d.label.substring(d.label.indexOf(' ') + 1)); // Resto do nome

  simulation.on("tick", () => {
    link.attr("x1", d => d.source.x).attr("y1", d => d.source.y).attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    node.attr("transform", d => `translate(${d.x},${d.y})`);
  });

  function getNodeColor(type) {
    const colors = { hub: "#ffad4d", biblioteca: "#00d4ff", feed: "#38bdf8", qbank: "#ffc107", tool: "#4ef0a1", module: "#7c3aed", theme: "#64748b", file: "#94a3b8" };
    return colors[type] || "#64748b";
  }

  function showDetails(d) {
    const drawer = document.getElementById('drawer');
    document.getElementById('drawerTitle').textContent = d.label;
    document.getElementById('drawerBody').innerHTML = `
      <p>${d.body || d.description || 'Conexão clínica ativa.'}</p>
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

window.addEventListener('resize', renderGraph);
renderGraph();
