# 🚀 Guia Rápido - Taxa de Produção v2.0

## 📌 Tela 1: TINTURARIA

### Campos a Preencher:
| Campo | Formato | Exemplo |
|-------|---------|---------|
| Artigo | Texto | ART-001 |
| Cor | Texto | Azul |
| Descrição | Texto | Algodão 100% |
| Gramatura (g/m) | Decimal | 150.5 |
| Peça (m) | Decimal | 1000 |
| Nº Rolos | Inteiro | 5 |
| Nº Cordas | Inteiro | 2 |
| Tempos (M01-M11) | HH:MM ou Decimal | 2:30 ou 2.5 |

### Máquinas Disponíveis:
- M01: TEX24 (1 corda)
- M02: TEX25 (2 cordas)
- M03: TEX26 (2 cordas)
- M04: TEX25 (4 cordas)
- M05: TEX28 (4 cordas)
- M06: TEX21 (4 cordas)
- M07: TEX20 (4 cordas)
- M08: TEX19 (6 cordas)
- M09: TEX04 (6 cordas)
- M10: TEX05-350kg (2 cordas, peso fixo)
- M11: TEX06-600kg (4 cordas, peso fixo)

### Resultados Calculados:
✓ Metragem total processada
✓ Peso do lote
✓ Tempo em formato HH:MM:SS
✓ **Taxa de produção em m/h**

### Passos:
1. Preencha dados do produto
2. Insira tempos para as máquinas usadas (zeros ignorados)
3. Clique: **"Calcular Tinturaria"**
4. Veja resultados na tabela

---

## 📌 Tela 2: ACABAMENTO

### Campos a Preencher:
| Campo | Formato | Exemplo |
|-------|---------|---------|
| Código | Texto | AC-001 |
| Código Cor | Texto | 01 |
| Descrição | Texto | Soft Touch |
| g/m² (Seco) | Decimal | 150 |
| g/m² (Úmido) | Decimal | 180 |
| Largura (m) | Decimal | 1.5 |
| Velocidade (m/h) | Decimal | 100 |
| Código Químico 1 | Texto (opt) | QUIM001 |
| Código Químico 2 | Texto (opt) | QUIM002 |
| Código Químico 3 | Texto (opt) | QUIM003 |

### Resultados Automaticamente Calculados:
✓ **Pick-up %** = (g/m² Úmido - g/m² Seco) / g/m² Seco × 100

✓ **Taxa de Produção (m/h)** = Largura × Velocidade

✓ **Arraste Total %** = Pick-up

### Passos:
1. Preencha dados do acabamento
2. Informe pesos seco e úmido (antes e depois do banho)
3. Clique: **"Calcular Acabamento"**
4. Veja dados e fórmulas na tabela

---

## 💾 EXPORTAÇÃO

### Opção 1: Excel (.xlsx) ⭐ RECOMENDADO
```
Relatório_TX_Produção_20250327_143025.xlsx
├── Tinturaria (se calculado)
└── Acabamento (se calculado)
```
→ **Cada tema em uma aba separada**

### Opção 2: CSV (.csv)
```
Relatório_TX_Produção_20250327_143025.csv
→ Separador: ; (ponto-e-vírgula)
→ Codificação: UTF-8 (compatível Excel PT-BR)
```

### Como Fazer:
1. Calcule Tinturaria e/ou Acabamento
2. Clique: **"Exportar CSV"**
3. Escolha pasta e formato
4. ✓ Arquivo salvo!

---

## 🔢 FÓRMULAS USADAS

### Tinturaria:
```
Metragem = Comp × Rolos × Cordas × Nº Corpos
Peso = Metragem × Gramatura / 1000
Taxa Prod. (m/h) = Metragem / Tempo (horas)
Unidade: m/h
```

### Acabamento:
```
Pick-up (%) = (PU - PS) / PS × 100
Taxa Prod. (m/h) = Largura × Velocidade
Arraste % = Pick-up %
```

Onde:
- PS = g/m² Seco
- PU = g/m² Úmido

---

## ⚠️ VALIDAÇÕES

- ❌ Gramatura ≤ 0 → Erro
- ❌ Comprimento ≤ 0 → Erro
- ❌ g/m² ≤ 0 → Erro
- ❌ Largura ≤ 0 → Erro
- ❌ Velocidade ≤ 0 → Erro
- ❌ Campos não preenchidos → Erro

✓ Campos com 0 são ignorados em Tinturaria
✓ Valores com 2 ou 3 casas decimais

---

## 🎯 EXEMPLO PRÁTICO

### Cenário: Acabamento Soft Touch

**Entrada:**
```
Código: 001
Descrição: Soft Touch
g/m² Seco: 150
g/m² Úmido: 165
Largura: 1.5 m
Velocidade: 120 m/h
```

**Cálculos Automáticos:**
```
Pick-up = (165 - 150) / 150 × 100 = 10%
Taxa Prod = 1.5 × 120 = 180 m/h
Arraste = 10%
```

**Resultado:** Tecido recebe 10% de araste de banho a taxa de 180 m/h

---

## 📞 DÚVIDAS?

- Gramatura: peso do tecido por metro quadrado (g/m²)
- Pick-up: quanto de produto químico o tecido absorveu (%)
- Taxa de Produção: quantos metros por hora (m/h)
- Arraste: percentual total de absorção de banho

---

**Última Atualização: 27/03/2025**
**Versão: 2.0**
