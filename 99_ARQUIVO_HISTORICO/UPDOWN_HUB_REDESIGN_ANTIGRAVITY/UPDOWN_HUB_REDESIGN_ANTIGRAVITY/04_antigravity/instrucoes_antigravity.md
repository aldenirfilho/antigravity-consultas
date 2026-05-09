# Instruções prontas para Antigravity — refatoração da página UpDown

## Objetivo

Refatorar a página principal do projeto UpDown para ficar mais clara, navegável e conectada com Biblioteca, Imagens e Aplicações Extras.

---

# 1. Tarefas principais

## 1.1 Remover blocos ruins

Remover da página pública:

- bloco de templates genéricos;
- bloco de conexão com VM;
- qualquer item sem descrição clínica clara.

Não apagar definitivamente se houver risco de perda; mover para área privada ou comentar no código.

---

## 1.2 Criar triângulo de navegação

Adicionar seção visual:

```text
UPDOWN ↔ BIBLIOTECA ↔ IMAGENS
```

Cada card deve ter:

- título;
- descrição curta;
- botão principal;
- contador;
- últimos adicionados.

---

## 1.3 Melhorar aplicações extras

Criar seção:

```text
Aplicações extras para plantão e UTI
```

Cards iniciais:

- Calculadora de drogas vasoativas;
- Mapa de FAN;
- Delirium/CAM-ICU;
- Sepse + SOFA/qSOFA;
- Wells;
- Glasgow;
- SAPS 3;
- Adrogué-Madias;
- NaCl mEq/mL.

---

## 1.4 Atualizar calculadora de drogas vasoativas

Usar os documentos:

```text
03_calculadoras/calculadora_drogas_vasoativas_v2.md
03_calculadoras/especificacao_formula_mlh_dose.md
03_calculadoras/prescricoes_comuns_brasil_vasoativas.md
05_data/vasoactive_drugs_brasil_presets.json
```

Implementar:

- seleção da droga;
- apresentação da ampola;
- número de ampolas;
- volume final;
- concentração automática;
- cálculo dose → mL/h;
- cálculo mL/h → dose;
- prescrição formatada;
- alertas de segurança.

---

# 2. Rotas sugeridas

Criar ou ajustar:

```text
/updown/index.html
/biblioteca/index.html
/imagens/index.html
/apps/index.html
/apps/vasoativas/index.html
```

Preparar placeholders:

```text
/apps/fan/index.html
/apps/delirium/index.html
/apps/sepse/index.html
/apps/wells/index.html
/apps/glasgow/index.html
/apps/saps3/index.html
/apps/adroguemadias/index.html
/apps/nacl/index.html
```

---

# 3. Prompt operacional para Antigravity

```text
Refatore a página principal do projeto UpDown usando os arquivos Markdown deste pacote como especificação. Remova os blocos pouco claros de templates e conexão com VM da página pública. Crie uma navegação central em triângulo entre UpDown, Biblioteca e Imagens. Mantenha uma seção de Aplicações Extras para ferramentas de plantão/UTI. Melhore a calculadora de drogas vasoativas usando presets brasileiros, cálculo dose↔mL/h, concentração por ampola/volume final e prescrição formatada. Prepare placeholders para Mapa de FAN, Delirium/CAM-ICU, Sepse/SOFA/qSOFA, Wells, Glasgow, SAPS3, Adrogué-Madias e NaCl mEq/mL. A página deve ser intuitiva, responsiva e em modo leitor. Não exibir prompts internos nem notas privadas ao público.
```

---

# 4. Critérios de aceitação

A implementação estará boa quando:

- a página UpDown abrir sem Markdown bruto;
- houver cards claros para UpDown, Biblioteca e Imagens;
- aplicações extras estiverem agrupadas e compreensíveis;
- a calculadora de vasoativas aceitar apresentações comuns;
- prescrição formatada puder ser copiada;
- houver alertas de segurança;
- placeholders dos próximos apps estiverem visíveis mas marcados como “em breve”;
- não houver bastidores ou prompts no site público.
