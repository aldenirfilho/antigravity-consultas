# Mapa de Mudanças — AVC Interativo

## Arquivo principal

`01_Modulos_Clinicos/AVC_Agudo/avc.html`

### Mudanças

1. Adicionar links CSS compartilhados:
   - `../../assets/css/base.css`
   - `./avc-theme.css`

2. Manter Tailwind temporariamente como camada de compatibilidade, porque `avc.js` ainda injeta classes Tailwind.

3. Alterar body:
   - antes: classes Tailwind light/dark
   - depois: `class="avc-page"`

4. Trocar header:
   - antes: header fixed branco/dark Tailwind
   - depois: topbar glass institucional.

5. Trocar hero:
   - antes: gradiente violeta/fúcsia/pink
   - depois: hero glass escuro com métricas.

6. Trocar sidebar:
   - antes: painel branco/dark Tailwind
   - depois: sidebar escura/glass com padrão do projeto.

7. Manter os IDs essenciais:
   - `menuBtn`
   - `sidebar`
   - `overlay`
   - `sidebar-nav`
   - `themeToggle`
   - `dynamic-content`

8. Manter scripts:
   - `db_fundamentos.js`
   - `db_pratica.js`
   - `db_interativo.js`
   - `db_pesquisa.js`
   - `db_cross_ia.js`
   - `avc.js`

## Arquivo novo

`01_Modulos_Clinicos/AVC_Agudo/avc-theme.css`

### Função

Criar camada visual institucional para o módulo AVC, usando variáveis do projeto e sobrescrevendo os elementos dinâmicos renderizados pelo `avc.js`.

## Relatório

Criar:

`08_Documentacao_Projeto/RELATORIO_REPADRONIZACAO_AVC.md`
