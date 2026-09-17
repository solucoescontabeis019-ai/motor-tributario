# 📸 GUIA VISUAL — Como Usar Upload de PDFs

## 🎯 O que você consegue fazer agora:

Você pode **arrastar seus PDFs direto no sistema** e ele vai extrair os dados automaticamente!

---

## 📋 Passo a Passo:

### **PASSO 1: Abrir o sistema**

- Acesse: `https://seu-app.onrender.com` (sua URL no Render)
- Você verá a tela do dashboard

### **PASSO 2: Ir para aba "Upload" 📤**

```
┌─────────────────────────────────┐
│ 📤 Upload  ✏️ Dados   📊 Resultado│
│ ↑ CLIQUE AQUI                   │
└─────────────────────────────────┘
```

### **PASSO 3: Arrastar PDFs**

Você verá uma caixa assim:

```
┌─────────────────────────────────────────┐
│                                         │
│             📁                          │
│      Arraste seus PDFs aqui             │
│                                         │
│   ou clique para abrir seletor          │
│                                         │
│      [Selecionar Arquivos]              │
│                                         │
└─────────────────────────────────────────┘
```

**Opções:**
- ✅ Arrastar PDFs direto na caixa
- ✅ Clicar no botão para selecionar

### **PASSO 4: Arquivos sendo enviados**

Você verá uma mensagem assim:

```
📤 Upload em andamento... 95%
```

Aguarde até ficar 100%.

### **PASSO 5: Processamento automático**

Depois aparece:

```
🔄 Processando PDFs... Extraindo dados...
```

O sistema está lendo os PDFs e extraindo as informações.

### **PASSO 6: Ver dados extraídos**

Pronto! Aparecerá um preview:

```
┌─────────────────────────────────────┐
│ Simples Nacional WAS.pdf            │
│                                     │
│ Tipo: PGDAS                         │
│ CNPJ: 04.286.335/0001-79            │
│ Razão Social: WASHINGTON L LOPES    │
│ RBT12: R$ 2.236.444,92              │
│ DAS: R$ 18.607,42                   │
│ Período: 08/2026                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Entradas.pdf                        │
│                                     │
│ Tipo: ENTRADA                       │
│ Período: 01/01/2026 a 31/08/2026    │
│ Empresa CNPJ: 04.286.335/0001-79    │
│ Total: R$ 404.301,55                │
│ Itens: 46                           │
│                                     │
│ Ver itens (expandir tabela)         │
└─────────────────────────────────────┘
```

### **PASSO 7: Usar dados extraídos**

Clique no botão:

```
┌─────────────────────────┐
│ ✅ Usar Dados Extraídos │
│ 📤 Novo Upload          │
└─────────────────────────┘
```

O sistema vai:
1. ✅ Preencher automaticamente os dados da empresa
2. ✅ Adicionar fornecedores
3. ✅ Adicionar clientes
4. ✅ Ir para aba "Dados Manuais"

### **PASSO 8: Revisar dados (opcional)**

Você vai estar na aba "Dados Manuais" com tudo preenchido:

```
Empresa:
  CNPJ: 04.286.335/0001-79
  Razão Social: WASHINGTON L LOPES COSMOPOLIS
  RBT12: 2236444.92
  DAS: 18607.42

Fornecedores: 46 adicionados
Clientes: X adicionados
```

**Você pode:**
- ✅ Revisar os dados
- ✅ Mudar valores se precisar
- ✅ Adicionar/remover fornecedores ou clientes
- ✅ Deixar como está

### **PASSO 9: Calcular cenários**

Clique em:

```
┌──────────────────────────────┐
│ 🚀 Calcular Cenários         │
└──────────────────────────────┘
```

### **PASSO 10: Ver resultado**

A aba "Resultado" vai mostrar:

```
┌──────────────────────────┐
│ 2026 Real                │
│ R$ 18.607,42             │
└──────────────────────────┘

┌──────────────────────────┐
│ 2027 Simples Puro        │
│ R$ 18.607,42             │
└──────────────────────────┘

┌──────────────────────────┐
│ 2027 Híbrido             │
│ R$ 178.159,89            │
└──────────────────────────┘

🟢 MANTER SIMPLES NACIONAL
Economia anual: R$ 159.552,47
```

---

## 📊 Arquivos que você pode enviar:

### ✅ Recomendados (o sistema lê perfeitamente):

1. **Simples Nacional WAS.pdf** (PGDAS-D)
   - Extrai: CNPJ, Razão Social, RBT12, DAS, Período

2. **Entradas.pdf** (Acompanhamento de compras)
   - Extrai: Lista de fornecedores, valores

3. **Saídas.pdf** (Acompanhamento de vendas)
   - Extrai: Lista de clientes, valores

4. **Serviços.pdf** (Receita de serviços)
   - Extrai: Lista de clientes, valores

5. **RELAÇÃO DE FORNECEDORES.pdf**
   - Extrai: CNPJs, nomes, valores totais

6. **RELAÇÃO DE CLIENTES.pdf**
   - Extrai: CNPJs, nomes, valores totais

### ⚠️ Pode ter problemas:

- ❌ PDFs que são imagens/scaneados (sem texto)
- ❌ PDFs protegidos com senha
- ❌ PDFs com layout muito diferente

Se tiver problema, me comunica o erro!

---

## 🔴 Erros comuns:

### **Erro: "Nenhum arquivo PDF"**
- ✅ Certifique-se que são PDFs reais (não imagens)

### **Erro: "Upload falhou"**
- ✅ Tente novamente
- ✅ Verifique conexão de internet

### **Erro: "Dados não aparecem"**
- ✅ O PDF pode ser uma imagem scaneada
- ✅ Tente outro PDF

### **Dados incompletos**
- ✅ Normal: o parser pode não achar tudo
- ✅ Você pode revisar e corrigir na aba "Dados Manuais"

---

## 💡 Dicas:

1. **Enviar todos os PDFs de uma vez**
   - Você pode arrastar 6 PDFs ao mesmo tempo
   - Sistema processa todos automaticamente

2. **Revisar os dados extraídos**
   - Antes de calcular, olhe o preview
   - Se algo errado, ajuste na aba "Dados Manuais"

3. **Testar com dados de teste**
   - Use os PDFs que você já tem (WASHINGTON L LOPES)
   - Depois pode usar dados reais de seus clientes

4. **Se der erro em um PDF**
   - Sistema mostra qual falhou
   - Você pode:
     - Preencher manualmente aquele PDF
     - Tentar novo upload sem aquele

---

## 🎯 Fluxo resumido:

```
Arrastar PDFs
    ↓
Upload automático
    ↓
Processamento automático
    ↓
Preview dos dados
    ↓
"Usar Dados Extraídos"
    ↓
Formulário preenchido
    ↓
"Calcular Cenários"
    ↓
Resultado com 3 cenários tributários
```

---

## ✅ Pronto para usar!

Agora você consegue:
- ✅ Arrastar PDFs direto no sistema
- ✅ Extrair dados automaticamente
- ✅ Ver preview dos dados
- ✅ Calcular os 3 cenários tributários
- ✅ Tomar decisão de regime tributário

---

**Versão:** 0.5.0  
**Data:** 2026-09-17  
**Status:** ✅ Ativo e funcionando
