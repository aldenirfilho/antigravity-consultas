# Checklist de validação — UpDown Integrator

## 1) Descoberta
- [ ] Foram verificados novos `.md` em `00_INBOX_ATUALIZACAO/03_Conteudos_UpDown_MD`.
- [ ] O arquivo selecionado está legível e sem corrupção.

## 2) Segurança
- [ ] Não há prompts internos/instruções de sistema no conteúdo final.
- [ ] Não há segredos, tokens, chaves, e-mails privados ou dados sensíveis.
- [ ] Não há dados reais de pacientes.
- [ ] O conteúdo não viola propriedade intelectual/licenciamento.

## 3) Manifesto
- [ ] Card criado no manifesto UpDown.
- [ ] `id` é único.
- [ ] `path` resolve sem erro.
- [ ] `title` e `category` estão consistentes.

## 4) Conexões
- [ ] Biblioteca conectada (`biblioteca_refs`) quando aplicável.
- [ ] Imagens conectadas (`imagens_refs`) quando aplicável.
- [ ] Questões conectadas (`questoes_refs`) quando aplicável.

## 5) Rotas e compatibilidade
- [ ] Rotas antigas preservadas (ou mapeadas em `legacy_routes`).
- [ ] Nenhum arquivo público crítico foi removido/movido sem plano.

## 6) Validação de links
- [ ] Links internos do Markdown testados.
- [ ] Links do card no manifesto testados.
- [ ] Nenhum 404 encontrado nas rotas adicionadas.

## 7) Encerramento
- [ ] Alterações documentadas com resumo objetivo.
- [ ] Commit pequeno, auditável e reversível.
