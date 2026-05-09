# Roadmap de calculadoras padronizadas — UTI e plantão

Este documento prepara a abertura dos próximos tópicos extras.

---

# 1. Vasoativas v2

## Campos

- peso;
- droga;
- apresentação;
- número de ampolas;
- volume final;
- concentração calculada;
- dose alvo;
- unidade de dose;
- resultado em mL/h;
- texto de prescrição.

## Saídas

- concentração final;
- dose ↔ mL/h;
- prescrição pronta;
- alertas de segurança.

---

# 2. Mapa de FAN

## Campos

- padrão FAN;
- título;
- autoanticorpos associados;
- manifestações clínicas;
- suspeita principal.

## Saídas

- interpretação provável;
- diagnósticos associados;
- próximos exames sugeridos;
- alertas de falso positivo.

---

# 3. Delirium / CAM-ICU

## Campos

- alteração aguda/flutuante;
- inatenção;
- nível de consciência;
- pensamento desorganizado;
- RASS.

## Saídas

- CAM-ICU positivo/negativo;
- conduta inicial;
- fatores precipitantes;
- bundle não farmacológico.

---

# 4. Sepse / SOFA / qSOFA

## Campos

- PA/PAM;
- FR;
- Glasgow;
- PaO2/FiO2 ou SatO2;
- plaquetas;
- bilirrubina;
- creatinina/diurese;
- vasopressor;
- lactato.

## Saídas

- qSOFA;
- SOFA estimado;
- suspeita de disfunção orgânica;
- bundle inicial;
- necessidade de UTI.

---

# 5. Wells TEP/TVP

## Campos

- sinais de TVP;
- TEP mais provável;
- frequência cardíaca;
- imobilização/cirurgia;
- TVP/TEP prévio;
- hemoptise;
- câncer ativo.

## Saídas

- pontuação;
- probabilidade;
- próximo passo diagnóstico conforme risco.

---

# 6. Glasgow

## Campos

- abertura ocular;
- resposta verbal;
- resposta motora;
- intubação/sedação;
- pupilas futuro.

## Saídas

- ECG total;
- classificação;
- alerta para via aérea/neuroimagem.

---

# 7. SAPS 3

## Campos

- idade;
- comorbidades;
- procedência;
- motivo de admissão;
- variáveis fisiológicas;
- suporte recebido.

## Saídas

- SAPS 3 estimado;
- mortalidade estimada;
- aviso de uso institucional/epidemiológico.

---

# 8. Adrogué-Madias

## Campos

- sódio atual;
- potássio da solução;
- sódio da solução;
- água corporal total estimada;
- volume infundido.

## Saídas

- variação prevista do sódio;
- alerta de correção rápida;
- comparação entre soluções.

---

# 9. Soluções de NaCl em mEq e mL

## Campos

- concentração disponível: NaCl 0,9%, 3%, 10%, 20%;
- volume desejado;
- mEq desejados;
- volume da ampola;
- concentração em mEq/mL.

## Saídas

- mEq totais;
- mL necessários;
- sugestão de preparo;
- alerta de osmolaridade e via de administração.

---

# 10. Evolução contínua

```text
v1: cálculo básico
v2: prescrição formatada
v3: alertas de segurança
v4: integração com biblioteca e UpDowns
v5: versão mobile otimizada
```
