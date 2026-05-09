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
