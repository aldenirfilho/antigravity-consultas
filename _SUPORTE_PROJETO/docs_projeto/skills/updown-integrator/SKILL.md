# Skill: updown-integrator

## Objetivo
Integrar com segurança conteúdos Markdown de UpDown ao projeto **Antigravity Consultas** sem quebrar rotas antigas, sem exposição de prompts internos e sem vazamento de conteúdo proprietário.

## Quando usar
Use esta Skill sempre que houver novos arquivos `.md` em:

- `00_INBOX_ATUALIZACAO/03_Conteudos_UpDown_MD`

## Escopo e limites
- ✅ Integrar conteúdo novo em formato Markdown (UpDown).
- ✅ Atualizar manifesto UpDown com novo card.
- ✅ Conectar o conteúdo aos índices de Biblioteca, Imagens e Questões quando aplicável.
- ✅ Preservar compatibilidade com rotas antigas.
- ❌ Não publicar prompts internos.
- ❌ Não copiar conteúdo proprietário sem permissão explícita.
- ❌ Não alterar design global durante a integração de conteúdo.

## Fluxo operacional (passo a passo)
1. **Descobrir novos arquivos**
   - Inspecionar `00_INBOX_ATUALIZACAO/03_Conteudos_UpDown_MD`.
   - Selecionar apenas arquivos `.md` elegíveis para publicação.

2. **Triagem de segurança e propriedade intelectual**
   - Remover/mascarar qualquer prompt interno, instruções de sistema, tokens, segredos ou dados sensíveis.
   - Validar se o conteúdo não é proprietário/restrito sem autorização.

3. **Mapear destino público**
   - Definir caminho de publicação em `updown/` (e espelho em `public_site/updown/`, quando aplicável ao fluxo do repositório).
   - Evitar renomeações desnecessárias e manter URLs estáveis.

4. **Criar card no manifesto UpDown**
   - Adicionar entrada no manifesto usando o template desta Skill.
   - Garantir `id` único, `title` claro, `path` válido e metadados mínimos.

5. **Conectar com Biblioteca, Imagens e Questões**
   - Criar/atualizar conexões semânticas:
     - `biblioteca_refs`
     - `imagens_refs`
     - `questoes_refs`
   - Não duplicar links já existentes.

6. **Preservar rotas antigas**
   - Se houver alteração de caminho, manter alias/redirect estático ou arquivo-ponte.
   - Atualizar manifests para continuidade de navegação.

7. **Validar links antes de finalizar**
   - Verificar links internos/externos do novo card e do conteúdo `.md`.
   - Garantir ausência de `404` nas rotas citadas.

8. **Fechar com checklist**
   - Executar `checklists/validacao-updown.md` e registrar status.

## Arquivos da Skill
- `templates/updown_manifest_card.template.json`
- `templates/connections_patch.template.json`
- `checklists/validacao-updown.md`
- `examples/tarefa_exemplo.md`
- `SECURITY_RULES.md`

## Como usar (rápido)
1. Abra `examples/tarefa_exemplo.md` e adapte para a tarefa atual.
2. Crie o card com base em `templates/updown_manifest_card.template.json`.
3. Atualize conexões usando `templates/connections_patch.template.json`.
4. Rode a checklist em `checklists/validacao-updown.md`.
5. Só finalize após validação de links e segurança.
