# PACOTE DE RESGATE DO SITE UPDOWN



---

# Arquivo: `README.md`

# 🚑 RESGATE DO SITE UPDOWN — pacote de recuperação

Este pacote é para corrigir a desintegração do site após reorganização de rotas/links.

## Diagnóstico provável

O problema provavelmente ocorreu porque a última atualização **substituiu ou mudou a estrutura de links** sem preservar:

- a página da Biblioteca com PDFs/Word;
- links dos Markdown/HTML já gerados;
- rotas antigas dos módulos UpDown;
- caminhos relativos entre páginas;
- páginas de índice intermediárias.

## Regra de emergência

Não reescrever o site inteiro agora.

Primeiro, restaurar acesso com uma camada de navegação segura:

1. criar um `index.html` de resgate;
2. recriar `/biblioteca/index.html`;
3. recriar `/updown/index.html`;
4. recriar `/imagens/index.html`;
5. recriar `/apps/index.html`;
6. mapear arquivos existentes sem mover nada;
7. só depois melhorar visual.

## Arquivos deste pacote

```text
00_LEIA_PRIMEIRO/PLANO_DE_RESGATE.md
01_RESTAURAR_ROTAS/index_resgate.html
01_RESTAURAR_ROTAS/mapa_de_rotas.md
02_BIBLIOTECA/biblioteca_index_recovery.md
03_UPDOWN/updown_index_recovery.md
04_IMAGENS/imagens_index_recovery.md
05_APPS/apps_index_recovery.md
06_ANTIGRAVITY/PROMPT_RESGATE_ANTIGRAVITY.md
06_ANTIGRAVITY/CHECKLIST_NAO_QUEBRAR_LINKS.md
manifest_resgate.json
```

## Uso

Cole a pasta no repositório e peça ao Antigravity para seguir o arquivo:

```text
06_ANTIGRAVITY/PROMPT_RESGATE_ANTIGRAVITY.md
```



---

# Arquivo: `00_LEIA_PRIMEIRO/PLANO_DE_RESGATE.md`

# Plano de resgate do site UpDown

## 1. Pare a reorganização visual

Antes de mexer em layout, restaurar acesso aos arquivos.

## 2. Não apagar nada

O Antigravity deve ser instruído a:

- não deletar PDFs;
- não deletar `.docx`;
- não deletar `.md`;
- não deletar `.html`;
- não mover arquivos sem atualizar todos os links;
- não substituir páginas de biblioteca por cards vazios.

## 3. Criar uma camada de rotas estáveis

Criar estas páginas mesmo que algumas fiquem simples inicialmente:

```text
/index.html
/updown/index.html
/biblioteca/index.html
/imagens/index.html
/apps/index.html
```

## 4. Restaurar a Biblioteca

A Biblioteca precisa listar todos os arquivos reais existentes no repositório:

- PDFs;
- Word `.docx`;
- Markdown `.md`;
- HTML leitor;
- ZIPs, se existirem.

Cada item deve ter link direto e descrição curta.

## 5. Restaurar UpDowns

A página `/updown/index.html` deve ter cards para:

- UPDOWN #001 — LES manifestações e diagnóstico;
- UPDOWN #002 — LES manejo e prognóstico;
- UPDOWN #003 — autoanticorpos anti-dsDNA, anti-Sm e anti-U1 RNP.

Cada card deve apontar preferencialmente para `index.html` do módulo, não para `.md`.

## 6. Restaurar Imagens

A página `/imagens/index.html` deve existir mesmo sem todas as imagens prontas.

Ela deve agrupar:

- imagens geradas;
- prompts privados não devem aparecer;
- placeholders podem aparecer como “em breve”.

## 7. Restaurar Apps

A página `/apps/index.html` deve listar:

- calculadora de drogas vasoativas;
- mapa de FAN;
- CAM-ICU/delirium;
- sepse/SOFA/qSOFA;
- Wells;
- Glasgow;
- SAPS3;
- Adrogué-Madias;
- NaCl mEq/mL.

## 8. Depois de restaurar, melhorar

Somente depois de todos os links funcionarem:

- melhorar cards;
- melhorar layout;
- melhorar busca;
- melhorar responsividade;
- organizar metadados.



---

# Arquivo: `01_RESTAURAR_ROTAS/index_resgate.html`

```html
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UpDown — Página de Resgate</title>
<style>
:root{--bg:#f6f7fb;--paper:#fff;--text:#1b2433;--muted:#68758a;--line:#e5e8f0;--accent:#3557ff;}
body{margin:0;background:var(--bg);color:var(--text);font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;}
main{max-width:1100px;margin:32px auto;padding:0 18px;}
.hero{background:var(--paper);border:1px solid var(--line);border-radius:26px;padding:28px;box-shadow:0 8px 30px rgba(20,30,60,.06);}
h1{margin:0 0 8px;font-size:2.2rem;letter-spacing:-.04em;}
p{color:var(--muted);}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px;}
.card{background:var(--paper);border:1px solid var(--line);border-radius:22px;padding:20px;text-decoration:none;color:var(--text);box-shadow:0 8px 24px rgba(20,30,60,.05);}
.card:hover{border-color:var(--accent);}
.card strong{font-size:1.2rem;}
.small{font-size:.92rem;color:var(--muted);}
.section{margin-top:28px;background:var(--paper);border:1px solid var(--line);border-radius:22px;padding:20px;}
ul{padding-left:22px;}
code{background:#eef2ff;padding:.15em .35em;border-radius:6px;}
@media(max-width:800px){.grid{grid-template-columns:1fr;}}
</style>
</head>
<body>
<main>
<section class="hero">
<h1>🚑 UpDown — Página de Resgate</h1>
<p>Esta página restaura acesso rápido aos módulos, biblioteca, imagens e aplicações enquanto a estrutura definitiva é reorganizada.</p>
<div class="grid">
<a class="card" href="./updown/index.html"><strong>📖 UpDowns</strong><br><span class="small">Conteúdos em modo leitor</span></a>
<a class="card" href="./biblioteca/index.html"><strong>📚 Biblioteca</strong><br><span class="small">PDFs, Word, Markdown e fontes</span></a>
<a class="card" href="./imagens/index.html"><strong>🖼️ Imagens</strong><br><span class="small">Cards, mapas e fluxogramas</span></a>
<a class="card" href="./apps/index.html"><strong>🧮 Aplicações</strong><br><span class="small">Calculadoras e escalas</span></a>
<a class="card" href="./questoes/index.html"><strong>🏆 Questões</strong><br><span class="small">Banco TEMI/R3</span></a>
<a class="card" href="./admin/index.html"><strong>🛠️ Admin</strong><br><span class="small">Área técnica privada</span></a>
</div>
</section>

<section class="section">
<h2>Triângulo principal</h2>
<ul>
<li><strong>UpDown</strong>: página pública em modo leitor.</li>
<li><strong>Biblioteca</strong>: arquivos-fonte e materiais de referência.</li>
<li><strong>Imagens</strong>: infográficos e mapas visuais relacionados.</li>
</ul>
</section>

<section class="section">
<h2>Regra de recuperação</h2>
<p>Se algum link estiver quebrado, não apagar o conteúdo. Criar card provisório apontando para o arquivo real encontrado no repositório.</p>
</section>
</main>
</body>
</html>

```


---

# Arquivo: `01_RESTAURAR_ROTAS/mapa_de_rotas.md`

# Mapa de rotas estáveis — UpDown

## Rotas obrigatórias

```text
/
├── index.html
├── updown/
│   └── index.html
├── biblioteca/
│   └── index.html
├── imagens/
│   └── index.html
├── apps/
│   └── index.html
└── questoes/
    └── index.html
```

## Rotas dos UpDowns

```text
/updown/001-les-manifestacoes/index.html
/updown/002-les-manejo/index.html
/updown/003-autoanticorpos/index.html
```

## Rotas de biblioteca

```text
/biblioteca/001-les-manifestacoes/
/biblioteca/002-les-manejo/
/biblioteca/003-autoanticorpos/
```

## Rotas de imagens

```text
/imagens/001-les-manifestacoes/
/imagens/002-les-manejo/
/imagens/003-autoanticorpos/
```

## Rotas de aplicações

```text
/apps/vasoativas/
/apps/fan/
/apps/delirium/
/apps/sepse/
/apps/wells/
/apps/glasgow/
/apps/saps3/
/apps/adroguemadias/
/apps/nacl/
```

## Regra

Rotas antigas devem ser preservadas com redirect simples ou links equivalentes.


---

# Arquivo: `02_BIBLIOTECA/biblioteca_index_recovery.md`

# Biblioteca — recuperação dos arquivos

> Página pública/semipública para recuperar acesso aos arquivos já gerados.

## Função

Listar todos os arquivos disponíveis no repositório:

- `.pdf`
- `.docx`
- `.md`
- `.html`
- `.zip`

## Bloco inicial sugerido

```markdown
# Biblioteca do Projeto UpDown

Esta área reúne os materiais-fonte e produtos gerados: PDFs, documentos Word, páginas HTML, Markdown e pacotes ZIP.

## UpDown #001 — LES manifestações e diagnóstico

- PDF fonte: inserir link se existir.
- HTML leitor: inserir link para `updown/001-les-manifestacoes/index.html`.
- Markdown público: inserir link direto.
- ZIP do módulo: inserir link direto se estiver no repositório.

## UpDown #002 — LES manejo e prognóstico

- PDF fonte: inserir link se existir.
- HTML leitor: inserir link para `updown/002-les-manejo/index.html`.
- Markdown público: inserir link direto.
- ZIP do módulo: inserir link direto se estiver no repositório.

## UpDown #003 — Autoanticorpos dsDNA, Sm e U1 RNP

- PDF fonte: inserir link se existir.
- HTML leitor: inserir link para `updown/003-autoanticorpos/index.html`.
- Markdown público: inserir link direto.
- ZIP do módulo: inserir link direto se estiver no repositório.
```

## Instrução para Antigravity

Escanear o repositório e montar automaticamente uma lista de arquivos por extensão, sem mover os arquivos.


---

# Arquivo: `03_UPDOWN/updown_index_recovery.md`

# Índice UpDown — recuperação

## Objetivo

Restaurar a navegação dos módulos UpDown.

## Cards obrigatórios

### UPDOWN #001 — LES manifestações clínicas e diagnóstico

- Abrir modo leitor: `/updown/001-les-manifestacoes/index.html`
- Biblioteca: `/biblioteca/001-les-manifestacoes/index.html`
- Imagens: `/imagens/001-les-manifestacoes/index.html`

### UPDOWN #002 — LES manejo, monitoramento e prognóstico

- Abrir modo leitor: `/updown/002-les-manejo/index.html`
- Biblioteca: `/biblioteca/002-les-manejo/index.html`
- Imagens: `/imagens/002-les-manejo/index.html`

### UPDOWN #003 — Autoanticorpos anti-dsDNA, anti-Sm e anti-U1 RNP

- Abrir modo leitor: `/updown/003-autoanticorpos/index.html`
- Biblioteca: `/biblioteca/003-autoanticorpos/index.html`
- Imagens: `/imagens/003-autoanticorpos/index.html`
- Aplicação relacionada: `/apps/fan/index.html`

## Regra

Se o arquivo HTML leitor ainda estiver em outra pasta, criar link provisório direto para o arquivo existente e depois padronizar.


---

# Arquivo: `04_IMAGENS/imagens_index_recovery.md`

# Imagens — recuperação da galeria

## Objetivo

Restaurar a página de imagens sem misturar prompts privados no site público.

## Estrutura sugerida

```text
/imagens/
├── index.html
├── 001-les-manifestacoes/
├── 002-les-manejo/
└── 003-autoanticorpos/
```

## Cards iniciais

### LES manifestações

- LES em 10 sinais de alerta
- LES ativo versus infecção
- Mapa sistêmico do LES

### LES manejo

- Corticoide é ponte, não casa
- FAROL de cada consulta
- Hidroxicloroquina sem erro

### Autoanticorpos

- Anti-dsDNA e rim
- Anti-Sm: selo do LES
- Anti-U1 RNP e DMTC
- FAN homogêneo versus pontilhado grosso

## Regra

Prompts e instruções de produção ficam fora da página pública.


---

# Arquivo: `05_APPS/apps_index_recovery.md`

# Aplicações extras — recuperação

## Objetivo

Restaurar acesso às ferramentas clínicas e deixar placeholders bem caracterizados.

## Cards

| Aplicação | Função | Status |
|---|---|---|
| Drogas vasoativas | dose ↔ mL/h, concentração e prescrição | revisar v2 |
| Mapa de FAN | padrões, ENA e autoanticorpos | em breve |
| Delirium/CAM-ICU | rastreio de delirium | em breve |
| Sepse/SOFA/qSOFA | triagem, gravidade e bundle | em breve |
| Wells | probabilidade TEP/TVP | em breve |
| Glasgow | escala neurológica | em breve |
| SAPS3 | gravidade UTI | em breve |
| Adrogué-Madias | correção de sódio | em breve |
| NaCl mEq/mL | preparo de solução salina | em breve |

## Regra

Aplicações futuras podem aparecer como “em breve”, mas com descrição clara.


---

# Arquivo: `06_ANTIGRAVITY/PROMPT_RESGATE_ANTIGRAVITY.md`

# PROMPT DE RESGATE PARA ANTIGRAVITY

Você está corrigindo um site do projeto Enciclomedia/UpDown que perdeu acesso aos arquivos após uma reorganização de rotas.

## Objetivo principal

Restaurar a navegação e os links sem apagar arquivos existentes.

## Instruções obrigatórias

1. Não delete nenhum arquivo `.pdf`, `.docx`, `.md`, `.html`, `.zip`, `.png`, `.jpg`, `.webp`.
2. Não mova arquivos sem atualizar todos os links.
3. Crie uma camada de resgate com:
   - `/index.html`
   - `/updown/index.html`
   - `/biblioteca/index.html`
   - `/imagens/index.html`
   - `/apps/index.html`
4. Escaneie o repositório e gere uma lista de todos os arquivos em PDF, Word, Markdown, HTML e ZIP.
5. Recrie a Biblioteca com links diretos para esses arquivos.
6. Recrie a página UpDown com cards para os módulos #001, #002 e #003.
7. Preserve o triângulo:
   - UpDown ↔ Biblioteca ↔ Imagens.
8. Não exiba prompts privados, sugestões internas ou bastidores na página pública.
9. Se algum destino não existir, criar placeholder “em breve” sem quebrar a navegação.
10. Antes de finalizar, validar que todos os links internos apontam para arquivos existentes ou placeholders reais.

## Tarefa imediata

Use o arquivo `01_RESTAURAR_ROTAS/index_resgate.html` como base para reconstruir a home temporária. Depois gere índices públicos para Biblioteca, UpDown, Imagens e Apps usando os arquivos Markdown deste pacote.

## Critério de sucesso

O site deve permitir ao usuário acessar novamente:

- PDFs;
- Word;
- Markdown;
- HTML leitor;
- ZIPs;
- módulos UpDown;
- aplicações extras.


---

# Arquivo: `06_ANTIGRAVITY/CHECKLIST_NAO_QUEBRAR_LINKS.md`

# Checklist — não quebrar links novamente

## Antes de publicar

- [ ] Fiz backup ou commit antes da alteração.
- [ ] Não apaguei nenhum arquivo de conteúdo.
- [ ] `/index.html` abre.
- [ ] `/biblioteca/index.html` abre.
- [ ] `/updown/index.html` abre.
- [ ] `/imagens/index.html` abre.
- [ ] `/apps/index.html` abre.
- [ ] PDFs aparecem na Biblioteca.
- [ ] Word aparece na Biblioteca.
- [ ] Markdown aparece na Biblioteca.
- [ ] HTML leitor aparece na Biblioteca.
- [ ] UpDown #001 abre.
- [ ] UpDown #002 abre.
- [ ] UpDown #003 abre.
- [ ] Links relativos foram testados.
- [ ] Links absolutos foram testados.
- [ ] Nenhuma página pública mostra prompt privado.
- [ ] Aplicações futuras aparecem como “em breve”, não como erro 404.

## Depois de publicar

- [ ] Abrir o site em aba anônima.
- [ ] Testar no celular.
- [ ] Clicar em 10 links aleatórios.
- [ ] Conferir se a Biblioteca mostra arquivos reais.


---

# Arquivo: `manifest_resgate.json`

```json
{
  "project": "UPDOWN_RESGATE_SITE_ANTIGRAVITY",
  "purpose": "Restaurar navegação e acesso a arquivos perdidos após reorganização do site.",
  "required_routes": [
    "/index.html",
    "/updown/index.html",
    "/biblioteca/index.html",
    "/imagens/index.html",
    "/apps/index.html"
  ],
  "do_not_delete_extensions": [
    ".pdf",
    ".docx",
    ".md",
    ".html",
    ".zip",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
  ],
  "updowns": [
    {
      "id": "001",
      "title": "LES manifestações clínicas e diagnóstico"
    },
    {
      "id": "002",
      "title": "LES manejo, monitoramento e prognóstico"
    },
    {
      "id": "003",
      "title": "Autoanticorpos anti-dsDNA, anti-Sm e anti-U1 RNP"
    }
  ],
  "navigation_model": "UPDOWN <-> BIBLIOTECA <-> IMAGENS",
  "apps_placeholders": [
    "vasoativas",
    "fan",
    "delirium/cam-icu",
    "sepse/sofa/qsofa",
    "wells",
    "glasgow",
    "saps3",
    "adrogué-madias",
    "nacl-meq-ml"
  ]
}
```
