/**
 * MAPA VIVO 3.0 — MOTOR D3.JS DYNAMIC BRAIN
 * Enciclopédia Médica Intensiva
 */

async function renderGraph() {
  const container = document.getElementById('graph');
  if (!container) return;

  // 1. Configurações de Dimensão
  const width = container.clientWidth || 800;
  const height = container.clientHeight || 500;

  // 2. Carregar Dados
  let nodes = [];
  let links = [];
  try {
    const res = await fetch('data/connections.json');
    const data = await res.json();
    nodes = data.nodes;
    links = data.edges.map(e => ({ source: e.from, target: e.to, relation: e.relation }));
  } catch (e) {
    console.error("Erro ao carregar mapa:", e);
    return;
  }

  // 3. Limpar container
  container.innerHTML = '';
  const svg = d3.select("#graph")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .call(d3.zoom().on("zoom", (event) => {
      g.attr("transform", event.transform);
    }))
    .append("g");

  const g = svg.append("g");

  // 4. Simulação de Força
  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(40));

  // 5. Desenhar Arestas (Links)
  const link = g.append("g")
    .attr("stroke", "rgba(255,255,255,0.1)")
    .attr("stroke-width", 1)
    .selectAll("line")
    .data(links)
    .join("line");

  // 6. Desenhar Nós
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

  // Círculo de fundo (Glow)
  node.append("circle")
    .attr("r", d => d.type === 'hub' ? 12 : 8)
    .attr("fill", d => getNodeColor(d.type))
    .attr("filter", "url(#glow)");

  // Label
  node.append("text")
    .attr("dy", 25)
    .attr("text-anchor", "middle")
    .attr("fill", "rgba(255,255,255,0.7)")
    .attr("font-size", "10px")
    .text(d => d.label);

  // 7. Atualização da Simulação
  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node
      .attr("transform", d => `translate(${d.x},${d.y})`);
  });

  // 8. Funções Auxiliares
  function getNodeColor(type) {
    const colors = {
      hub: "#ffad4d",
      biblioteca: "#00d4ff",
      feed: "#38bdf8",
      qbank: "#ffc107",
      tool: "#4ef0a1",
      module: "#7c3aed",
      theme: "#64748b",
      file: "#94a3b8"
    };
    return colors[type] || "#64748b";
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

  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }

  // Definição de Glow no SVG
  const defs = svg.append("defs");
  const filter = defs.append("filter").attr("id", "glow");
  filter.append("feGaussianBlur").attr("stdDeviation", "3").attr("result", "coloredBlur");
  const feMerge = filter.append("feMerge");
  feMerge.append("feMergeNode").attr("in", "coloredBlur");
  feMerge.append("feMergeNode").attr("in", "SourceGraphic");
}

window.addEventListener('resize', renderGraph);
renderGraph();
