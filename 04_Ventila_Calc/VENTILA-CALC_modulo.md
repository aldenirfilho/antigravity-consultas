# 🫁 VENTILA-CALC — Calculadora de Ventilação Mecânica & Gasometria
> **Módulo interativo para UTI** | Dr. Aldenir Rocha | v2026  
> Fonte original: `VENTILA-CALC.numbers` (Apple Numbers, Fortaleza/CE)  
> Convertido para integração com Enciclopédia Médica Intensiva

---

## 📋 INSTRUÇÕES PARA O ANTIGRAVITY

**O que fazer com este arquivo:**
1. Criar página: `01_Modulos_Clinicos/Ventilacao_Mecanica/ventila-calc.html`
2. Plugar link na homepage `index.html` na seção "Medicina Intensiva" como card novo
3. Plugar link no banco TEMI em `02_Banco_Questoes_TEMI/index.html` como módulo "VM/SDRA"
4. Usar o template visual existente (mesmo estilo do AVC Agudo)
5. Transformar cada seção abaixo em um **card colapsável** com emoji no título
6. As **calculadoras** devem ser inputs interativos com JavaScript inline — ver specs abaixo
7. Adicionar breadcrumb: `Início > Módulos > Ventilação Mecânica`

**Estilo:** mesmo padrão visual do AVC Agudo (fundo escuro, verde teal, tipografia serif nos títulos)  
**Gerado por:** Claude Inspector | **Aplicar em:** Antigravity | **Data:** 2026-05-06

---

## 🧭 MAPA DO MÓDULO (7 blocos)

| # | Bloco | Tipo |
|---|---|---|
| 1 | Peso Corporal Ideal (PCI) | 🧮 Calculadora |
| 2 | Volume Corrente Alvo (Vt) | 🧮 Calculadora |
| 3 | Mecânica Respiratória | 🧮 Calculadora |
| 4 | Índice ROX | 🧮 Calculadora |
| 5 | Gasometria Arterial — 6 Passos | 🧮 Calculadora |
| 6 | Tabela ARDSnet PEEP/FiO₂ | 📊 Tabela interativa |
| 7 | Classificação SARA / PaO₂/FiO₂ | 🎯 Decisão clínica |

---

## 🫁 BLOCO 1 — Peso Corporal Ideal (PCI)

> Base obrigatória para ventilação protetora. **NUNCA usar peso real em VM.**

### Fórmula de Devine (1974)

```
Homem:  PCI = 50 + 0,91 × (altura em cm − 152,4)
Mulher: PCI = 45,5 + 0,91 × (altura em cm − 152,4)
```

### 🧮 Calculadora PCI — spec para o Antigravity

```
INPUT:
  - Sexo: [M] [F]    (radio button)
  - Altura: ___ cm   (número inteiro, range 140-210)

OUTPUT (atualiza em tempo real):
  - PCI = ___ kg
  - Vt mínimo seguro (4 mL/kg PCI) = ___ mL    [⚠️ SARA grave / hipercapnia permissiva]
  - Vt-alvo padrão ARDSnet (6 mL/kg PCI) = ___ mL    [🎯 ALVO TERAPÊUTICO PRINCIPAL]
  - Vt máximo (8 mL/kg PCI) = ___ mL    [🔴 Limite superior — pulmão sem patologia]
```

**JavaScript para Antigravity:**
```javascript
function calcPCI(sexo, altura) {
  const base = sexo === 'M' ? 50 : 45.5;
  const pci = base + 0.91 * (altura - 152.4);
  return {
    pci: pci.toFixed(1),
    vt4: (pci * 4).toFixed(0),
    vt6: (pci * 6).toFixed(0),
    vt8: (pci * 8).toFixed(0)
  };
}
```

---

## 🌬️ BLOCO 2 — Parâmetros do Ventilador & Mecânica Respiratória

### Inputs necessários (beira-leito)

| Parâmetro | Símbolo | Unidade | Valor normal |
|---|---|---|---|
| Volume corrente entregue | Vt | mL | 6 mL/kg PCI |
| Pressão de pico | P-pico | cmH₂O | < 35 |
| Pressão de platô | P-plat | cmH₂O | ≤ 30 |
| PEEP total (pausa expiratória) | PEEP-tot | cmH₂O | — |
| PEEP set | PEEP-set | cmH₂O | — |
| Frequência respiratória | FR | ipm | 12–20 |
| FiO₂ | FiO₂ | fração (0.21–1.00) | — |
| Fluxo inspiratório | Q-insp | L/min | 40–60 |

### 🧮 Calculadora de Mecânica — spec

```
CÁLCULOS AUTOMÁTICOS:

Complacência estática (Cst):
  Cst = Vt / (P-plat − PEEP-tot)
  Normal: > 60 mL/cmH₂O | SARA grave: < 25

Resistência das vias aéreas (Raw):
  Raw = (P-pico − P-plat) / Fluxo (L/s)
  Normal: < 10 cmH₂O/L/s | Elevado: > 20 (broncoespasmo/secreção)

Auto-PEEP (PEEP intrínseco):
  auto-PEEP = PEEP-tot − PEEP-set
  Leve: < 3 | Moderada: 3-5 | Significativa + TE: > 5

Driving Pressure (ΔP):
  ΔP = P-plat − PEEP-tot
  Alvo: ≤ 15 cmH₂O | > 15 = REDUZIR Vt

Mechanical Power (MP):
  MP = 0,098 × FR × Vt × (P-pico + P-plat) / 2
  (simplificado beira-leito)
  Limiar: > 17 J/min = VILI risk aumentado
```

### 🚨 Alertas automáticos (lógica para JS)

```javascript
// Driving Pressure
if (drivingPressure > 15) alerta("🔴 REDUZIR Vt! ΔP elevado — risco VILI");
if (drivingPressure <= 15 && cst < 25) alerta("🟠 SARA GRAVE — considerar prona 16h + BNM 48h");

// Complacência
if (cst >= 60) status("✅ Excelente (> 60)");
else if (cst >= 40) status("🟡 Aceitável (40–60)");
else if (cst >= 25) status("🟠 SARA leve-moderada");
else status("🔴 SARA GRAVE (< 25) — PEEP alta + Vt 4-6 mL/kg PCI + considerar ECMO");

// Resistência
if (raw > 20) alerta("🔴 Broncoespasmo / secreção / obstrução grave");
else if (raw > 10) alerta("🟡 Resistência elevada — investigar");

// P-plat
if (pPlat > 30) alerta("🔴 P-plat > 30: REDUZIR Vt IMEDIATAMENTE");
if (pPico > 35) alerta("🟠 P-pico elevado — checar curva de fluxo e Raw");
```

---

## 🩺 BLOCO 3 — Índice ROX

> Preditor de falha de VNI/oxigenoterapia de alto fluxo em SARA.

### Fórmula

```
ROX = (SpO₂ / FiO₂) / FR

Interpretação:
  ROX > 4,88 após 12h OAF → Sucesso provável (evita IOT)
  ROX 3,85–4,88           → Zona cinzenta — reavaliar
  ROX < 3,85              → Risco de falha → preparar IOT
  ROX < 3,85 com piora    → IOT (Glasgow ≤ 8 = IOT imediata!)
```

### 🧮 Calculadora ROX — spec

```
INPUTS:
  - SpO₂: ___ %
  - FiO₂: ___ % (ex: 50%)  [converter internamente para fração ÷100]
  - FR: ___ ipm

OUTPUT:
  - ROX = ___
  - Interpretação: [Sucesso provável | Zona cinzenta | Risco falha | IOT!]
  - Recomendação clínica automática
```

---

## 🩸 BLOCO 4 — Gasometria Arterial: Análise em 6 Passos

> **Metodologia sistemática. Nunca pule etapas.**

### Inputs

| Campo | Unidade | Referência normal |
|---|---|---|
| pH | — | 7,35–7,45 |
| PaCO₂ | mmHg | 35–45 |
| HCO₃⁻ | mEq/L | 22–26 |
| BE | mEq/L | −2 a +2 |
| PaO₂ | mmHg | 80–100 |
| Lactato | mmol/L | < 2 |
| Na⁺ | mEq/L | — |
| Cl⁻ | mEq/L | — |
| Albumina | g/dL | — |

### Os 6 Passos — lógica completa

#### Passo 1 — pH: Acidemia ou Alcalemia?

```
pH < 7,35 → ACIDEMIA
pH 7,35–7,45 → NORMAL
pH > 7,45 → ALCALEMIA
pH < 7,20 → ACIDEMIA GRAVE (proteger via aérea!)
```

#### Passo 2 — Componente Primário (heurística)

```
ACIDEMIA:
  PaCO₂ > 45 E HCO₃ normal/alto → Acidose Respiratória primária
  HCO₃ < 22 E PaCO₂ normal/baixo → Acidose Metabólica primária
  Ambos alterados → Distúrbio misto

ALCALEMIA:
  PaCO₂ < 35 E HCO₃ normal/baixo → Alcalose Respiratória primária
  HCO₃ > 26 E PaCO₂ normal/alto → Alcalose Metabólica primária
```

#### Passo 3 — Compensação Esperada

```
Acidose Metabólica:
  PaCO₂ esperado = 1,5 × HCO₃ + 8 ± 2   [Fórmula de Winter]
  PaCO₂ medido > esperado → Acidose Resp ASSOCIADA
  PaCO₂ medido < esperado → Alcalose Resp ASSOCIADA

Alcalose Metabólica:
  PaCO₂ esperado = 0,7 × HCO₃ + 21 ± 2

Acidose Respiratória AGUDA:
  HCO₃ aumenta 1 mEq a cada 10 mmHg de ↑ PaCO₂

Acidose Respiratória CRÔNICA:
  HCO₃ aumenta 3,5 mEq a cada 10 mmHg de ↑ PaCO₂

Alcalose Respiratória AGUDA:
  HCO₃ cai 2 mEq a cada 10 mmHg de ↓ PaCO₂

Alcalose Respiratória CRÔNICA:
  HCO₃ cai 5 mEq a cada 10 mmHg de ↓ PaCO₂

⚠️ Compensação adequada = ABS(diferença) ≤ 2
   Fora do esperado = Distúrbio misto / adicional
```

#### Passo 4 — Anion Gap (AG)

```
AG = Na⁺ − (Cl⁻ + HCO₃⁻)   [normal: 8–12 mEq/L]

AG corrigido (se albumina < 4 g/dL):
  AG-corrigido = AG + 2,5 × (4 − albumina)

AG < 8 → Baixo: hipoalbuminemia, intoxicação por lítio, mieloma
AG 8–12 → Normal
AG 12–20 → Moderadamente elevado → investigar MUDPILES-A
AG > 20 → ELEVADO: investigar MUDPILES-A

MUDPILES-A:
  M — Metanol / Metformina
  U — Uremia
  D — Cetoacidose Diabética (DKA)
  P — Paraldeído / Propilenoglicol
  I — Isoniazida / Intoxicações
  L — Lactato (sepse, isquemia, mitocondrial, infecção)
  E — Etilenoglicol
  S — Salicilatos
  A — Álcool / outros
```

#### Passo 5 — Delta-Delta (se AG elevado)

```
Δ/Δ = (AG medido − 12) / (24 − HCO₃ medido)

< 1    → Acidose Metabólica MISTA (AG elevado + hiperclorêmica)
1–2   → Acidose Metabólica de AG pura
> 2   → Alcalose Metabólica concomitante (HCO₃ pré-existente elevado)
```

#### Passo 6 — Lactato & Perfusão

```
Lactato < 2 mmol/L  → Normal
Lactato 2–4 mmol/L  → Hiperlactatemia moderada (sepse, metformina, isquemia)
Lactato > 4 mmol/L  → Hiperlactatemia grave → DDRP (Distúrbio Distribuição/Perfusão)
                       investigar: sepse grave, choque, isquemia mesentérica

⚠️ Normalização do lactato em 6h = meta terapêutica Surviving Sepsis
```

---

## 📊 BLOCO 5 — Tabela ARDSnet PEEP/FiO₂

> Fonte: ALVEOLI Trial 2004 | ART Trial 2017

### Estratégia LOW PEEP (pulmão pouco recrutável)

| FiO₂ | 0,30 | 0,40 | 0,40 | 0,50 | 0,50 | 0,60 | 0,70 | 0,70 | 0,70 | 0,80 | 0,90 | 0,90 | 0,90 | 1,00 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **PEEP** | 5 | 5 | 8 | 8 | 10 | 10 | 10 | 12 | 14 | 14 | 14 | 16 | 18 | 18–24 |

### Estratégia HIGH PEEP (SARA grave/recrutável — LOVES)

| FiO₂ | 0,30 | 0,30 | 0,30 | 0,30 | 0,30 | 0,40 | 0,40 | 0,50 | 0,50 | 0,50–0,80 | 0,80 | 0,90 | 1,00 | 1,00 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **PEEP** | 5 | 8 | 10 | 12 | 14 | 14 | 16 | 16 | 18 | 20 | 22 | 22 | 22 | 24 |

### 🎯 Escolha da estratégia

```
LOW PEEP:   SARA leve-moderada / pulmão pouco recrutável
HIGH PEEP:  SARA grave / recrutável — use individualizada:
            titulada por P-plat, complacência mínima,
            P-transpulmonar (EIT, ECO-ART)

⚠️ ART Trial 2017: manobras agressivas de recrutamento (> 35 cmH₂O)
   aumentaram mortalidade — NÃO realizar rotineiramente
```

### 🧮 Ajustador PEEP/FiO₂ — spec para Antigravity

```
INPUT:
  - FiO₂ atual: ___ (decimal, ex: 0.50)
  - Estratégia: [LOW] [HIGH]  (radio)

OUTPUT:
  - PEEP sugerida: ___ cmH₂O
  - Faixa recomendada: ___
  - Alerta se HIGH PEEP + sem titulação individualizada
```

---

## 🎯 BLOCO 6 — Classificação SARA (Berlim 2012) & Conduta

| Índice P/F | Classificação | Conduta |
|---|---|---|
| ≥ 300 | ✅ Sem SARA | VM padrão, desescalonar FiO₂ |
| 200–300 | 🟡 SARA Leve | Otimizar P/PEEP/sedação titulada |
| 100–200 | 🟠 SARA Moderada | Q4 titulada, HIGH PEEP, sedação profunda |
| < 100 | 🔴 SARA Grave | PRONA 16h + BNM 48h + PEEP alta + Vt 4–6 mL/kg PCI + considerar ECMO |

### 🧮 Calculadora P/F — spec

```
INPUT:
  - PaO₂: ___ mmHg
  - FiO₂: ___ % (ex: 60%)

OUTPUT:
  - P/F = ___
  - Classificação SARA
  - Conduta recomendada (texto automático da tabela acima)
  - Alerta: "INDICADA (<150): Pronação 16h + BNM 48h" se P/F < 150
```

---

## 🧠 MNEMÔNICOS DO MÓDULO

### DOPE — causas de dessat. súbita no VM
```
D — Deslocamento do tubo (IOT seletiva ou extubação)
O — Obstrução (rolha de muco, dobra no tubo)
P — Pneumotórax
E — Equipamento (desconexão, falha do ventilador)
```

### MUDPILES-A — acidose metabólica com AG elevado
```
M — Metanol / Metformina
U — Uremia
D — DKA (cetoacidose diabética)
P — Paraldeído / Propilenoglicol
I — Isoniazida / Intoxicações
L — Lactato
E — Etilenoglicol
S — Salicilatos
A — Álcool
```

---

## ⚡ FLASHCARDS TEMI — 10 perguntas relâmpago

| # | Pergunta | Resposta |
|---|---|---|
| 1 | Fórmula PCI homem (Devine) | 50 + 0,91 × (cm − 152,4) |
| 2 | Vt-alvo ARDSnet | 6 mL/kg PCI |
| 3 | P-plat máxima no SARA | ≤ 30 cmH₂O |
| 4 | Driving Pressure alvo | ≤ 15 cmH₂O |
| 5 | ROX < ? = risco IOT | < 3,85 |
| 6 | Fórmula Winter | 1,5 × HCO₃ + 8 ± 2 |
| 7 | AG normal | 8–12 mEq/L |
| 8 | Lactato sepse grave | > 4 mmol/L |
| 9 | P/F SARA grave | < 100 |
| 10 | MP risco VILI | > 17 J/min |

---

## 🚨 PEGADINHAS TEMI

1. **"Usar peso real no Vt"** → ❌ SEMPRE PCI (Devine)
2. **"ROX normal = extubação segura"** → ❌ ROX é para predizer FALHA de OAF/VNI, não extubação
3. **"Compensação renal da acidose resp é imediata"** → ❌ Demora 3–5 dias (resposta crônica)
4. **"P-pico = P-plat"** → ❌ P-pico inclui resistência; P-plat reflete complacência (medir em pausa)
5. **"Prona em qualquer SARA"** → ❌ Indicação: P/F < 150 por ≥ 12h com FiO₂ ≥ 0,60 e PEEP ≥ 5

---

## 📚 REFERÊNCIAS

- ARDSNet. NEJM 2000 (ARMA Trial — Vt 6 vs 12 mL/kg)
- Guerin C et al. NEJM 2013 (PROSEVA — prona)
- Briel M et al. JAMA 2010 (ALVEOLI/LOVS/Express — HIGH vs LOW PEEP)
- Cavalcanti AB et al. JAMA 2017 (ART Trial — manobras de recrutamento)
- Roca O et al. 2016 (Índice ROX)
- Devine BJ. Drug Intelligence 1974 (fórmula PCI)
- Surviving Sepsis Campaign 2021 (metas lactato)
- Berlim Definition SARA — JAMA 2012

---

## 🔗 CONEXÕES COM OUTROS MÓDULOS

- → [Sepse & Choque Séptico] — VM em sepse, hipercapnia permissiva
- → [AVC Agudo] — neuroproteção ventilatória, hiperventilação no herniamento
- → [IRA/TRS] — ajuste de ventilação em paciente em diálise
- → [SAD — Sedação/Analgesia/Delirium] — acoplamento VM + sedação

---

*🤖 Gerado por Claude Inspector a partir de VENTILA-CALC.numbers | Aplicar via Antigravity | v2026-05-06*  
*⚕️ Conteúdo educacional para médicos — não substitui julgamento clínico e protocolos locais*
