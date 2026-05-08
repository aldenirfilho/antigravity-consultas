# 📋 Relatório de Repadronização — Módulo AVC Agudo Interativo

**Data:** 2026-05-08  
**Autor:** Dr. Aldenir Rocha (via Antigravity)

---

## ✅ Arquivos criados

| Arquivo | Função |
|---|---|
| `01_Modulos_Clinicos/AVC_Agudo/avc-theme.css` | CSS institucional com glass, variáveis do projeto, sidebar sticky, hero com métricas, compatibilidade dinâmica |

## ✏️ Arquivos modificados

| Arquivo | Mudança |
|---|---|
| `01_Modulos_Clinicos/AVC_Agudo/avc.html` | Refatorado: topbar institucional, breadcrumb, sidebar glass, hero com métricas, painel de ações, footer, botões Banco TEMI/Calculadoras/Card Feed |

## 🔒 Preservado (IDs funcionais)

- ✅ `menuBtn` — botão menu mobile
- ✅ `sidebar` — painel lateral
- ✅ `overlay` — overlay mobile
- ✅ `sidebar-nav` — navegação dinâmica (preenchida por avc.js)
- ✅ `themeToggle` — toggle dark/light
- ✅ `dynamic-content` — container dinâmico (preenchido por avc.js)

## 🔒 Scripts preservados (sem alteração)

- ✅ `db_fundamentos.js`
- ✅ `db_pratica.js`
- ✅ `db_interativo.js`
- ✅ `db_pesquisa.js`
- ✅ `db_cross_ia.js`
- ✅ `avc.js`

## 🎨 Mudanças visuais

| Antes | Depois |
|---|---|
| Tailwind light/dark branco/fúcsia | Dark glass institucional |
| Header branco fixo | Topbar glass sticky institucional |
| Hero gradiente violeta/fúcsia/pink | Hero glass escuro com métricas (janela, PA, eixos) |
| Sidebar branca | Sidebar glass escura com border-radius 28px |
| Sem botões extras na topbar | Botões: Material Extenso, Galeria, Dashboard, Banco TEMI, Calculadoras, Card Feed |
| Breadcrumb inline simples | Breadcrumb institucional com pill glass |

## ⚠️ Tailwind CDN

**Status: MANTIDO temporariamente**

O `avc.js` injeta classes Tailwind nos acordeões e cards dinâmicos. O `avc-theme.css` sobrescreve os estilos visuais mais destoantes via `!important`, mas o CDN precisa ficar até que `avc.js` seja refatorado para usar classes institucionais.

## 📌 Pendências

1. ⏳ Remover Tailwind CDN quando avc.js for refatorado
2. ⏳ Testar todos os acordeões no mobile
3. ⏳ Verificar calculadoras inline (NIHSS, LAMS)
4. ⏳ Adicionar logo institucional na topbar

---

*Ferramenta educacional/de apoio. Não substitui julgamento clínico.*
