/**
 * MAPA VIVO 4.5 PRO — ANTIGRAVITY ENGINE
 * Estável, Filtrável e Responsivo.
 */

const MAP_CONFIG = {
  HEIGHT: 760,
  FORCE: -2000,
  DISTANCE: 180,
  COLLISION: 90,
  MODES: {
    CORE: ['hub', 'biblioteca', 'feed', 'qbank', 'tool'],
    CLINICAL: ['hub', 'module', 'topic', 'theme'],
    FILES: ['hub', 'biblioteca', 'file'],
    ALL: ['hub', 'biblioteca', 'feed', 'qbank', 'tool', 'module', 'topic', 'theme', 'file']
  }
};

let currentMode = 'CORE';
let fullData = { nodes: [], edges: [] };
let simulation, svg, g, zoom;

async function initGraph() {
  const container = document.getElementById('graph');
  if (!container) return;

  container.innerHTML = '<div style="padding:40px; color:#64748b; font-family:Syne;">🧠 Conectando neurais...</div>';

  if (typeof d3 === 'undefined') {
    renderFallback(container, "D3.js não carregado.");
    return;
  }

  try {
    const res = await fetch('data/connections.json?t=' + Date.now());
    if (!res.ok) throw new Error("Erro ao ler conexões.");
    fullData = await res.json();
    
    // Normalizar Dados
    fullData.nodes.forEach(n => {
      n.label = n.label || n.title || n.id;
      n.type = n.type || "theme";
      n.status = n.status || "ativo";
      n.body = n.body || n.description || "Tópico da Enciclopédia.";
      
      // Coordenadas Fallback se necessário
      if (n.x === undefined) n.x = Math.random() * 800;
      if (n.y === undefined) n.y = Math.random() * 600;
    });

    renderInterface(container);
    updateGraph();
  } catch (err) {
    renderFallback(container, err.message);
  }
}

function renderInterface(container) {
  const width = container.clientWidth || 1000;
  
  container.innerHTML = `
    <div class="graph-toolbar">
      <input type="text" class="graph-search" placeholder="🔍 Buscar tema ou arquivo..." oninput="searchNode(this.value)">
      <div class="graph-actions">
        <button class="btn primary" onclick="setMode('CORE')">🧠 Núcleo</button>
        <button class="btn primary" onclick="setMode('CLINICAL')">🏥 Clínico</button>
        <button class="btn primary" onclick="setMode('FILES')">📄 Arquivos</button>
        <button class="btn ghost" onclick="setMode('ALL')">🌐 Tudo</button>
      </div>
      <div class="graph-actions">
        <button class="btn ghost" onclick="zoomIn()">➕</button>
        <button class="btn ghost" onclick="zoomOut()">➖</button>
        <button class="btn ghost" onclick="resetZoom()">🔄 Reset</button>
      </div>
    </div>
    <div id="graph-canvas-wrap" style="width:100%; height:${MAP_CONFIG.HEIGHT}px"></div>
  `;

  svg = d3.select("#graph-canvas-wrap")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("viewBox", `0 0 ${width} ${MAP_CONFIG.HEIGHT}`);

  g = svg.append("g");

  zoom = d3.zoom()
    .scaleExtent([0.05, 5])
    .on("zoom", (event) => g.attr("transform", event.transform));

  svg.call(zoom);
}

function updateGraph() {
  const width = document.getElementById('graph-canvas-wrap').clientWidth || 1000;
  const height = MAP_CONFIG.HEIGHT;

  // Filtrar nós pelo modo
  const typesToMatch = MAP_CONFIG.MODES[currentMode];
  let filteredNodes = fullData.nodes.filter(n => typesToMatch.includes(n.type));
  
  // Limite de arquivos para não explodir a home
  if (currentMode === 'FILES') {
    filteredNodes = filteredNodes.slice(0, 30);
  }

  const nodeIds = new Set(filteredNodes.map(n => n.id));
  const filteredLinks = fullData.edges.filter(e => nodeIds.has(e.from) && nodeIds.has(e.to));

  // Limpar anterior
  g.selectAll("*").remove();

  // Links
  const link = g.append("g")
    .selectAll("line")
    .data(filteredLinks)
    .join("line")
    .attr("class", "graph-link");

  // Nodes
  const node = g.append("g")
    .selectAll(".node-group")
    .data(filteredNodes)
    .join("g")
    .attr("class", d => `node-group node-${d.type}`)
    .style("color", d => getNodeColor(d.type))
    .call(d3.drag()
      .on("start", dragStarted)
      .on("drag", dragged)
      .on("end", dragEnded))
    .on("click", (event, d) => showDrawer(d));

  // Card (Retângulo)
  node.append("rect")
    .attr("class", "node-card")
    .attr("rx", 12)
    .attr("ry", 12)
    .attr("x", d => -(d.label.length * 4 + 20))
    .attr("y", -18)
    .attr("width", d => d.label.length * 8 + 40)
    .attr("height", 36);

  // Label
  node.append("text")
    .attr("class", "node-label")
    .attr("text-anchor", "middle")
    .attr("dy", 5)
    .attr("font-size", "12px")
    .text(d => d.label);

  // Sub-label (ID ou tipo)
  node.append("text")
    .attr("class", "node-sub")
    .attr("text-anchor", "middle")
    .attr("dy", 26)
    .text(d => d.type.toUpperCase());

  // Simulação
  if (simulation) simulation.stop();
  simulation = d3.forceSimulation(filteredNodes)
    .force("link", d3.forceLink(filteredLinks).id(d => d.id).distance(MAP_CONFIG.DISTANCE))
    .force("charge", d3.forceManyBody().strength(MAP_CONFIG.FORCE))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(MAP_CONFIG.COLLISION));

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node
      .attr("transform", d => `translate(${d.x},${d.y})`);
  });
}

function showDrawer(d) {
  const drawer = document.getElementById('drawer');
  document.getElementById('drawerTitle').textContent = d.label;
  document.getElementById('drawerBody').innerHTML = `
    <p style="margin-bottom:1.5rem">${d.body}</p>
    <div class="drawer-meta">
      <span>TIPO: ${d.type.toUpperCase()}</span>
      <span>STATUS: ${d.status || 'ativo'}</span>
      <span>ID: ${d.id}</span>
    </div>
    <div class="drawer-actions">
      ${d.url && d.url !== '#' ? `<a href="${d.url}" class="btn primary" style="display:block;text-align:center">Abrir Conteúdo →</a>` : '<span class="muted">Conteúdo interno da Enciclopédia</span>'}
    </div>
  `;
  drawer.hidden = false;
  
  const close = document.getElementById('drawerClose');
  if (close) close.onclick = () => drawer.hidden = true;
}

function searchNode(val) {
  if (!val) {
    g.selectAll(".node-group").style("opacity", 1);
    return;
  }
  const term = val.toLowerCase();
  g.selectAll(".node-group").style("opacity", d => 
    d.label.toLowerCase().includes(term) || d.id.toLowerCase().includes(term) ? 1 : 0.1
  );
}

function setMode(mode) {
  currentMode = mode;
  updateGraph();
}

function zoomIn() { svg.transition().call(zoom.scaleBy, 1.4); }
function zoomOut() { svg.transition().call(zoom.scaleBy, 0.7); }
function resetZoom() { svg.transition().call(zoom.transform, d3.zoomIdentity); }

function getNodeColor(type) {
  const colors = { hub: "#ffad4d", biblioteca: "#00d4ff", feed: "#38bdf8", qbank: "#ffc107", tool: "#4ef0a1", module: "#7c3aed", theme: "#64748b", file: "#94a3b8" };
  return colors[type] || "#64748b";
}

function dragStarted(event, d) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x; d.fy = d.y;
}
function dragged(event, d) {
  d.fx = event.x; d.fy = event.y;
}
function dragEnded(event, d) {
  if (!event.active) simulation.alphaTarget(0);
  d.fx = null; d.fy = null;
}

function renderFallback(container, msg) {
  container.innerHTML = `
    <div class="graph-fallback">
      <h3>⚠️ Mapa Vivo: Modo de Segurança</h3>
      <p>${msg}</p>
      <div class="graph-fallback-grid">
        <a href="01_Modulos_Clinicos/AVC_Agudo/avc.html" class="card">🧠 AVC Agudo</a>
        <a href="05_Biblioteca_IA/index.html" class="card">📚 Biblioteca IA</a>
        <a href="02_Banco_Questoes_TEMI/index.html" class="card">🏆 Banco TEMI</a>
      </div>
    </div>
  `;
}

document.addEventListener('DOMContentLoaded', initGraph);
