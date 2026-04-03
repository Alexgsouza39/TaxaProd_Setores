# 📋 Melhorias Implementadas - App Taxas de Produção

## ✨ Novas Funcionalidades

### 1️⃣ **Interface com Abas (TabWidget)**
- **Aba "Tinturaria"**: Mantém toda a funcionalidade original
- **Aba "Acabamento"**: Nova seção para cálculos de acabamento/finishing

### 2️⃣ **Módulo de Acabamento Completo**
A nova aba inclui campos para:

#### **Dados Básicos:**
- ✅ Código do acabamento
- ✅ Código da cor
- ✅ Descrição

#### **Parâmetros de Cálculo:**
- ✅ **g/m² (Seco)** - Peso seco do tecido (PS)
- ✅ **g/m² (Úmido)** - Peso úmido após banho (PU)
- ✅ **Largura (m)** - Largura do tecido em metros
- ✅ **Velocidade (m/h)** - Velocidade de processamento em m/h

#### **Produtos Químicos:**
- ✅ Código Químico 1
- ✅ Código Químico 2
- ✅ Código Químico 3

### 3️⃣ **Cálculos Automáticos de Acabamento**

#### **Pick-up (Arraste de Banho) em %**
```
Pick-up (%) = (PU - PS) / PS × 100
```
Onde:
- PU = Peso úmido (g/m²)
- PS = Peso seco (g/m²)

#### **Taxa de Produção em m/h**
```
Taxa Produção (m/h) = Largura (m) × Velocidade (m/h)
```

#### **Arraste Total de Químico (%)**
- Soma do Pick-up, mostrando o percentual total de arraste

### 4️⃣ **Exportação em Excel com Múltiplas Abas**
- 📊 Novo formato: **`.xlsx` (Excel)**
- 📑 Cada tipo de relatório em uma sheet separada:
  - **Sheet 1: "Tinturaria"** - Dados das máquinas de tintura
  - **Sheet 2: "Acabamento"** - Dados de acabamento/finishing
- ✅ Também suporta **CSV** (compatível com Excel PT-BR)

### 5️⃣ **Tabela de Visualização Melhorada**
- Colunas específicas para cada módulo
- Formatação com linhas alternadas
- Precisão de 2 casas decimais para valores numéricos

---

## 🎯 Como Usar

### **Calcular Tinturaria:**
1. Clique na aba **"Tinturaria"**
2. Preencha os dados do produto (Artigo, Cor, Descrição, Gramatura)
3. Informe Comprimento da peça, Nº de Rolos e Nº de Cordas
4. Insira os tempos (HH:MM ou formato decimal) para cada máquina
5. Clique em **"Calcular Tinturaria"**
6. A tabela será preenchida com os resultados

### **Calcular Acabamento:**
1. Clique na aba **"Acabamento"**
2. Preencha:
   - Código, Código Cor, Descrição
   - g/m² Seco (PS) e g/m² Úmido (PU)
   - Largura em metros
   - Velocidade em m/h
   - Códigos dos 3 químicos (opcional)
3. Clique em **"Calcular Acabamento"**
4. Os valores de Pick-up e Taxa de Produção são calculados automaticamente

### **Exportar Relatório:**
1. Complete os cálculos desejados (Tinturaria e/ou Acabamento)
2. Clique em **"Exportar CSV"** (botão disponível na aba Tinturaria)
3. Escolha o local e formato:
   - **`.xlsx`** → Excel com múltiplas abas (recomendado)
   - **`.csv`** → CSV com separador `;` (compatível Excel PT-BR)
4. O arquivo será salvo no local escolhido

---

## 📊 Estrutura de Exportação

### **Arquivo `.xlsx` (Excel)**
```
Relatório_TX_Produção_20250327_143025.xlsx
├── Sheet "Tinturaria"
│   ├── Maquina | Cordas | Metragem | Peso | Gramatura | Tempo | Taxa Prod | Unidade
│   └── [Dados das máquinas de tintura]
│
└── Sheet "Acabamento"
    ├── Código | Cor | Descrição | g/m² Seco | g/m² Úmido | Pick-up %
    │   Largura | Velocidade | Taxa Prod (m/h) | Arraste Total % | Quim1 | Quim2 | Quim3
    └── [Dados de acabamento]
```

---

## 🔧 Fórmulas Implementadas

| Módulo | Cálculo | Fórmula |
|--------|---------|---------|
| **Tinturaria** | Taxa de Produção | Metragem / Tempo |
| **Acabamento** | Pick-up/Arraste | (PU - PS) / PS × 100 |
| **Acabamento** | Taxa de Produção | Largura × Velocidade |

---

## ⚙️ Requisitos Técnicos

✅ Python 3.7+
✅ tkinter (incluído com Python)
✅ pandas 2.0+
✅ openpyxl 3.0+ (para Excel)
✅ Decimal (biblioteca padrão - para precisão numérica)

---

## 🎨 Visual & UX

✨ Interface com tema "clam"
✨ Fontes modernas (Segoe UI)
✨ Cores alternadas nas tabelas (#bdd59d e #bec0cc)
✨ Barras de scroll para dados grandes
✨ Layout responsivo com abas

---

## 💡 Dicas Importantes

⚠️ **Precisão Numérica:**
- Use Decimal internamente para cálculos (maior precisão)
- Valores exibidos com 2 casas decimais

⚠️ **Validações:**
- Todos os campos numéricos são validados
- Valores negativos ou zero são rejeitados onde apropriado
- Mensagens de erro claras para o usuário

⚠️ **Segurança:**
- Não permite salvar em diretórios do Windows (/Windows, /Program Files)
- Caminho de arquivo criado automaticamente se não existir

---

## 📝 Changelog

**Versão 2.0 (Nova)**
- ✅ Interface com abas (Tinturaria + Acabamento)
- ✅ Novo módulo de Acabamento/Finishing
- ✅ Cálculo de Pick-up (arraste de banho)
- ✅ Exportação em Excel com múltiplas sheets
- ✅ Campos para códigos químicos

**Versão 1.0 (Original)**
- Cálculos de Tinturaria
- Exportação em CSV

---

## 🚀 Próximas Melhorias Possíveis

- 🔮 Histórico de cálculos salvos
- 🔮 Integração com banco de dados
- 🔮 Gráficos de comparação de taxas
- 🔮 Templates de relatório personalizados
- 🔮 Configurações do usuário (idioma, temas, etc.)

---

**Desenvolvido com ❤️ para otimização de produção**
