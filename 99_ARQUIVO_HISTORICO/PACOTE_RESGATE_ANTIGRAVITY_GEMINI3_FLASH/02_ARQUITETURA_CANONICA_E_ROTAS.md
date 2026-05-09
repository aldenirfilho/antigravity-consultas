# 02 — Arquitetura canônica e rotas públicas

## Objetivo

Impedir que o site se desintegre novamente por múltiplos `index.html`, pacotes de resgate e caminhos concorrentes.

## Rotas canônicas

| Rota pública | Arquivo | Função | Ação |
|---|---|---|---|
| `/` | `index.html` | Home principal | manter, corrigir links |
| `/updown/` | `updown/index.html` | atalho público estável | wrapper para `07_Estudos_Markdown/` |
| `/07_Estudos_Markdown/` | `07_Estudos_Markdown/index.html` | hub UpDown canônico | corrigir renderização |
| `/biblioteca/` | `biblioteca/index.html` | biblioteca pública | reconstruir dinâmica |
| `/05_Biblioteca_IA/` | `05_Biblioteca_IA/index.html` | acervo legado/canônico | corrigir 0 arquivos |
| `/imagens/` | `imagens/index.html` | galeria pública | wrapper para hub de imagens |
| `/apps/` | `apps/index.html` | apps públicos | wrapper para apps |
| `/03_Calculadoras_UTI/` | `03_Calculadoras_UTI/index.html` | calculadoras UTI | preservar |
| `/questoes/` | `questoes/index.html` | atalho de questões | wrapper |
| `/02_Banco_Questoes_TEMI/` | `02_Banco_Questoes_TEMI/index.html` | banco TEMI | preservar |

## Não usar como navegação principal

Pastas como abaixo são **pacotes de implementação/documentação**, não devem dominar a home:

```txt
PACOTE_*
UPDOWN_RESGATE_SITE_ANTIGRAVITY/
UPDOWN_HUB_REDESIGN_ANTIGRAVITY/
enciclopedia_markdown_updown_upgrade_v3/
mapa_vivo_editavel_3_1_antigravity/
backups/
```

Elas podem permanecer acessíveis via documentação técnica, mas não como rota clínica principal.

## `route_aliases.json` sugerido

```json
{
  "aliases": [
    {"from": "questoes/index.html", "to": "02_Banco_Questoes_TEMI/index.html"},
    {"from": "updown/index.html", "to": "07_Estudos_Markdown/index.html"},
    {"from": "biblioteca/index.html", "to": "05_Biblioteca_IA/index.html"},
    {"from": "imagens/index.html", "to": "07_Estudos_Markdown/imagens/index.html"},
    {"from": "apps/index.html", "to": "07_Estudos_Markdown/apps/index.html"}
  ]
}
```

## Wrapper HTML seguro

Quando uma rota antiga existir, não apagar. Trocar por um wrapper elegante:

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="refresh" content="0; url=../07_Estudos_Markdown/index.html" />
  <title>Redirecionando...</title>
</head>
<body>
  <p>Redirecionando para o hub correto...</p>
  <p><a href="../07_Estudos_Markdown/index.html">Abrir manualmente</a></p>
</body>
</html>
```

Adaptar `href` conforme a rota.
