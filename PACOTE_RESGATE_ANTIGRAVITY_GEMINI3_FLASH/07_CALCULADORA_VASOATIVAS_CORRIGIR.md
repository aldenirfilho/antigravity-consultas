# 07 — Corrigir Calculadora de Drogas Vasoativas

## Objetivo

Corrigir erros de dose, concentração e prescrição comum nas calculadoras de vasoativas, mantendo segurança clínica.

## Arquivos prováveis

```txt
03_Calculadoras_UTI/index.html
03_Calculadoras_UTI/manifest.json
07_Estudos_Markdown/apps/vasoativas/index.html
07_Estudos_Markdown/data/vasoactive_drugs_brasil_presets.json
UPDOWN_HUB_REDESIGN_ANTIGRAVITY/.../vasoactive_drugs_brasil_presets.json
```

## Fórmula principal

Para drogas em mcg/kg/min:

```txt
mL/h = dose_mcg_kg_min × peso_kg × 60 / concentração_mcg_mL
```

Para drogas em mcg/min:

```txt
mL/h = dose_mcg_min × 60 / concentração_mcg_mL
```

Para vasopressina em U/min:

```txt
mL/h = dose_U_min × 60 / concentração_U_mL
```

## Presets comuns Brasil/UTI

> Conferir com farmácia/protocolo local antes de uso real.

| Droga | Diluição comum | Concentração | Unidade usual |
|---|---:|---:|---|
| Noradrenalina | 4 mg em 250 mL | 16 mcg/mL | mcg/kg/min |
| Noradrenalina concentrada | 8 mg em 250 mL | 32 mcg/mL | mcg/kg/min |
| Noradrenalina muito concentrada | 16 mg em 250 mL | 64 mcg/mL | mcg/kg/min |
| Adrenalina | 4 mg em 250 mL | 16 mcg/mL | mcg/kg/min |
| Dobutamina | 250 mg em 250 mL | 1000 mcg/mL | mcg/kg/min |
| Dopamina | 400 mg em 250 mL | 1600 mcg/mL | mcg/kg/min |
| Vasopressina | 20 U em 100 mL | 0,2 U/mL | U/min |
| Nitroglicerina | 50 mg em 250 mL | 200 mcg/mL | mcg/min |
| Nitroprussiato | 50 mg em 250 mL | 200 mcg/mL | mcg/kg/min ou mcg/min conforme protocolo |

## Validações de segurança

- peso obrigatório quando unidade for `mcg/kg/min`;
- dose não pode ser negativa;
- concentração não pode ser zero;
- alertar para dose fora de faixa usual;
- mostrar cálculo passo a passo;
- mostrar prescrição textual:
  - droga;
  - quantidade;
  - diluente;
  - volume final;
  - concentração;
  - dose-alvo;
  - velocidade em mL/h;
  - reavaliação/titulação.

## Testes rápidos

Paciente 70 kg:

### Noradrenalina 4 mg/250 mL, dose 0,1 mcg/kg/min
```txt
mL/h = 0,1 × 70 × 60 / 16 = 26,25 mL/h
```

### Vasopressina 20 U/100 mL, dose 0,03 U/min
```txt
mL/h = 0,03 × 60 / 0,2 = 9 mL/h
```

### Dobutamina 250 mg/250 mL, dose 5 mcg/kg/min
```txt
mL/h = 5 × 70 × 60 / 1000 = 21 mL/h
```

## Critérios de sucesso

- calculadora bate com os testes acima;
- presets aparecem em dropdown;
- prescrição fica clara;
- avisos clínicos aparecem;
- nenhuma dose é apresentada como prescrição definitiva sem validação institucional.
