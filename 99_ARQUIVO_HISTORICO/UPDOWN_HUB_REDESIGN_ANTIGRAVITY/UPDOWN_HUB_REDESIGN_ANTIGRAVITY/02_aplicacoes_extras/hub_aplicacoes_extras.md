# Hub de Aplicações Extras — Plantão, UTI e estudo

> Área modular para ferramentas práticas que serão adicionadas e melhoradas continuamente.

---

# 1. Princípio

As aplicações extras não devem parecer links soltos. Cada uma precisa ter:

- nome claro;
- finalidade clínica;
- entrada de dados;
- saída esperada;
- avisos de segurança;
- link para UpDowns relacionados;
- status de desenvolvimento.

---

# 2. Aplicações prioritárias

| Aplicação | Uso no plantão/UTI | Status inicial |
|---|---|---|
| Calculadora de drogas vasoativas | Converter dose ↔ mL/h e gerar prescrição padronizada | revisar e publicar v2 |
| Mapa de FAN | Interpretar FAN, ENA e autoanticorpos | abrir estrutura |
| Delirium/CAM-ICU | Rastrear delirium na UTI | abrir estrutura |
| Sepse + SOFA/qSOFA | Triagem, gravidade, bundle e reavaliação | abrir estrutura |
| Wells TEP/TVP | Probabilidade pré-teste | abrir estrutura |
| Glasgow | Avaliação neurológica | abrir estrutura |
| SAPS 3 | Prognóstico e gravidade UTI | abrir estrutura |
| Adrogué-Madias | Prever variação do sódio sérico | abrir estrutura |
| NaCl mEq/mL | Preparar soluções de NaCl e calcular mEq | abrir estrutura |

---

# 3. Card padrão de aplicação

```markdown
## Calculadora de drogas vasoativas

**Finalidade:** converter dose prescrita em mL/h e gerar prescrição padronizada com concentração e ampolas.  
**Público:** médicos, UTI, emergência, enfermaria monitorizada.  
**Status:** v2 em revisão contínua.  
**Segurança:** exige conferência com protocolo institucional e farmácia.

[Abrir calculadora] [Ver instruções] [Reportar erro] [Ver fontes]
```

---

# 4. Categorias

## Hemodinâmica

- drogas vasoativas;
- choque séptico;
- choque cardiogênico;
- nitroprussiato/nitroglicerina;
- Wells TEP/TVP.

## Neurologia/UTI

- Glasgow;
- CAM-ICU;
- delirium;
- sedação;
- RASS futuro.

## Sepse e gravidade

- qSOFA;
- SOFA;
- SAPS 3;
- bundle sepse.

## Distúrbios hidroeletrolíticos

- Adrogué-Madias;
- NaCl 3%;
- NaCl 20%;
- cálculo de mEq;
- velocidade de correção do sódio.

## Imunologia/Reumatologia

- mapa de FAN;
- ENA;
- antifosfolipídios;
- atividade de LES.

---

# 5. Rotas sugeridas

```text
/apps/index.html
/apps/vasoativas/index.html
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

# 6. Aviso padrão

> Ferramenta educacional e de apoio. Conferir apresentação disponível, diluição institucional, bomba de infusão, via de administração, compatibilidade, função renal/hepática, peso utilizado e metas clínicas antes de prescrever.
