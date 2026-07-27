# 🔄 Sincronização segura: Mac Air, Mac Pro e web

> **Objetivo:** editar e acompanhar o Antigravity em qualquer Mac ou navegador
> sem duplicar arquivos, sobrescrever trabalho nem expor conteúdo privado.

## 🚨 Regra principal

Use **um único centro de verdade para cada tipo de conteúdo**:

| Conteúdo | Fonte oficial | Para que serve |
|---|---|---|
| Código e conteúdo publicável | GitHub, branch `main` | Sincronizar versões, revisar mudanças e publicar o site |
| Edição em andamento | Branch própria no GitHub | Isolar cada alteração até a revisão |
| Site publicado | GitHub Pages | Visualizar a versão aprovada pelo público |
| Notas privadas do Obsidian | iCloud **ou** Obsidian Sync, nunca os dois juntos | Notas pessoais e rascunhos não publicáveis |
| Materiais com dados pessoais ou de pacientes | Armazenamento privado fora do repositório | Preservar LGPD, sigilo e privacidade |

**Não mantenha o repositório Git ativo dentro do iCloud Drive.** O iCloud
sincroniza arquivo por arquivo, inclusive os milhares de objetos internos da
pasta `.git`, e pode produzir cópias de conflito como `arquivo 2.md`. O GitHub
sincroniza commits e é o mecanismo adequado para conciliar edições de código.

## ✅ Estado implantado no Mac Air

- Clone canônico local:
  `/Users/aldenirfilho/Projects/antigravity-consultas`
- Repositório web:
  <https://github.com/aldenirfilho/antigravity-consultas>
- Site público:
  <https://aldenirfilho.github.io/antigravity-consultas/>
- Atualização local configurada como `fast-forward only`: o Git interrompe em
  vez de criar um merge automático inesperado.
- A pasta antiga do iCloud foi preservada para conferência. Trate-a como
  **arquivo legado somente leitura** até a quarentena dos conflitos ser
  explicitamente aprovada.

## 🍎 Configurar o Mac Pro

### Opção visual recomendada: GitHub Desktop

1. No Mac Pro, acesse <https://desktop.github.com/>.
2. Baixe e instale o **GitHub Desktop**.
3. Abra o app e escolha **Sign in to GitHub.com**.
4. Autorize pelo navegador usando a conta `aldenirfilho`.
5. No GitHub Desktop, selecione **File → Clone Repository**.
6. Escolha `aldenirfilho/antigravity-consultas`.
7. Em **Local Path**, use uma pasta local fora do iCloud:
   `~/Projects/antigravity-consultas`.
8. Clique em **Clone**.
9. Confirme que a branch selecionada é `main`.
10. Clique em **Fetch origin** e, se aparecer, **Pull origin**.

### Opção Terminal

```bash
mkdir -p ~/Projects
git clone --filter=blob:none --single-branch --branch main \
  https://github.com/aldenirfilho/antigravity-consultas.git \
  ~/Projects/antigravity-consultas
cd ~/Projects/antigravity-consultas
git config pull.ff only
git config fetch.prune true
git config fetch.pruneTags true
git config push.default current
git config core.autocrlf input
git config core.precomposeunicode true
git config rerere.enabled true
git config rerere.autoupdate false
```

Depois, abra **essa pasta local** no Codex, VS Code ou editor escolhido. Não abra
a cópia antiga do iCloud para editar o site.

## 🌐 Acessar e editar pela web

### Visualizar o código

Abra:
<https://github.com/aldenirfilho/antigravity-consultas>

O repositório é público. Portanto, **nunca adicione** prontuários, nomes de
pacientes, documentos familiares, financeiros ou jurídicos, senhas, tokens,
arquivos `.env` ou rascunhos privados.

### Editor web completo

1. Abra o repositório no GitHub.
2. Pressione a tecla `.` ou acesse
   <https://github.dev/aldenirfilho/antigravity-consultas>.
3. Antes de editar, crie ou selecione uma branch própria.
4. Edite os arquivos.
5. Abra **Source Control**.
6. Revise a lista de arquivos alterados.
7. Escreva uma mensagem curta e clique em **Commit & Push**.
8. Crie um Pull Request para `main`.

Nunca edite `main` simultaneamente no navegador e em um Mac.

### ChatGPT e Codex

Para o ChatGPT web **ler e pesquisar** o repositório:

1. Abra **Configurações → Apps → GitHub**.
2. Conecte a conta do GitHub.
3. Em **Choose repositories**, autorize somente
   `aldenirfilho/antigravity-consultas`.
4. Aguarde a indexação. Se o projeto não aparecer, pesquise no GitHub:
   `repo:aldenirfilho/antigravity-consultas import`.

O app GitHub do ChatGPT é voltado à leitura e análise. Para alterações, commits
e Pull Requests, use o Codex com o repositório GitHub conectado ou trabalhe no
clone local. A disponibilidade das superfícies web pode variar conforme plano e
workspace.

## 🔁 Ritual de edição sem conflitos

### Antes de começar — 30 segundos

1. Confirme em qual Mac e branch você está.
2. Feche o projeto no outro Mac.
3. Verifique se não existem mudanças locais pendentes.
4. Atualize `main`.
5. Crie uma branch nova a partir da `main`.

No Terminal:

```bash
cd ~/Projects/antigravity-consultas
bash scripts_admin/sincronizar_git_seguro.sh
git switch -c codex/descricao-curta-da-tarefa
```

Ou dê duplo clique em `sincronizar_codigo_seguro.command` no Finder.

### Durante a edição

- Trabalhe em **uma tarefa por branch**.
- Faça commits pequenos.
- Não use a mesma branch em dois Macs ao mesmo tempo.
- Não copie manualmente a pasta inteira entre Macs.
- Não arraste a pasta `.git` pelo Finder, AirDrop ou iCloud.

### Ao terminar

1. Execute os testes relevantes.
2. Revise `git status` e `git diff`.
3. Faça commit apenas dos arquivos da tarefa.
4. Envie a branch ao GitHub.
5. Abra um Pull Request em rascunho.
6. Aguarde os testes e faça a revisão humana.
7. Só então faça o merge em `main`.

### Para continuar no outro Mac

1. Finalize e envie o trabalho do primeiro Mac.
2. Feche o editor no primeiro Mac.
3. No segundo Mac, abra o clone local.
4. Se a tarefa foi incorporada:

```bash
git switch main
bash scripts_admin/sincronizar_git_seguro.sh
```

5. Se precisa continuar uma branch ainda aberta:

```bash
git fetch --prune origin
git switch nome-da-branch
git pull --ff-only
```

## ☁️ Por que a pasta antiga pode não aparecer no Mac Pro ou no iCloud.com?

A pasta antiga está dentro do contêiner do Obsidian:

```text
iCloud Drive/Obsidian/Comando Central/Antigravity_Consultas
```

No Mac Pro:

1. Abra **Ajustes do Sistema → Conta Apple → iCloud → Drive**.
2. Ative **Sincronizar este Mac**.
3. Abra **Apps sincronizados com o iCloud Drive**.
4. Ative **Obsidian**.
5. Confirme que os dois Macs usam a **mesma Conta Apple**.
6. No Finder, abra **iCloud Drive → Obsidian → Comando Central**.
7. No Obsidian, abra o seletor de cofres e escolha **Open folder as vault**.

No iCloud.com, abra <https://www.icloud.com/iclouddrive/>. Dados de apps de
terceiros nem sempre aparecem como pastas navegáveis na web, mesmo quando usam
armazenamento do iCloud. Por isso, use o **GitHub** para acompanhar o projeto
pela web.

Se optar pelo Obsidian Sync no futuro, mova primeiro o cofre para fora do iCloud.
Não use iCloud e Obsidian Sync ao mesmo tempo no mesmo cofre.

## 🆘 Se aparecer conflito

Pare e não clique em “Discard”, não apague arquivos e não force um pull.

```bash
git status --short --branch
git diff
```

Registre:

- Mac usado;
- caminho da pasta aberta;
- branch atual;
- arquivos listados;
- última ação executada.

Peça uma revisão antes de mover, apagar, renomear, fazer `reset`, `clean`,
`checkout --` ou `push --force`.

## 🧠 Checklist TDAH-friendly

Antes de editar, repita:

> **MAC CERTO → PASTA LOCAL → MAIN ATUALIZADA → BRANCH PRÓPRIA → EDITAR**

Antes de publicar:

> **STATUS → DIFF → TESTES → COMMIT → PUSH → PR → REVISÃO → MERGE**

## 📚 Referências oficiais

- Apple — configurar o iCloud Drive:
  <https://support.apple.com/pt-br/118443>
- Apple — configurar iCloud para apps de terceiros:
  <https://support.apple.com/guide/icloud/mmfeb236a772/icloud>
- Obsidian — sincronizar notas entre dispositivos:
  <https://obsidian.md/help/sync-notes>
- GitHub — configurar o GitHub Desktop:
  <https://docs.github.com/desktop/installing-and-authenticating-to-github-desktop/setting-up-github-desktop>
- GitHub — editor `github.dev`:
  <https://docs.github.com/codespaces/the-githubdev-web-based-editor>
- OpenAI — conectar o GitHub ao ChatGPT:
  <https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt-deep-resear>
- OpenAI — usar o Codex com o plano ChatGPT:
  <https://help.openai.com/en/articles/11369540>
