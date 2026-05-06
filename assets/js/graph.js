const fallbackNodes = [
  { id: 'avc', label: '🧠 AVC Agudo', body: 'Hub inaugural do projeto.', x: 42, y: 38 },
  { id: 'trombolise', label: '💉 Trombólise', body: 'Janela, contraindicações, PA e sangramento.', x: 10, y: 18 },
  { id: 'trombectomia', label: '🧲 Trombectomia', body: 'OGV, angioTC, perfusão e regulação.', x: 68, y: 18 },
  { id: 'pa', label: '🎚️ PA no AVC', body: 'Metas pressóricas por cenário clínico.', x: 12, y: 65 },
  { id: 'fa', label: '❤️ FA', body: 'AVC cardioembólico e anticoagulação.', x: 72, y: 64 },
  { id: 'neuroimagem', label: '🖥️ Neuroimagem', body: 'TC, ASPECTS, angioTC e perfusão.', x: 34, y: 10 },
  { id: 'temi', label: '🏆 TEMI', body: 'Pegadinhas, questões e flashcards.', x: 44, y: 74 }
];

async function renderGraph() {
  const graph = document.getElementById('graph');
  if (!graph) return;
  const data = await loadJSON('data/connections.json', { nodes: fallbackNodes, edges: [] });
  graph.innerHTML = data.nodes.map(node => `
    <button class="node" style="left:${node.x}%; top:${node.y}%;" data-title="${node.label}" data-body="${node.body}">
      ${node.label}
    </button>
  `).join('');

  const drawer = document.getElementById('drawer');
  const title = document.getElementById('drawerTitle');
  const body = document.getElementById('drawerBody');
  const close = document.getElementById('drawerClose');

  graph.querySelectorAll('.node').forEach(node => {
    node.addEventListener('click', () => {
      title.textContent = node.dataset.title;
      body.textContent = node.dataset.body;
      drawer.hidden = false;
    });
  });

  if (close) close.addEventListener('click', () => drawer.hidden = true);
}

renderGraph();
