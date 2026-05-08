const fallbackNodes = [
  { id: 'avc', label: '🧠 AVC Agudo', body: 'Hub inaugural do projeto.', x: 42, y: 28 },
  { id: 'trombolise', label: '💉 Trombólise', body: 'Janela, contraindicações, PA e sangramento.', x: 10, y: 12 },
  { id: 'trombectomia', label: '🧲 Trombectomia', body: 'OGV, angioTC, perfusão e regulação.', x: 72, y: 12 },
  { id: 'pa', label: '🎚️ PA no AVC', body: 'Metas pressóricas por cenário clínico.', x: 8, y: 42 },
  { id: 'fa', label: '❤️ FA', body: 'AVC cardioembólico e anticoagulação.', x: 76, y: 42 },
  { id: 'neuroimagem', label: '🖥️ Neuroimagem', body: 'TC, ASPECTS, angioTC e perfusão.', x: 34, y: 6 },
  { id: 'temi', label: '🏆 TEMI', body: 'Pegadinhas, questões e flashcards.', x: 50, y: 50 },
  { id: 'aki-trs', label: '🧪 AKI/TRS', body: 'KDIGO 2026, hemodiálise, TRRC, AKI na UTI.', x: 18, y: 68 },
  { id: 'vm-sdra', label: '🫁 VM/SDRA', body: 'Ventilação protetora, driving pressure, PEEP, prona.', x: 42, y: 72 },
  { id: 'sepse', label: '🦠 Sepse/Choque', body: 'Bundle 1h/3h, DVA, lactato, antimicrobianos.', x: 68, y: 68 },
  { id: 'diabetes', label: '👨‍👩‍👧 Diabetes/Família', body: 'Orientação para cuidador, insulina, glicemia.', x: 88, y: 56 },
  { id: 'card-feed', label: '🖼️ Card Feed', body: 'Feed visual de cards médicos com revisão espaçada.', x: 28, y: 88 },
  { id: 'biblioteca-ia', label: '📚 Biblioteca IA', body: 'Repositório de PDFs, Word e HTML com curadoria IA.', x: 56, y: 88 },
  { id: 'calculadoras', label: '🧮 Calculadoras UTI', body: 'Drogas, diluições, ventilação, eletrólitos, renal.', x: 82, y: 82 }
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
