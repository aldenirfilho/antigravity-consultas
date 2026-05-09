# 00 — Diagnóstico estrutural do repositório `antigravity-consultas`

**Objetivo:** orientar o Gemini 3 Flash/Antigravity a resgatar o site sem destruir material existente.

## Resumo executivo 🚨

O problema principal não parece ser perda real de arquivos. A listagem mostra um repositório **grande, vivo e rico**, mas com camadas concorrentes:

- **918 caminhos únicos** na listagem enviada.
- **198 arquivos** dentro de `05_Biblioteca_IA/inbox/`, incluindo **108 DOCX** e **83 PDF**.
- **30 arquivos `index.html`**, o que cria múltiplas entradas públicas e risco de rotas desencontradas.
- Muitos pacotes de resgate/patch (`PACOTE_*`, `UPDOWN_*`, `backups`, `mapa_vivo_*`) coexistem no root, competindo com as rotas públicas.

## Diagnóstico provável

### 1. Biblioteca existe, mas a UI está vazia
O acervo está em `05_Biblioteca_IA/inbox/`, mas a página publicada pode apontar para JSON errado, catálogo incompleto ou caminho relativo quebrado. Resultado: aparece “0 arquivos” apesar de existirem muitos arquivos.

### 2. Rotas canônicas se misturaram com pacotes de instalação
O GitHub Pages está vendo pastas que são **pacotes de trabalho**, não necessariamente páginas finais. Isso polui o projeto e pode confundir o agente.

### 3. Há duplicação de hubs
Existem pelo menos estes hubs públicos/semipúblicos:

- `index.html`
- `updown/index.html`
- `07_Estudos_Markdown/index.html`
- `biblioteca/index.html`
- `05_Biblioteca_IA/index.html`
- `imagens/index.html`
- `apps/index.html`
- `03_Calculadoras_UTI/index.html`

Sem um manifesto central, cada alteração quebra outra rota.

### 4. Mapa Vivo usa múltiplos JSONs
Há `connections.json`, `data/connections.json`, `mapa_vivo_editavel_3_1_antigravity/data/connections.json` e outros patches. O sistema precisa escolher **um JSON canônico**.

### 5. UpDown tem dados, mas o contador pode renderizar zero
O arquivo `07_Estudos_Markdown/registry.json` deve alimentar o hub, mas a página pode não estar hidratando corretamente os cards/métricas.

## Princípio de resgate

> **Manifest-first:** antes de redesenhar, gere um inventário central e faça as páginas lerem esse inventário. Não mover, não apagar e não renomear arquivos originais.

## Regra de ouro

✅ Pode criar wrappers, manifests, índices e redirects seguros.  
❌ Não pode excluir PDFs, DOCX, MD, HTML, imagens, ZIPs, JSONs ou pacotes antigos sem backup e relatório.
