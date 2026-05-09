# PROMPT PARA ANTIGRAVITY — Aplicar Mapa Vivo Editável 3.1

Você está no repositório `aldenirfilho/antigravity-consultas`.

Objetivo: aplicar o pacote `mapa_vivo_editavel_3_1_antigravity` para corrigir e otimizar o Mapa Vivo da seção `#mapa`.

## Regras de segurança

1. Antes de substituir qualquer arquivo, crie backup lógico de:
   - `index.html`
   - `assets/js/graph.js`
   - `assets/css/graph-vivo.css`
   - `data/connections.json`
2. Não apagar arquivos sem confirmar.
3. Não usar dados reais de pacientes.
4. Fazer commits pequenos e reversíveis.
5. Validar no navegador e no console.

## Tarefas

1. Copiar/substituir:
   - `assets/js/graph.js`
   - `assets/css/graph-vivo.css`
   - `data/connections.json`
2. Adicionar:
   - `data/mapa_vivo_schema_v3.json`
   - `data/mapa_vivo_admin_config.json`
   - `templates/TEMPLATE_PATCH_MAPA_VIVO_ADMIN.json`
   - `scripts/validate_mapa_vivo.py`
   - `08_Documentacao_Projeto/RELATORIO_MAPA_VIVO_EDITAVEL_3_1.md`
3. Conferir `index.html`:
   - carregar `assets/css/graph-vivo.css` no head;
   - carregar D3 v7;
   - carregar `assets/js/graph.js` antes de `</body>`;
   - garantir `section#mapa` com `div#graph`.
4. Rodar validação:
   - `python3 scripts/validate_mapa_vivo.py data/connections.json`
5. Testar manualmente:
   - home → `#mapa`;
   - linhas contínuas;
   - linhas tracejadas;
   - clique nos nós;
   - drawer;
   - busca;
   - filtros Núcleo/Clínico/Arquivos/Tudo;
   - zoom/reset;
   - painel `🛠️ Curadoria`;
   - incluir tema;
   - ocultar tema;
   - adicionar conexão direta;
   - adicionar conexão sugerida;
   - exportar patch JSON;
   - teste mobile.

## Critério de sucesso

O Mapa Vivo deve deixar de ser apenas decorativo e funcionar como cérebro visual editável da Enciclopédia:

- nó novo aparece imediatamente;
- tema oculto desaparece sem apagar do JSON;
- conexão direta aparece como linha contínua;
- conexão sugerida aparece como linha tracejada;
- patch JSON é exportado/copiado;
- não há erro no console;
- não há drawer fantasma.
