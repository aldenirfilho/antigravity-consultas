// Script de auto-classificação dos arquivos do inbox
// Lê os arquivos, compara com keywords da taxonomia, gera catalogo + brain connections
const fs = require('fs');
const path = require('path');

const INBOX = path.join(__dirname, '05_Biblioteca_IA/inbox');
const TAX_PATH = path.join(__dirname, '05_Biblioteca_IA/data/biblioteca_taxonomia_temas.json');
const CAT_OUT = path.join(__dirname, '05_Biblioteca_IA/data/biblioteca_catalogo.json');
const BRAIN_OUT = path.join(__dirname, '05_Biblioteca_IA/data/biblioteca_brain_connections.json');

const taxonomy = JSON.parse(fs.readFileSync(TAX_PATH, 'utf8'));
const themes = taxonomy.themes;

// Ler arquivos do inbox
const files = fs.readdirSync(INBOX).filter(f => {
  if (f === '.DS_Store' || f === 'README.md') return false;
  return true;
});

console.log(`📂 Total de arquivos no inbox: ${files.length}`);

// Determinar tipo
function getType(name) {
  const ext = path.extname(name).toLowerCase().replace('.', '');
  if (['pdf'].includes(ext)) return 'pdf';
  if (['docx', 'doc'].includes(ext)) return 'word';
  if (['html', 'htm'].includes(ext)) return 'html';
  if (['md', 'txt'].includes(ext)) return 'text';
  if (['csv', 'xlsx'].includes(ext)) return 'data';
  if (['png', 'jpg', 'jpeg', 'webp'].includes(ext)) return 'image';
  return 'outro';
}

// Classificar por keywords
function classify(filename) {
  const lower = filename.toLowerCase().replace(/[_\-\.]/g, ' ');
  let bestTheme = null;
  let bestScore = 0;
  
  for (const theme of themes) {
    if (theme.id === 'inbox-revisar') continue;
    let score = 0;
    for (const kw of theme.keywords) {
      if (lower.includes(kw.toLowerCase())) {
        score += kw.length; // Longer keyword matches score more
      }
    }
    if (score > bestScore) {
      bestScore = score;
      bestTheme = theme;
    }
  }
  
  return bestScore >= 3 ? bestTheme : themes.find(t => t.id === 'inbox-revisar');
}

// Gerar slug
function toSlug(name) {
  return name.replace(/\.[^.]+$/, '')
    .replace(/[^a-zA-Z0-9]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .toLowerCase()
    .slice(0, 80);
}

// Gerar título
function toTitle(name) {
  return name.replace(/\.[^.]+$/, '')
    .replace(/[_\-]+/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())
    .trim();
}

// Processar
const items = [];
const nodes = [
  { id: 'biblioteca-ia', label: '📚 Biblioteca IA', type: 'module', theme: 'projeto', path: '05_Biblioteca_IA/index.html' }
];
const edges = [];
const stats = {};

for (const file of files) {
  const theme = classify(file);
  const tipo = getType(file);
  const slug = toSlug(file);
  const title = toTitle(file);
  const themeId = theme ? theme.id : 'inbox-revisar';
  
  stats[themeId] = (stats[themeId] || 0) + 1;
  
  items.push({
    id: slug,
    title: title,
    filename: file,
    theme: themeId,
    tipo: tipo,
    tags: [themeId, tipo],
    status: themeId === 'inbox-revisar' ? 'revisar' : 'catalogado',
    path: 'inbox/' + file,
    resumo: '',
    ia_origem: 'Auto-classificado',
    data: '2026-05',
    createdAt: new Date().toISOString()
  });
  
  // Brain node
  nodes.push({
    id: slug,
    label: (theme ? theme.emoji + ' ' : '📥 ') + title.slice(0, 50),
    type: 'file',
    theme: themeId,
    path: 'inbox/' + file
  });
  
  // Brain edges
  edges.push({ from: slug, to: 'biblioteca-ia', relation: 'pertence-a' });
  edges.push({ from: slug, to: themeId, relation: 'classificado-em' });
  
  // Extra connections
  if (['temi-prova'].includes(themeId) || file.toLowerCase().includes('temi')) {
    edges.push({ from: slug, to: 'banco-temi', relation: 'gera-questoes' });
  }
  if (['farmaco-doses'].includes(themeId) || file.toLowerCase().includes('dose') || file.toLowerCase().includes('calculo')) {
    edges.push({ from: slug, to: 'calculadoras-uti', relation: 'apoia-calculo' });
  }
}

// Add theme nodes
for (const theme of themes) {
  nodes.push({
    id: theme.id,
    label: theme.emoji + ' ' + theme.label,
    type: 'theme',
    theme: theme.id,
    path: theme.folder
  });
}

// Save catalog
const catalog = {
  updatedAt: new Date().toISOString().slice(0, 10),
  project: 'Biblioteca IA — Enciclopédia Médica Intensiva',
  totalFiles: items.length,
  stats: stats,
  items: items
};
fs.writeFileSync(CAT_OUT, JSON.stringify(catalog, null, 2), 'utf8');

// Save brain
const brain = {
  updatedAt: new Date().toISOString().slice(0, 10),
  nodes: nodes,
  edges: edges
};
fs.writeFileSync(BRAIN_OUT, JSON.stringify(brain, null, 2), 'utf8');

// Report
console.log(`\n✅ Catálogo gerado: ${items.length} arquivos`);
console.log(`📊 Classificação por tema:`);
const sorted = Object.entries(stats).sort((a, b) => b[1] - a[1]);
for (const [theme, count] of sorted) {
  const t = themes.find(th => th.id === theme);
  console.log(`   ${t ? t.emoji : '📥'} ${theme}: ${count}`);
}
console.log(`\n🧠 Brain: ${nodes.length} nós, ${edges.length} edges`);
console.log(`📄 Salvos em:`);
console.log(`   ${CAT_OUT}`);
console.log(`   ${BRAIN_OUT}`);
