# 🧠 Mapa Vivo Editável 3.1 — Pacote pronto para Antigravity

Este pacote corrige e expande o Mapa Vivo do repositório:

`aldenirfilho/antigravity-consultas`

## O que ele resolve

✅ Incluir temas pelo painel de curadoria  
✅ Ocultar/excluir temas com segurança, sem apagar fisicamente  
✅ Editar temas selecionados  
✅ Criar conexão direta com linha contínua  
✅ Criar conexão sugerida com linha tracejada  
✅ Aprovar/rejeitar conexão sugerida  
✅ Exportar/copiar patch JSON  
✅ Busca, filtros, zoom, reset, drawer robusto e fallback seguro  

## Arquivos do pacote

Copie para a raiz do repositório:

```txt
assets/js/graph.js
assets/css/graph-vivo.css
data/connections.json
data/mapa_vivo_schema_v3.json
data/mapa_vivo_admin_config.json
templates/TEMPLATE_PATCH_MAPA_VIVO_ADMIN.json
scripts/validate_mapa_vivo.py
08_Documentacao_Projeto/RELATORIO_MAPA_VIVO_EDITAVEL_3_1.md
index_demo_mapa_vivo.html
```

## Antes de substituir

Crie backup lógico dos arquivos atuais:

```txt
index.html
assets/js/graph.js
assets/css/graph-vivo.css
data/connections.json
```

Sugestão de pasta:

```txt
08_Documentacao_Projeto/backups/mapa-vivo-antes-3-1/
```

## Conferir index.html

No `<head>` precisa existir:

```html
<link rel="stylesheet" href="assets/css/graph-vivo.css" />
<script src="https://d3js.org/d3.v7.min.js"></script>
```

Antes de `</body>` precisa existir:

```html
<script src="assets/js/graph.js"></script>
```

Na seção do mapa, garantir:

```html
<section id="mapa">
  <div id="graph"></div>
</section>
```

## Teste rápido

1. Abrir `index_demo_mapa_vivo.html`.
2. Verificar linhas contínuas.
3. Verificar linhas tracejadas.
4. Clicar em um nó.
5. Abrir `🛠️ Curadoria`.
6. Adicionar novo tema.
7. Adicionar conexão sugerida.
8. Ocultar tema.
9. Exportar patch JSON.

## Validação

No terminal do Antigravity:

```bash
python3 scripts/validate_mapa_vivo.py data/connections.json
```

## Commit sugerido

```txt
Upgrade Mapa Vivo editável 3.1 com curadoria e linhas tracejadas
```
