# ⚡ QUICK START — Dashboard em 5 Minutos

## 🚀 Comece AGORA (sem complicações)

### Com Docker (Recomendado — Mais Fácil)

```bash
# 1. Copie todos os arquivos para uma pasta
mkdir motor-web && cd motor-web
# (Copie: main.py, requirements.txt, index.html, docker-compose.yml, 
#  Dockerfile, nginx.conf)

# 2. Rode tudo
docker-compose up

# 3. Abra no navegador
# Frontend: http://localhost:3000
# API: http://localhost:8000/docs
```

**É isso!** Em 2 minutos tudo está rodando.

---

### Sem Docker (Python Puro)

```bash
# 1. Crie ambiente
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instale dependências
pip install fastapi uvicorn pydantic pydantic-settings python-multipart python-dotenv python-jose passlib

# 3. Rode o backend
python -m uvicorn main:app --reload --port 8000

# 4. Em outro terminal, abra o frontend
# Opção A: Abra index.html direto no navegador
open index.html

# Opção B: Use um servidor web
python -m http.server 8080
# Acessa: http://localhost:8080
```

---

## 📊 Usando o Dashboard

### 1️⃣ Preencha os Dados
- Vá à aba **"Dados Manuais"**
- Dados já estão pré-preenchidos (WASHINGTON L LOPES)
- Clique em **"Calcular Cenários"**

### 2️⃣ Veja o Resultado
- Automaticamente mostra os **3 cenários**
- **Recomendação destacada** (verde para Simples, aviso para Híbrido)
- **Tabelas** com fornecedores e clientes
- **Economia anual** em destaque

### 3️⃣ Baixe o Resultado
- Clique **"Baixar JSON"** para salvar os dados
- Use para compartilhar com contador/gestor

---

## 🎯 O Que o Dashboard Calcula?

| Cenário | O Quê? |
|---------|--------|
| 📊 **2026 Real** | O que você pagou/paga agora em 2026 |
| 🟢 **2027 Simples Puro** | Se ficar no Simples em 2027 |
| 🔴 **2027 Híbrido** | Se optar por IBS/CBS no regime regular |

**Compara os 3 e recomenda qual é melhor!**

---

## 🔗 URLs de Acesso

| URL | O Quê? |
|-----|--------|
| `http://localhost:3000` | **Dashboard** (interface do usuário) |
| `http://localhost:8000/docs` | **Swagger** (testa API) |
| `http://localhost:8000/health` | Verifica se API está ok |

---

## 📝 Exemplo: Teste Rápido

1. Abra http://localhost:3000
2. Aba "Dados Manuais" já tem dados pré-carregados
3. Clique em "🚀 Calcular Cenários"
4. Em 2 segundos, resultado aparece na aba "Resultado"
5. Veja:
   - Cards com R$ dos 3 cenários
   - Recomendação (🟢 SIMPLES NACIONAL)
   - Economia anual
   - Observações importantes
   - Tabelas de fornecedores e clientes

---

## 🛠️ Customizar Dados

### Para Testar com Sua Empresa

Na aba **"Dados Manuais"**:

1. **Empresa**
   - CNPJ: seu CNPJ
   - Razão Social: seu nome
   - RBT12: receita bruta últimos 12 meses
   - DAS: quanto você pagou em 2026

2. **Fornecedores**
   - Clique "Adicionar Fornecedor"
   - Preencha CNPJ, nome, total comprado

3. **Clientes**
   - Clique "Adicionar Cliente"
   - Preencha CNPJ, nome, quanto você faturou

4. Clique **"Calcular"** e pronto!

---

## 📚 Arquivos Entregues

```
✅ main.py                  → Backend (FastAPI)
✅ index.html               → Frontend (interface)
✅ requirements.txt         → Dependências Python
✅ docker-compose.yml       → Orquestração Docker
✅ Dockerfile               → Build da imagem
✅ nginx.conf               → Servidor web
✅ .env.example             → Variáveis de ambiente
✅ README_DASHBOARD.md      → Documentação completa
✅ QUICK_START.md           → Este arquivo
✅ PLANO_DASHBOARD_WEB.md   → Roadmap completo
```

---

## 🔄 Estrutura das Requisições

```
Você preenche dados no formulário
         ↓
Clica "Calcular"
         ↓
JavaScript envia POST para /api/calcular
         ↓
FastAPI recebe e calcula
         ↓
Retorna JSON com resultados
         ↓
Dashboard mostra cenários
```

---

## 💡 Dicas

### 1. Não Funciona?
```bash
# Verifique se backend está rodando
curl http://localhost:8000/health
# Deve retornar: {"status": "healthy"}
```

### 2. Quer Ver os Logs?
```bash
docker-compose logs backend
```

### 3. Quer Parar Tudo?
```bash
docker-compose down
```

### 4. Quer Limpar Dados?
```bash
docker-compose down -v
```

---

## 🎓 Próxima Etapa

Quando quiser funcionalidades avançadas:

- ✅ Upload automático de PDFs
- ✅ Gráficos interativos
- ✅ Análise de sensibilidade (CBS, faturamento, compras)
- ✅ Relatório PDF profissional
- ✅ Histórico de simulações

**Tudo está planejado para Fase 2-3!**

---

## ✨ Está Pronto!

```bash
docker-compose up
# http://localhost:3000
```

**Qualquer dúvida, me avise!**

---

*Última atualização: 16 de setembro de 2026*  
*Versão: 0.4.0*
