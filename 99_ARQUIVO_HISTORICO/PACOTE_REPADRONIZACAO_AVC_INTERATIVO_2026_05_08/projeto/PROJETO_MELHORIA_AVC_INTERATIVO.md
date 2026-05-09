# Projeto de Melhoria — Repadronização do Módulo Interativo AVC Agudo

## 1. Diagnóstico

A página atual `01_Modulos_Clinicos/AVC_Agudo/avc.html` funciona, mas está visualmente fora do padrão geral do projeto.

### Diferenças detectadas

| Ponto | Página atual AVC | Padrão do projeto |
|---|---|---|
| Framework visual | Tailwind CDN + classes próprias | CSS compartilhado `assets/css/base.css` + identidade institucional |
| Paleta | violeta/fúcsia/pink + light/dark | fundo escuro, cyan/green/violet, glass cards |
| Topbar | fixed própria | topbar institucional sticky/glass |
| Hero | gradiente fúcsia | hero escuro com glass, métricas e ações |
| Sidebar | branca no modo light | painel escuro/glass institucional |
| Conteúdo dinâmico | cards Tailwind claros | acordeões/card glass escuros |
| Identidade | “Matriz V7” isolada | Enciclopédia Médica Intensiva & Medicina Interna |

## 2. Objetivo da repadronização

Transformar o módulo interativo de AVC em uma página com identidade única da Enciclopédia, preservando a funcionalidade dinâmica.

## 3. Escopo técnico

### Alterar

- `01_Modulos_Clinicos/AVC_Agudo/avc.html`
- criar `01_Modulos_Clinicos/AVC_Agudo/avc-theme.css`
- opcionalmente ajustar `01_Modulos_Clinicos/AVC_Agudo/avc.js` apenas em classes visuais
- atualizar documentação em `08_Documentacao_Projeto/RELATORIO_REPADRONIZACAO_AVC.md`

### Não alterar conteúdo clínico

- `db_fundamentos.js`
- `db_pratica.js`
- `db_interativo.js`
- `db_pesquisa.js`
- `db_cross_ia.js`

## 4. Nova arquitetura visual

```text
AVC Agudo Interativo
├── topbar institucional
├── breadcrumb discreto
├── layout com sidebar + main
├── hero glass
├── painel de métricas
├── botões de ação
├── conteúdo dinâmico renderizado por avc.js
├── footer institucional
└── scripts db_*.js preservados
```

## 5. Padrão editorial

A página deve comunicar:

- emergência tempo-dependente;
- foco UTI/TEMI;
- navegação rápida;
- segurança clínica;
- estudo ativo;
- conexão com Banco TEMI, Dashboard e Biblioteca IA.

## 6. Critério de sucesso

- A página abre em GitHub Pages.
- O menu lateral é preenchido pelo `avc.js`.
- O conteúdo dinâmico aparece.
- Botões para Material Extenso, Galeria e Dashboard funcionam.
- Visual fica coerente com home, Calculadoras, Banco TEMI e Card Feed.
- Mobile fica utilizável.
