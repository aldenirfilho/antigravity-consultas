# 01 — SUPERCOMANDO PARA GEMINI 3 FLASH / ANTIGRAVITY

Você está no repositório:

`aldenirfilho/antigravity-consultas`

## Missão

Corrigir o site quebrado **sem apagar, mover ou renomear materiais originais**. O projeto é uma Enciclopédia Médica Intensiva/Medicina Interna com Biblioteca IA, UpDown, Imagens, Apps, Mapa Vivo, Banco TEMI e Calculadoras.

## Diagnóstico operacional

O site foi desorganizado por alterações anteriores que quebraram links e padrões. A listagem mostra que os materiais ainda existem, principalmente:

- `05_Biblioteca_IA/inbox/` com muitos PDF/DOCX/MD.
- `07_Estudos_Markdown/` com o hub UpDown e registros.
- `06_Card_Feed_Medico/` com feed visual.
- `03_Calculadoras_UTI/` e `07_Estudos_Markdown/apps/vasoativas/`.
- `01_Modulos_Clinicos/` com módulos como AVC e ventilação.
- muitos pacotes `PACOTE_*`, `UPDOWN_*` e `backups/` que devem ser preservados, mas não tratados como navegação pública principal.

## Regras obrigatórias

1. **Não deletar nada.**
2. **Não mover arquivos clínicos originais.**
3. Antes de alterar, criar relatório em:
   `08_Documentacao_Projeto/RELATORIO_RESGATE_GEMINI3_FLASH.md`
4. Trabalhar em pequenos lotes.
5. Para cada arquivo alterado, registrar:
   - caminho;
   - motivo;
   - antes/depois esperado;
   - risco de quebra;
   - como validar.
6. Preferir wrappers e manifests em vez de reestruturação destrutiva.
7. Preservar rotas antigas criando atalhos/redirecionamentos.
8. Não trocar todo o design de uma vez.
9. Primeiro restaurar acesso; depois melhorar estética.
10. Não inserir dados de pacientes, tokens, chaves, senhas ou dados sensíveis.

## Ordem de execução obrigatória

### Fase 0 — Inventário e backup lógico

Crie:

```txt
08_Documentacao_Projeto/RELATORIO_RESGATE_GEMINI3_FLASH.md
data/site_manifest.json
data/route_aliases.json
data/rescue_audit.json
```

Não altere a home ainda.

### Fase 1 — Definir rotas canônicas

Rotas públicas estáveis:

```txt
/index.html                                  -> Home
/updown/index.html                           -> wrapper para 07_Estudos_Markdown/index.html
/07_Estudos_Markdown/index.html              -> Hub UpDown canônico
/biblioteca/index.html                       -> Biblioteca pública estável
/05_Biblioteca_IA/index.html                 -> Biblioteca IA legada/canônica de acervo
/imagens/index.html                          -> Galeria pública
/apps/index.html                             -> Apps públicos
/03_Calculadoras_UTI/index.html              -> Calculadoras UTI
/02_Banco_Questoes_TEMI/index.html           -> Banco TEMI
/questoes/index.html                         -> wrapper para Banco TEMI
/data/connections.json                       -> JSON canônico do Mapa Vivo
```

### Fase 2 — Restaurar Biblioteca

Criar/atualizar:

```txt
05_Biblioteca_IA/data/biblioteca_inbox_manifest_auto.json
05_Biblioteca_IA/data/biblioteca_catalogo.json
biblioteca/index.html
05_Biblioteca_IA/index.html
```

A Biblioteca deve exibir todos os arquivos disponíveis em `05_Biblioteca_IA/inbox/`, com busca, filtro por tipo e tema, e botão “Abrir arquivo”.

### Fase 3 — Restaurar UpDown Hub

Corrigir:

```txt
07_Estudos_Markdown/index.html
07_Estudos_Markdown/assets/estudos.js
07_Estudos_Markdown/registry.json
updown/index.html
```

Critério: o painel não pode mostrar 0 UpDowns se `registry.json` tiver documentos.

### Fase 4 — Restaurar triângulo UpDown ↔ Biblioteca ↔ Imagens

Em todas as páginas centrais, inserir cards de navegação cruzada:

```txt
UpDown -> Biblioteca -> Imagens -> UpDown
```

Cada módulo UpDown deve apontar para:
- conteúdo leitor;
- fontes/biblioteca;
- imagens/infográficos;
- apps relacionados quando existirem.

### Fase 5 — Corrigir Mapa Vivo

Usar `data/connections.json` como fonte canônica. Se estiver vazio, reconstruir a partir de `connections.json` e `data/site_manifest.json`.

Corrigir:
- links inexistentes;
- linhas diretas e sugeridas;
- modo de busca;
- persistência local;
- export/import patch;
- fallback visual caso D3/CDN falhe.

### Fase 6 — Corrigir calculadoras de vasoativas

Usar:

```txt
07_Estudos_Markdown/data/vasoactive_drugs_brasil_presets.json
07_Estudos_Markdown/apps/vasoativas/index.html
03_Calculadoras_UTI/index.html
```

Corrigir fórmula, unidades, presets e alertas.

### Fase 7 — Teste de links

Validar no GitHub Pages:

- Home abre.
- Biblioteca mostra arquivos.
- UpDown mostra módulos.
- Imagens abre.
- Apps abre.
- Vasoativas abre e calcula corretamente.
- Banco TEMI abre.
- Mapa Vivo abre, mostra linhas e links funcionais.
- Nenhum link público principal leva a 404.

## Critério final de sucesso

O site volta a ser navegável com padrão:

```txt
Home
├── UpDown
│   ├── Biblioteca relacionada
│   ├── Imagens relacionadas
│   └── Apps relacionados
├── Biblioteca
├── Imagens
├── Apps / Calculadoras
├── Banco TEMI
├── Card Feed
└── Mapa Vivo
```

No final, entregar relatório com checklist de validação e lista de pendências.
