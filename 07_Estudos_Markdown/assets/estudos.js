const grid = document.getElementById('docsGrid');
const themeFilter = document.getElementById('themeFilter');
const statusFilter = document.getElementById('statusFilter');
const searchInput = document.getElementById('searchInput');
let registry = { documents: [] };

const badge = (text, cls='pill') => `<span class="${cls}">${text}</span>`;

async function loadRegistry(){
  try{
    const res = await fetch('registry.json?t=' + Date.now());
    registry = await res.json();
    hydrateFilters();
    renderDocs();
  }catch(err){
    grid.innerHTML = `<article class="card"><h3>⚠️ Erro</h3><p>Não consegui abrir registry.json: ${err.message}</p></article>`;
  }
}

function hydrateFilters(){
  const themes = [...new Set(registry.documents.map(d => d.theme).filter(Boolean))].sort();
  const statuses = [...new Set(registry.documents.map(d => d.status).filter(Boolean))].sort();
  themes.forEach(t => themeFilter.insertAdjacentHTML('beforeend', `<option value="${t}">${t}</option>`));
  statuses.forEach(s => statusFilter.insertAdjacentHTML('beforeend', `<option value="${s}">${s}</option>`));
  document.getElementById('metricDocs').textContent = registry.documents.length;
  document.getElementById('metricThemes').textContent = themes.length;
}

function renderDocs(){
  const q = (searchInput.value || '').toLowerCase();
  const theme = themeFilter.value;
  const status = statusFilter.value;
  const docs = registry.documents.filter(d => {
    const hay = `${d.title} ${d.theme} ${(d.tags||[]).join(' ')} ${d.summary||''}`.toLowerCase();
    return (!q || hay.includes(q)) && (!theme || d.theme === theme) && (!status || d.status === status);
  });
  grid.innerHTML = docs.map(d => `
    <article class="card">
      <h3>${d.icon || '📄'} ${d.title}</h3>
      <p>${d.summary || ''}</p>
      <div class="pillrow">
        ${badge(d.status || 'sem status','pill status')}
        ${badge(d.version || 'v0')}
        ${badge(d.theme || 'tema')}
        ${(d.tags||[]).slice(0,4).map(t => badge('#'+t)).join('')}
      </div>
      <div class="actions">
        <a class="btn primary" href="${d.path.endsWith('.html') ? d.path : `viewer.html?doc=${encodeURIComponent(d.path)}`}">
          ${d.path.endsWith('.html') ? 'Abrir Leitor PRO →' : 'Abrir MD →'}
        </a>
        ${d.relatedUrl ? `<a class="btn ghost" href="${d.relatedUrl}">Conectar →</a>` : ''}
      </div>
    </article>
  `).join('') || `<article class="card"><h3>🔍 Nada encontrado</h3><p>Tente outro tema, status ou termo.</p></article>`;
}

[searchInput, themeFilter, statusFilter].forEach(el => el && el.addEventListener('input', renderDocs));
loadRegistry();
