const fallbackNodes = [
  { id: 'home', label: '🏠 Portal', x: 50, y: 50, type: 'hub' },
  { id: 'biblioteca-ia', label: '📚 Biblioteca', x: 20, y: 30, type: 'biblioteca' },
  { id: 'card-feed-medico', label: '🖼️ Feed', x: 80, y: 30, type: 'feed' },
  { id: 'banco-temi', label: '🏆 TEMI', x: 30, y: 70, type: 'qbank' },
  { id: 'calculadoras-uti', label: '🧮 Calculadoras', x: 70, y: 70, type: 'tool' },
  { id: 'avc-agudo', label: '🧠 AVC Agudo', x: 50, y: 80, type: 'module' }
];

const fallbackEdges = [
  { from: 'home', to: 'biblioteca-ia' },
  { from: 'home', to: 'card-feed-medico' },
  { from: 'home', to: 'banco-temi' },
  { from: 'home', to: 'calculadoras-uti' },
  { from: 'home', to: 'avc-agudo' }
];

async function renderGraph() {
  const container = document.getElementById('graph');
  if (!container) return;

  // 1. Carregar dados
  let data = { nodes: fallbackNodes, edges: fallbackEdges };
  try {
    const res = await fetch('data/connections.json');
    if (res.ok) data = await res.json();
  } catch (e) { console.warn("Usando fallback para o mapa."); }

  // 2. Filtrar para não poluir a Home (Max 40 nós)
  // Mostramos Hubs, Módulos e os arquivos mais prioritários
  const priorityNodes = data.nodes.filter(n => 
    n.type !== 'file' || 
    (n.priority === 'alta' || n.priority === 'core' || n.status === 'ativo')
  ).slice(0, 45);
  
  const nodeIds = new Set(priorityNodes.map(n => n.id));
  const validEdges = data.edges.filter(e => nodeIds.has(e.from) && nodeIds.has(e.to));
  const nodeMap = new Map(priorityNodes.map(n => [n.id, n]));

  // 3. Preparar SVG
  container.innerHTML = `
    <svg id="graph-svg" width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice">
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="3" markerHeight="3" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="rgba(255,255,255,0.2)" />
        </marker>
      </defs>
      <g id="edges-group"></g>
      <g id="nodes-group"></g>
    </svg>
  `;

  const edgesGroup = document.getElementById('edges-group');
  const nodesGroup = document.getElementById('nodes-group');

  // 4. Renderizar Linhas (Edges)
  edgesGroup.innerHTML = validEdges.map(edge => {
    const from = nodeMap.get(edge.from);
    const to = nodeMap.get(edge.to);
    if (!from || !to) return '';
    return `<line x1="${from.x}" y1="${from.y}" x2="${to.x}" y2="${to.y}" stroke="rgba(255,255,255,0.1)" stroke-width="0.3" marker-end="url(#arrow)" />`;
  }).join('');

  // 5. Renderizar Nós (Nodes)
  nodesGroup.innerHTML = priorityNodes.map(node => {
    const color = getComputedStyle(document.documentElement).getPropertyValue(`--node-${node.type}`).trim() || '#64748b';
    const radius = (node.type === 'hub' ? 3 : (node.type === 'module' || node.type === 'biblioteca' ? 2.5 : 2));
    
    return `
      <g class="node-group" onclick="showNodeDetails('${node.id}')" style="cursor:pointer">
        <circle cx="${node.x}" cy="${node.y}" r="${radius}" fill="${color}" opacity="0.8">
          ${node.status === 'ativo' ? '<animate attributeName="r" values="'+radius+';'+(radius*1.3)+';'+radius+'" dur="3s" repeatCount="indefinite" />' : ''}
        </circle>
        <text x="${node.x}" y="${node.y + radius + 3}" text-anchor="middle" fill="rgba(255,255,255,0.6)" font-size="2" font-family="Syne">${node.label}</text>
      </g>
    `;
  }).join('');

  // 6. Detalhes (Drawer)
  window.showNodeDetails = (id) => {
    const node = nodeMap.get(id);
    if (!node) return;
    const drawer = document.getElementById('drawer');
    const title = document.getElementById('drawerTitle');
    const body = document.getElementById('drawerBody');
    
    title.textContent = node.label;
    body.innerHTML = `
      <p>${node.body || node.description || 'Nó de conexão clínica.'}</p>
      <div class="drawer-meta">
        <span>Tipo: ${node.type}</span>
        <span>Status: ${node.status || 'planejado'}</span>
      </div>
      ${node.url && node.url !== '#' ? `<a class="btn primary" href="${node.url}">Abrir Módulo →</a>` : '<span class="btn ghost">Em desenvolvimento</span>'}
    `;
    drawer.hidden = false;
  };

  const close = document.getElementById('drawerClose');
  if (close) close.onclick = () => document.getElementById('drawer').hidden = true;
}

// Iniciar
renderGraph();
