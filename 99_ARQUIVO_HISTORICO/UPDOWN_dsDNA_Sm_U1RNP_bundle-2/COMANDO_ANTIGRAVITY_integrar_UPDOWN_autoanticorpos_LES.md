# 🧩 ORDEM PARA ANTIGRAVITY — Integrar UPDOWN autoanticorpos no LES

## Missão
Integrar ao projeto **Antigravity Consultas** o novo conteúdo público:

**UPDOWN — Autoanticorpos no LES: anti-dsDNA, anti-Sm e anti-U1 RNP**

## Regra de segurança máxima
Antes de qualquer alteração:

1. Criar backup ou branch de segurança.
2. Ler o inventário real do repositório.
3. Não deletar, mover ou renomear arquivos existentes sem atualizar manifestos, links e redirecionamentos.
4. Preservar rotas antigas da Biblioteca, UpDowns, Imagens e Apps.
5. Não reorganizar visual global do site nesta tarefa.

## Arquivos recebidos
- `UPDOWN_autoanticorpos_LES_dsDNA_Sm_U1RNP.md`
- `updown-autoanticorpos-les-dsdna-sm-u1rnp.html`
- `updown-autoanticorpos-les-dsdna-sm-u1rnp.json`

## Onde colocar
Seguir a arquitetura manifest-first:

1. Markdown original:
   - `00_INBOX_ATUALIZACAO/03_Conteudos_UpDown_MD/UPDOWN_autoanticorpos_LES_dsDNA_Sm_U1RNP.md`

2. Página pública HTML:
   - `01_UpDown_Hub/autoanticorpos-les-dsdna-sm-u1rnp/index.html`

3. Manifesto/metadados:
   - se existir manifesto central de UpDowns, adicionar o item sem sobrescrever a lista;
   - se não existir, criar/atualizar um JSON compatível preservando itens anteriores.

## Links internos obrigatórios
Adicionar este módulo aos hubs sem quebrar rotas:

- Página principal do UpDown.
- Biblioteca IA / Reumatologia / LES.
- Hub de Imagens, como conteúdo relacionado.
- Futuro módulo de Nefrite Lúpica.
- Futuro módulo de FAN e padrões de imunofluorescência.

## Título público
`Autoanticorpos no LES: anti-dsDNA, anti-Sm e anti-U1 RNP`

## Descrição curta para card
`Guia didático para interpretar anti-dsDNA, anti-Sm e anti-U1 RNP: diagnóstico, atividade, nefrite lúpica, DMTC e armadilhas laboratoriais.`

## Tags
`LES`, `lúpus`, `anti-dsDNA`, `anti-Sm`, `anti-U1 RNP`, `FAN`, `nefrite lúpica`, `DMTC`, `Reumatologia`, `Clínica Médica`, `UTI`.

## Regras de conteúdo público
- Não inserir bastidores, prompts internos, instruções privadas ou menções de “copiar UpToDate”.
- Não reproduzir texto proprietário.
- Manter linguagem original, didática, estilo UpDown.
- Manter modo leitor limpo.
- Não mostrar prompts de imagens dentro da página pública.

## Sugestões privadas de imagens para gerar depois
1. **Wallpaper 1080×1920:** “Autoanticorpos no LES em 1 tela: dsDNA, Sm, U1 RNP”.
2. **Infográfico 16:9:** “Como interpretar anti-dsDNA: método, tendência, complemento e rim”.
3. **Mapa visual 1080×1920:** “Nefrite lúpica: DNA + complemento + urina”.
4. **Card feed:** “Anti-Sm = selo específico, baixa sensibilidade”.
5. **Card feed:** “Anti-U1 RNP alto: pense DMTC/sobreposição”.

## Checklist pós-integração
- [ ] Página abre diretamente pela rota sugerida.
- [ ] Link aparece no hub UpDown.
- [ ] Link aparece na Biblioteca/Reumatologia.
- [ ] Link aparece no triângulo UPDOWN ↔ Biblioteca ↔ Imagens.
- [ ] Não houve sumiço de PDFs, DOCX, MD ou páginas antigas.
- [ ] Busca interna encontra: dsDNA, anti-Sm, U1 RNP, nefrite lúpica, DMTC.
- [ ] Página mobile está legível.
- [ ] Tabelas não quebram em tela pequena.

## Resultado esperado
Uma nova página pública estável, responsiva e integrada ao ecossistema Antigravity, sem desorganizar o repositório.
