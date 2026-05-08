const fallbackNodes = [
  { id: 'home', label: '🏠 Portal', body: 'Página-mãe da Enciclopédia.', x: 48, y: 8, type: 'hub', url: 'index.html' },
  { id: 'biblioteca-ia', label: '📚 Biblioteca IA', body: 'Repositório de documentos e curadoria IA.', x: 18, y: 24, type: 'biblioteca', url: '05_Biblioteca_IA/index.html' },
  { id: 'card-feed-medico', label: '🖼️ Card Feed', body: 'Feed visual de cards médicos.', x: 80, y: 24, type: 'feed', url: '06_Card_Feed_Medico/index.html' },
  { id: 'banco-temi', label: '🏆 Banco TEMI', body: 'Questões comentadas e simulação TEMI.', x: 34, y: 38, type: 'qbank', url: '02_Banco_Questoes_TEMI/index.html' },
  { id: 'calculadoras-uti', label: '🧮 Calculadoras UTI', body: 'Drogas, diluições, VM, eletrólitos e renal.', x: 64, y: 38, type: 'tool', url: '03_Calculadoras_UTI/index.html' },
  { id: 'avc-agudo', label: '🧠 AVC Agudo', body: 'Módulo ativo: emergência, reperfusão e neuroimagem.', x: 49, y: 54, type: 'module', url: '01_Modulos_Clinicos/AVC_Agudo/avc.html' }
];

const fallbackEdges = [
  { from: 'home', to: 'biblioteca-ia', relation: 'organiza' },
  { from: 'home', to: 'card-feed-medico', relation: 'revisão visual' },
  { from: 'home', to: 'banco-temi', relation: 'treino ativo' },
  { from: 'home', to: 'calculadoras-uti', relation: 'ferramentas' },
  { from: 'home', to: 'avc-agudo', relation: 'módulo ativo' },
  { from: 'biblioteca-ia', to: 'banco-temi', relation: 'gera questões' },
  { from: 'biblioteca-ia', to: 'card-feed-medico', relation: 'gera cards' }
];

function graphNodeClass(type = '') {
  const map = {
    hub: 'node-hub',
    biblioteca: 'node-library',
    feed: 'node-feed',
    qbank: 'node-qbank',
    tool: 'node-tool',
    module: 'node-module',
    topic: 'node-topic',
    theme: 'node-theme'
  };
  return map[type] || 'node-theme';
}

function makeLine(edge, fromNode, toNode) {
  const dx = toNode.x - fromNode.x;
  const dy = toNode.y - fromNode.y;
  const length = Math.sqrt(dx * dx + dy * dy);
  const angle = Math.atan2(dy, dx) * 180 / Math.PI;
  const midX = fromNode.x;
  const midY = fromNode.y;

  return `
    <div class="edge" style="left:${midX}%; top:${midY}%; width:${length}%; transform:rotate(${angle}deg);" title="${edge.relation || ''}"></div>
  `;
}

async function renderGraph() {
  const graph = document.getElementById('graph');
  if (!graph) return;

  const data = await loadJSON('data/connections.json', { nodes: fallbackNodes, edges: fallbackEdges });
  const nodes = data.nodes || [];
  const edges = data.edges || [];
  const nodeMap = new Map(nodes.map(node => [node.id, node]));

  const edgeHTML = edges.map(edge => {
    const fromNode = nodeMap.get(edge.from);
    const toNode = nodeMap.get(edge.to);
    if (!fromNode || !toNode) return '';
    return makeLine(edge, fromNode, toNode);
  }).join('');

  const nodeHTML = nodes.map(node => `
    <button
      class="node ${graphNodeClass(node.type)}"
      style="left:${node.x}%; top:${node.y}%;"
      data-id="${node.id}"
      data-title="${node.label}"
      data-body="${node.body || node.description || ''}"
      data-url="${node.url || ''}"
      data-status="${node.status || ''}"
      data-type="${node.type || ''}">
      <span>${node.label}</span>
      ${node.status ? `<small>${node.status}</small>` : ''}
    </button>
  `).join('');

  graph.innerHTML = `<div class="edge-layer">${edgeHTML}</div><div class="node-layer">${nodeHTML}</div>`;

  const drawer = document.getElementById('drawer');
  const title = document.getElementById('drawerTitle');
  const body = document.getElementById('drawerBody');
  const close = document.getElementById('drawerClose');

  graph.querySelectorAll('.node').forEach(node => {
    node.addEventListener('click', () => {
      const url = node.dataset.url;
      title.textContent = node.dataset.title;
      body.innerHTML = `
        <p>${node.dataset.body || ''}</p>
        <div class="drawer-meta">
          <span>Tipo: ${node.dataset.type || 'nó'}</span>
          ${node.dataset.status ? `<span>Status: ${node.dataset.status}</span>` : ''}
        </div>
        ${url && url !== '#' ? `<a class="btn primary" href="${url}">Abrir →</a>` : `<span class="btn ghost">Módulo planejado</span>`}
      `;
      drawer.hidden = false;
    });
  });

  if (close) close.addEventListener('click', () => drawer.hidden = true);
}

renderGraph();
