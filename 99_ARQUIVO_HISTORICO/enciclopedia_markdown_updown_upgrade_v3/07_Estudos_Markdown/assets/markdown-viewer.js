const params = new URLSearchParams(location.search);
const docPath = params.get('doc') || 'content/modelos/template_estudo_seguro.md';
const body = document.getElementById('markdownBody');
const meta = document.getElementById('readerMeta');

function escapeHtml(str){return str.replace(/[&<>]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[ch]));}
function parseFrontmatter(md){
  if(!md.startsWith('---')) return [{}, md];
  const end = md.indexOf('\n---', 3);
  if(end === -1) return [{}, md];
  const raw = md.slice(3,end).trim();
  const content = md.slice(end+4).trim();
  const data = {};
  raw.split('\n').forEach(line => {
    const idx = line.indexOf(':');
    if(idx > -1){ data[line.slice(0,idx).trim()] = line.slice(idx+1).trim().replace(/^['"]|['"]$/g,''); }
  });
  return [data, content];
}
function mdToHtml(md){
  let html = escapeHtml(md);
  const blocks = [];
  html = html.replace(/```([\s\S]*?)```/g, (_, code) => { const id = `@@CODE${blocks.length}@@`; blocks.push(`<pre><code>${code.trim()}</code></pre>`); return id; });
  html = html.replace(/^### (.*)$/gm,'<h3>$1</h3>')
             .replace(/^## (.*)$/gm,'<h2>$1</h2>')
             .replace(/^# (.*)$/gm,'<h1>$1</h1>')
             .replace(/^> (.*)$/gm,'<blockquote>$1</blockquote>')
             .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
             .replace(/`([^`]+)`/g,'<code>$1</code>')
             .replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');
  html = html.split(/\n{2,}/).map(chunk => {
    if(chunk.startsWith('<h') || chunk.startsWith('<blockquote') || chunk.startsWith('<pre') || chunk.startsWith('@@CODE')) return chunk;
    if(/^[-*] /m.test(chunk)) return '<ul>' + chunk.split('\n').filter(Boolean).map(li => `<li>${li.replace(/^[-*] /,'')}</li>`).join('') + '</ul>';
    if(/^\d+\. /m.test(chunk)) return '<ol>' + chunk.split('\n').filter(Boolean).map(li => `<li>${li.replace(/^\d+\. /,'')}</li>`).join('') + '</ol>';
    return `<p>${chunk.replace(/\n/g,'<br>')}</p>`;
  }).join('\n');
  blocks.forEach((b,i)=> html = html.replace(`@@CODE${i}@@`, b));
  return html;
}
async function loadDoc(){
  try{
    const res = await fetch(docPath + '?t=' + Date.now());
    if(!res.ok) throw new Error('Arquivo não encontrado');
    const text = await res.text();
    const [fm, content] = parseFrontmatter(text);
    meta.innerHTML = `<h2>${fm.icon || '📄'} ${fm.title || 'Documento'}</h2>
      <p class="muted"><strong>Versão:</strong> ${fm.version || '—'}</p>
      <p class="muted"><strong>Status:</strong> ${fm.status || '—'}</p>
      <p class="muted"><strong>Tema:</strong> ${fm.theme || '—'}</p>
      <p class="muted"><strong>Atualizado:</strong> ${fm.updated || '—'}</p>
      <a class="btn primary" href="${docPath}" download>⬇️ Baixar MD</a>`;
    body.innerHTML = mdToHtml(content);
  }catch(err){ body.innerHTML = `<h1>⚠️ Erro</h1><p>${err.message}</p>`; }
}
loadDoc();
