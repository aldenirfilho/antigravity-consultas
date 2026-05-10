# Regras de Segurança — updown-integrator

## Regras obrigatórias
1. **Nunca publicar prompts internos**
   - Proibido expor instruções de sistema, cadeia de raciocínio, notas operacionais internas ou chaves.

2. **Nunca copiar conteúdo proprietário sem autorização**
   - Exigir confirmação de licença/permissão para conteúdo de terceiros.
   - Quando não houver permissão, produzir resumo original em vez de cópia literal.

3. **Não incluir dados pessoais ou clínicos reais**
   - Usar apenas conteúdo educacional anonimizado/fictício.

4. **Preservar integridade do site estático**
   - Não introduzir dependências obrigatórias de build para publicar um UpDown.

5. **Validar links e rotas antes da entrega**
   - Nenhum card deve ser finalizado com caminho inválido.

## Bloqueios de publicação (hard stop)
- Detectou prompt interno? **Bloquear publicação**.
- Detectou potencial infração autoral? **Bloquear publicação**.
- Detectou link quebrado sem correção? **Bloquear publicação**.
