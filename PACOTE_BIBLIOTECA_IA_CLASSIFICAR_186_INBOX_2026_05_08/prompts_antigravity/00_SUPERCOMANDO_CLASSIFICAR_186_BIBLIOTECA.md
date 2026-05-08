# 00 — SUPERCOMANDO ANTIGRAVITY: Classificar 186 arquivos do Inbox da Biblioteca IA

Você está no repositório:

`aldenirfilho/antigravity-consultas`

## Objetivo

Classificar manualmente 186 arquivos do inbox da Biblioteca IA, organizando por tema, catalogando metadados e criando a “conexão cerebral” entre arquivos, temas, módulos e ferramentas do projeto.

## Pasta alvo

`05_Biblioteca_IA/inbox/`

## Arquivos de apoio deste pacote

Copiar para o repositório:

- `05_Biblioteca_IA/data/biblioteca_taxonomia_temas.json`
- `05_Biblioteca_IA/data/biblioteca_inbox_manifest_186.json`
- `05_Biblioteca_IA/data/biblioteca_catalogo.json`
- `05_Biblioteca_IA/data/biblioteca_brain_connections.json`
- `08_Documentacao_Projeto/PROJETO_CLASSIFICACAO_186_BIBLIOTECA_IA.md`
- `08_Documentacao_Projeto/WORKFLOW_MANUAL_186.md`
- `08_Documentacao_Projeto/CHECKLIST_CLASSIFICACAO_BIBLIOTECA.md`
- `08_Documentacao_Projeto/RELATORIO_CLASSIFICACAO_186_BIBLIOTECA.md`

## Regras críticas

1. Não apagar arquivos.
2. Não substituir conteúdo sem backup lógico.
3. Não classificar automaticamente arquivos ambíguos.
4. Se houver dúvida, usar `theme: "inbox-revisar"` e `status: "revisar"`.
5. Preservar extensão original.
6. Renomear somente após identificar tema.
7. Atualizar catálogo e grafo após cada lote.
8. Trabalhar em lotes de 20 arquivos.

## Tarefa 1 — Escanear inbox

Ler todos os arquivos em:

`05_Biblioteca_IA/inbox/`

Gerar/atualizar:

`05_Biblioteca_IA/data/biblioteca_inbox_manifest_186.json`

Substituindo `SUBSTITUIR_PELO_NOME_REAL_001` etc. pelos nomes reais.

Se o número for diferente de 186, registrar no relatório.

## Tarefa 2 — Criar pastas por tema

Criar as pastas conforme `biblioteca_taxonomia_temas.json`.

Exemplos:

- `05_Biblioteca_IA/acervo/uti-geral/`
- `05_Biblioteca_IA/acervo/sepse-choque/`
- `05_Biblioteca_IA/acervo/vm-sdra/`
- `05_Biblioteca_IA/acervo/nefro-aki-trs/`
- `05_Biblioteca_IA/acervo/infectologia/`
- `05_Biblioteca_IA/acervo/neuro-uti/`
- `05_Biblioteca_IA/acervo/temi-prova/`

## Tarefa 3 — Interface manual de classificação

Atualizar `05_Biblioteca_IA/index.html` para ter uma fila manual:

- lista de arquivos inbox;
- botão “Pré-visualizar”;
- seletor de tema;
- seletor de status;
- campo título;
- campo tags;
- campo resumo;
- campo uso clínico;
- campo relevância TEMI;
- campo observação de segurança;
- campo conexões cerebrais;
- botão copiar JSON do item;
- botão marcar como revisar.

Como GitHub Pages estático não grava no repositório sozinho, implementar pelo menos uma destas opções:

A) exportar JSON atualizado para download;
B) instruir o Antigravity a mesclar manualmente no `biblioteca_catalogo.json`;
C) se estiver rodando localmente no Antigravity, editar diretamente os JSONs.

## Tarefa 4 — Classificação manual por lote

Para cada lote de 20 arquivos:

1. Abrir arquivo.
2. Identificar tema.
3. Gerar título didático.
4. Gerar slug único.
5. Gerar nome novo.
6. Mover para pasta do tema.
7. Criar item no `biblioteca_catalogo.json`.
8. Criar node no `biblioteca_brain_connections.json`.
9. Criar edges:
   - arquivo -> Biblioteca IA
   - arquivo -> tema principal
   - arquivo -> tema correlato, se houver
   - arquivo -> Banco TEMI, se relevante
   - arquivo -> Card Feed, se virar imagem/card
   - arquivo -> Calculadoras UTI, se tiver dose/cálculo
10. Atualizar relatório.

## Tarefa 5 — Conexão cerebral

Cada arquivo catalogado deve virar um nó:

```json
{
  "id": "file-slug",
  "label": "Título",
  "type": "file",
  "theme": "tema",
  "path": "caminho"
}
```

Cada arquivo deve criar edges:

```json
[
  {"from": "file-slug", "to": "biblioteca-ia", "relation": "pertence-a"},
  {"from": "file-slug", "to": "tema", "relation": "classificado-em"}
]
```

Adicionar edges extras quando indicado:

- `gera-questoes` para Banco TEMI.
- `gera-card` para Card Feed.
- `apoia-calculo` para Calculadoras UTI.
- `complementa-modulo` para módulos clínicos.

## Tarefa 6 — Atualizar página

Atualizar `05_Biblioteca_IA/index.html` para carregar:

- `data/biblioteca_catalogo.json`
- `data/biblioteca_taxonomia_temas.json`
- `data/biblioteca_brain_connections.json`

A página deve exibir:

- estatísticas reais;
- filtros por tema;
- busca;
- cards de arquivos;
- badge de status;
- botão preview;
- botão copiar citação/legenda;
- seção “Mapa cerebral da Biblioteca”.

## Tarefa 7 — Validação final

Rodar validação:

- JSON válido;
- sem IDs duplicados;
- todos os caminhos existem;
- arquivos classificados saíram do inbox;
- arquivos `revisar` permanecem no inbox;
- página abre;
- filtros funcionam;
- grafo aparece.

## Resultado final esperado

- 186 arquivos triados ou marcados como revisar;
- catálogo atualizado;
- pastas organizadas;
- conexões cerebrais criadas;
- relatório final preenchido.
