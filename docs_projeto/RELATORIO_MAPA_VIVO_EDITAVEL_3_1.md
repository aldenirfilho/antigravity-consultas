# RELATÓRIO — Mapa Vivo Editável 3.1

Data: 2026-05-08  
Repositório alvo: `aldenirfilho/antigravity-consultas`  
Página alvo: `https://aldenirfilho.github.io/antigravity-consultas/#mapa`

## 1. Problemas corrigidos

- Linhas de conexão muito apagadas.
- Ausência de linhas tracejadas para conexões sugeridas.
- Falta de modo visual de curadoria.
- Inclusão/exclusão de itens não funcional.
- Mapa subutilizado como apenas desenho, sem cérebro visual.
- Drawer instável/fantasma.
- Falta de busca, filtros, zoom e fallback seguro.
- Falta de exportação de patch JSON.

## 2. Arquivos incluídos/substituíveis

- `assets/js/graph.js`
- `assets/css/graph-vivo.css`
- `data/connections.json`
- `data/mapa_vivo_schema_v3.json`
- `data/mapa_vivo_admin_config.json`
- `templates/TEMPLATE_PATCH_MAPA_VIVO_ADMIN.json`
- `scripts/validate_mapa_vivo.py`
- `index_demo_mapa_vivo.html`

## 3. Funções adicionadas

### Curadoria

- Incluir tema.
- Editar tema selecionado.
- Ocultar tema sem apagar fisicamente.
- Adicionar conexão direta.
- Adicionar conexão sugerida.
- Aprovar conexão sugerida.
- Rejeitar conexão sugerida.
- Exportar/copiar patch JSON.

### Visualização

- Linha contínua = conexão direta.
- Linha tracejada = sugestão/curadoria.
- Busca por tema, tag e módulo.
- Filtros: Núcleo, Clínico, Arquivos, Tudo.
- Zoom +, zoom -, reset.
- Drawer com conexões diretas, sugeridas e sugestões automáticas.

## 4. Segurança

A exclusão é lógica, não destrutiva:

```json
{ "op": "hideNode", "id": "tema", "reason": "motivo" }
```

O Antigravity deve aplicar posteriormente no JSON principal:

```json
{ "visible": false, "status": "oculto" }
```

## 5. Validação sugerida

No Antigravity:

```bash
python3 scripts/validate_mapa_vivo.py data/connections.json
```

Critérios:

- todo node tem `id`;
- todo edge aponta para nodes existentes;
- não há IDs duplicados;
- edges `suggested` renderizam tracejadas;
- edges `direct` renderizam contínuas;
- ocultos/rejeitados não renderizam.

## 6. Pendências futuras

- Criar ferramenta automática para aplicar patches exportados ao `data/connections.json`.
- Integrar com Card Feed e Biblioteca IA para gerar nós automaticamente.
- Criar versão de mapa focada em trilhas TEMI.
- Criar modo “plantão” com apenas protocolos de decisão rápida.
