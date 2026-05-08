# 06 — Corrigir Mapa Vivo sem quebrar o site

## Objetivo

Transformar o Mapa Vivo em uma camada funcional de navegação e curadoria.

## Fonte canônica

Usar:

```txt
data/connections.json
```

Se vazio ou quebrado, reconstruir com base em:

```txt
connections.json
data/site_manifest.json
07_Estudos_Markdown/registry.json
05_Biblioteca_IA/data/biblioteca_catalogo.json
```

## Correções obrigatórias

### 1. Links quebrados

Corrigir URLs que apontam para caminhos inexistentes. Exemplos de correção:

```txt
banco-temi/index.html -> 02_Banco_Questoes_TEMI/index.html
temas/avc-agudo/... -> 01_Modulos_Clinicos/AVC_Agudo/...
temas/vm-sdra/index.html -> 01_Modulos_Clinicos/Ventilacao_Mecanica/respirasense/index.html OU página placeholder
temas/aki-trs/index.html -> 07_Estudos_Markdown/biblioteca/index.html?theme=nefro-aki-trs OU página placeholder
```

### 2. Linhas visíveis

- direta: linha contínua;
- sugerida: linha tracejada forte;
- labels legíveis;
- camada de links abaixo dos nós;
- `vector-effect: non-scaling-stroke`.

### 3. Inclusão/exclusão real

Implementar overlay local:

```txt
localStorage key: mapaVivo.overlay.v4
```

Com:

```json
{
  "addedNodes": [],
  "updatedNodes": [],
  "hiddenNodeIds": [],
  "addedEdges": [],
  "updatedEdges": [],
  "hiddenEdgeKeys": [],
  "positions": {},
  "rejectedSuggestions": []
}
```

### 4. Botões obrigatórios

- Adicionar nó
- Editar nó selecionado
- Ocultar nó
- Adicionar conexão
- Aceitar sugestão
- Rejeitar sugestão
- Salvar localmente
- Exportar patch JSON
- Importar patch JSON
- Limpar alterações locais
- Resetar layout

### 5. Fallback sem D3/CDN

Se o grafo falhar, renderizar uma lista navegável:

```txt
Nó | tipo | status | abrir | conexões
```

## Critérios de validação

- Adicionar “Lúpus na UTI” aparece imediatamente.
- Atualizar página mantém alteração local.
- Excluir sem campo preenchido não cria `node`.
- Tracejadas aparecem.
- Busca por `sepse` mostra sepse + vizinhos.
- Links principais não dão 404.
