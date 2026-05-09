# Relatório — Repadronização AVC Interativo

**Data:** 2026-05-08  
**Página alvo:** `01_Modulos_Clinicos/AVC_Agudo/avc.html`

## Objetivo

Repadronizar o módulo interativo de AVC Agudo para o padrão visual geral da Enciclopédia Médica Intensiva & Medicina Interna.

## Arquivos criados

- `01_Modulos_Clinicos/AVC_Agudo/avc-theme.css`
- `08_Documentacao_Projeto/RELATORIO_REPADRONIZACAO_AVC.md`

## Arquivos modificados

- `01_Modulos_Clinicos/AVC_Agudo/avc.html`
- opcional: `01_Modulos_Clinicos/AVC_Agudo/avc.js`

## IDs preservados

- `menuBtn`
- `sidebar`
- `overlay`
- `sidebar-nav`
- `themeToggle`
- `dynamic-content`

## Scripts preservados

- `db_fundamentos.js`
- `db_pratica.js`
- `db_interativo.js`
- `db_pesquisa.js`
- `db_cross_ia.js`
- `avc.js`

## Validação

- [ ] Página abre.
- [ ] Menu lateral renderiza.
- [ ] Acordeões renderizam.
- [ ] Material Extenso abre.
- [ ] Galeria abre.
- [ ] Dashboard abre.
- [ ] Banco TEMI abre.
- [ ] Calculadoras abre.
- [ ] Card Feed abre.
- [ ] Mobile validado.

## Pendências

- Avaliar futura remoção completa do Tailwind CDN após refatoração integral de `avc.js`.
