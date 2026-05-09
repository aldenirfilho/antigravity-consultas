# 00 — SUPERCOMANDO: Reformatar e Repadronizar Módulo Interativo AVC Agudo

Você está no repositório:

`aldenirfilho/antigravity-consultas`

## Objetivo

Repadronizar a página:

`01_Modulos_Clinicos/AVC_Agudo/avc.html`

para o padrão visual geral da Enciclopédia Médica Intensiva & Medicina Interna, preservando o conteúdo clínico e o motor dinâmico.

## Contexto

A home do projeto usa CSS compartilhado:

- `assets/css/base.css`
- `assets/css/home.css`

O AVC interativo usa Tailwind CDN e uma paleta própria violeta/fúcsia, ficando visualmente diferente do restante do portal.

## Regra crítica

Não quebrar:

- `sidebar-nav`
- `dynamic-content`
- `menuBtn`
- `sidebar`
- `overlay`
- `themeToggle`
- scripts `db_*.js`
- `avc.js`

Não apagar conteúdo clínico.

## Entregas obrigatórias

1. Criar:
   - `01_Modulos_Clinicos/AVC_Agudo/avc-theme.css`

2. Atualizar:
   - `01_Modulos_Clinicos/AVC_Agudo/avc.html`

3. Opcionalmente ajustar apenas classes visuais em:
   - `01_Modulos_Clinicos/AVC_Agudo/avc.js`

4. Criar relatório:
   - `08_Documentacao_Projeto/RELATORIO_REPADRONIZACAO_AVC.md`

## Passo 1 — Backup lógico

Antes de alterar, registrar no relatório:

- arquivo original;
- mudanças propostas;
- caminhos que serão mantidos;
- IDs que não podem ser removidos.

## Passo 2 — Adicionar CSS compartilhado e tema AVC

No `<head>` de `avc.html`, adicionar:

```html
<link rel="stylesheet" href="../../assets/css/base.css" />
<link rel="stylesheet" href="avc-theme.css" />
```

Manter Tailwind CDN temporariamente se `avc.js` ainda usar classes Tailwind.

## Passo 3 — Recriar estrutura visual

Substituir a estrutura visual externa da página por:

- `body class="avc-page"`
- `header class="topbar avc-topbar"`
- breadcrumb institucional
- layout `avc-layout`
- sidebar `avc-sidebar`
- main `avc-main`
- hero `avc-hero glass`
- painel de métricas
- botões de ação
- container `dynamic-content`

Preservar os IDs funcionais.

## Passo 4 — Criar CSS institucional

Usar o arquivo fornecido no pacote:

`arquivos_prontos/01_Modulos_Clinicos/AVC_Agudo/avc-theme.css`

Copiar para:

`01_Modulos_Clinicos/AVC_Agudo/avc-theme.css`

## Passo 5 — Refatorar visual dinâmico

Aplicar compatibilidade visual no CSS para elementos gerados por `avc.js`:

- `#dynamic-content details`
- `#dynamic-content summary`
- `#dynamic-content li`
- `#dynamic-content .flashcard`
- `#dynamic-content img`
- `#dynamic-content input`
- `#dynamic-content select`
- `#dynamic-content button`

Se necessário, editar `avc.js` apenas para substituir classes Tailwind muito destoantes por classes neutras.

## Passo 6 — Validar

Testar:

- abertura da página;
- preenchimento do menu lateral;
- preenchimento do conteúdo dinâmico;
- abertura de acordeões;
- botões Material Extenso/Galeria/Dashboard;
- mobile;
- console sem erro crítico.

## Passo 7 — Relatório

Criar:

`08_Documentacao_Projeto/RELATORIO_REPADRONIZACAO_AVC.md`

com:

- arquivos alterados;
- arquivos criados;
- links testados;
- pendências;
- decisão sobre manter ou remover Tailwind no futuro.

## Critério de sucesso

A página AVC interativa deve parecer parte do mesmo produto visual da home, Banco TEMI, Calculadoras UTI e Card Feed, mantendo todo o conteúdo funcionando.


---

# 02 — Refatorar AVC HTML

Refatore:

`01_Modulos_Clinicos/AVC_Agudo/avc.html`

## Obrigatório

Adicionar no head:

```html
<link rel="stylesheet" href="../../assets/css/base.css" />
<link rel="stylesheet" href="avc-theme.css" />
```

Manter:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

por enquanto, pois `avc.js` ainda injeta classes Tailwind.

## Estrutura final esperada

```html
<body class="avc-page">
  <header class="topbar avc-topbar">...</header>

  <nav class="avc-breadcrumb">...</nav>

  <div id="overlay" class="avc-overlay hidden"></div>

  <div class="avc-layout">
    <aside id="sidebar" class="avc-sidebar">
      <nav>
        <p class="avc-sidebar-title">Navegação rápida</p>
        <ul id="sidebar-nav"></ul>
        <div class="avc-tip">...</div>
      </nav>
    </aside>

    <main class="avc-main">
      <section class="avc-hero glass">...</section>
      <section class="avc-actions-panel glass">...</section>
      <div id="dynamic-content" class="avc-dynamic-content"></div>
      <footer class="footer avc-footer">...</footer>
    </main>
  </div>

  scripts...
</body>
```

## Preservar IDs

- `menuBtn`
- `sidebar`
- `overlay`
- `sidebar-nav`
- `themeToggle`
- `dynamic-content`

## Botões obrigatórios

- Home
- Material Extenso
- Galeria
- Dashboard
- Banco TEMI
- Calculadoras UTI
- Card Feed

## Não remover scripts

- `db_fundamentos.js`
- `db_pratica.js`
- `db_interativo.js`
- `db_pesquisa.js`
- `db_cross_ia.js`
- `avc.js`


---

# 03 — Criar AVC Theme CSS

Criar o arquivo:

`01_Modulos_Clinicos/AVC_Agudo/avc-theme.css`

Usar o conteúdo do pacote:

`arquivos_prontos/01_Modulos_Clinicos/AVC_Agudo/avc-theme.css`

Objetivo:

- usar variáveis globais do projeto;
- criar topbar e layout institucional;
- sobrescrever blocos brancos/claros do Tailwind;
- criar cards glass;
- melhorar sidebar;
- ajustar mobile;
- manter acessibilidade e contraste.

Depois validar no navegador.


---

# 04 — Compatibilizar AVC JS

Abrir:

`01_Modulos_Clinicos/AVC_Agudo/avc.js`

## Objetivo

Preservar lógica, conteúdo e funções. Alterar somente classes visuais se necessário.

## Não alterar

- `globalDB`
- `renderMatriz`
- `renderCalculadoras`
- `calcLAMS`
- `calcNIHSS`
- `renderFlashcardsGrid`
- `renderQuizEngine`
- `setupScrollSpy`

## Permitido alterar

Classes Tailwind muito destoantes dentro de templates HTML para classes institucionais:

- `avc-section`
- `avc-accordion`
- `avc-accordion-summary`
- `avc-section-icon`
- `avc-list`
- `avc-list-item`
- `avc-card`
- `avc-form-control`

## Estratégia segura

Preferir manter `avc.js` intacto e resolver visual por CSS em `avc-theme.css`.

Só editar `avc.js` se algum bloco continuar muito fora do padrão após o CSS.


---

# 05 — Validar e Publicar

Depois da repadronização:

1. Abrir `01_Modulos_Clinicos/AVC_Agudo/avc.html`.
2. Conferir console.
3. Conferir rede/Network para 404.
4. Testar:
   - Home
   - Material Extenso
   - Galeria
   - Dashboard
   - Banco TEMI
   - Calculadoras UTI
   - Card Feed
5. Testar mobile.
6. Criar/atualizar:

`08_Documentacao_Projeto/RELATORIO_REPADRONIZACAO_AVC.md`

## Conteúdo do relatório

- Data.
- Arquivos criados.
- Arquivos modificados.
- O que foi preservado.
- O que ainda pode melhorar.
- Se Tailwind foi mantido ou removido.
- Pendências.
