# 🛡️ ANTIGRAVITY ENGINE — Manifesto de Arquitetura para IAs

Este documento serve como a "Instrução de Sistema" mestre para qualquer IA (GPT Codex, Claude, etc.) que atue neste repositório. O objetivo é garantir a continuidade, segurança e a experiência de usuário (UX) do Dr. Aldenir Rocha.

---

## 🧠 1. PERFIL DO USUÁRIO E MISSÃO
- **Usuário:** Médico Intensivista, Mestre, com **TDAH Grave**.
- **Missão:** Criar ferramentas de **beira-leito** que economizem tempo, reduzam erros e organizem o conhecimento de forma visual e rápida.
- **Estilo de Entrega:** **TDAH-Friendly**. Sem textos longos. Use checklists, tabelas, cards e muitos emojis (⚓, 🧬, 🚀, 🚨).

---

## 🏗️ 2. ARQUITETURA "BUNKER" DE DEPLOY
O repositório utiliza uma estratégia de isolamento para evitar erros de build no GitHub Pages:

- **Pasta Raiz (`/`):** Contém arquivos de trabalho, scripts administrativos e backups.
- **Pasta `public_site/` (O BUNKER):** É o espelho estático do site. **SOMENTE** o conteúdo desta pasta é publicado no GitHub Pages.
- **Workflow de Deploy:** Localizado em `.github/workflows/pages-static.yml`. Ele empacota e envia apenas a pasta `public_site`.
- **REGRA DE OURO:** Se você criar um novo recurso (ex: `modulo-novo.html`), ele deve ser salvo na sua pasta de origem E copiado para a pasta equivalente dentro de `public_site/`.

---

## 🗺️ 3. O REGISTRO CENTRAL (SINGLE SOURCE OF TRUTH)
O Hub de Estudos (`UpDown Hub`) é dinâmico e alimentado por um manifesto JSON:
- **Caminho:** `07_Estudos_Markdown/registry.json`
- **Ação:** Todo novo módulo de estudo deve ser registrado aqui para aparecer como um card na interface web.
- **Estrutura:** Seguir rigorosamente o esquema de `id`, `title`, `path` e `category`.

---

## 🎨 4. PADRÕES DE DESIGN E UX
- **Tecnologia:** HTML5, CSS3 (Vanilla) e JavaScript puro. Evite frameworks pesados.
- **Estética:** Premium, Dark Mode, Glassmorphism (blur de fundo), botões grandes e responsividade total para **iPhone**.
- **Rapidez:** O médico no plantão tem segundos. A informação crítica (doses, fluxogramas) deve estar visível no primeiro scroll.

---

## 🛡️ 5. SEGURANÇA E LGPD MÉDICA
- **NUNCA** use dados reais de pacientes (nomes, CPFs, prontuários).
- **Mocks:** Use `PACIENTE_EXEMPLO_001`.
- **Disclaimer:** Todo app médico deve conter: *"Ferramenta educacional/apoio. Não substitui julgamento clínico."*

---

## 🤖 6. COMUNICAÇÃO COM ANTIGRAVITY (GEMINI AGENT)
- Eu sou o **Antigravity**, o agente principal de manutenção estrutural.
- Trabalhe em modo cooperativo. Se fizer mudanças estruturais, documente no README ou em um novo commit claro.
- Use prefixos nos commits: `[GPT-CODEX]`, `[CLAUDE]`, `[FIX]`, `[FEAT]`.

---

## 📁 7. MAPA DE PASTAS PRINCIPAIS
- `01_Modulos_Clinicos/`: Apps e calculadoras complexas.
- `03_Calculadoras_UTI/`: Motores de cálculo.
- `05_Biblioteca_IA/`: Resgate de documentos e protocolos.
- `07_Estudos_Markdown/`: Conteúdo didático UpDown.
- `data/`: Arquivos JSON de configuração do Mapa Vivo e Site.
- `_SUPORTE_PROJETO/`: Documentos internos e manuais de IA.

---

**Assinado:** *Antigravity Engine Agent* 🚀🩺
