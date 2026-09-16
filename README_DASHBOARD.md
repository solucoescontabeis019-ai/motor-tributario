# 🚀 Motor de Decisão Tributária — Dashboard Web

**Versão:** 0.4.0  
**Status:** MVP — Fase 1 Essencial  
**Data:** 16 de setembro de 2026

---

## 📋 O Que É?

Dashboard web profissional para análise tributária de empresas brasileiras, comparando:

- **2026 Real** — Tributação atual (Simples Nacional)
- **2027 Simples Puro** — Mantendo Simples Nacional
- **2027 Híbrido** — Simples + IBS/CBS regime regular

Recomenda qual modelo é mais vantajoso economicamente.

---

## 🎯 Funcionalidades Entregues (Fase 1)

✅ **Interface Web Responsiva**
- Dashboard limpo e profissional
- 4 abas: Upload, Dados Manuais, Resultado, Sensibilidade
- Suporta desktop e mobile

✅ **Entrada de Dados**
- Upload de PDFs (estrutura pronta, implementar parser em Fase 2)
- Formulário manual para CNPJ, RBT12, DAS, fornecedores, clientes
- Dados pré-preenchidos com exemplo da empresa WASHINGTON L LOPES

✅ **Cálculos Tributários**
- 2026 Real (validado)
- 2027 Simples Puro (projeção)
- 2027 Simples Híbrido (com débitos/créditos)

✅ **Visualização**
- Cards com valores dos 3 cenários
- Recomendação destacada com ícone
- Tabelas de fornecedores e clientes
- Gráfico de comparação (Chart.js)

✅ **Backend API (FastAPI)**
- `POST /api/calcular` — Processa dados
- `GET /api/resultado/{id}` — Retorna resultado
- `GET /api/resultado/{id}/download` — Download JSON
- Health checks

✅ **Deploy**
- Docker Compose para orquestração
- Backend FastAPI + Frontend Nginx
- Pronto para rodar localmente ou nuvem

---

## 🛠️ Como Começar

### Opção 1: Localmente (Recomendado para Teste)

#### Pré-requisitos
- Python 3.11+
- Node.js 18+ (opcional)
- Docker + Docker Compose (mais fácil)

#### Passos

```bash
# 1. Clone ou copie os arquivos para uma pasta
mkdir motor-tributario-web
cd motor-tributario-web

# 2. Copie todos os arquivos:
# - main.py
# - requirements.txt
# - index.html
# - docker-compose.yml
# - Dockerfile
# - nginx.conf
# - .env.example

# 3. Crie arquivo .env
cp .env.example .env

# 4. Rode com Docker Compose
docker-compose up

# 5. Acesse em navegador
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Swagger API Docs: http://localhost:8000/docs
```

#### Sem Docker (Python puro)

```bash
# 1. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instale dependências
pip install -r requirements.txt

# 3. Rode FastAPI
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Em outro terminal, abra index.html
# Abra em navegador: file:///caminho/para/index.html
# (Pode ter CORS issues sem Nginx)

# Melhor: use um servidor web simples
python -m http.server 8080
# Acessa: http://localhost:8080
```

---

## 📊 Usando o Dashboard

### Fluxo Básico

1. **Preencher Dados** (Aba "Dados Manuais")
   - CNPJ, Razão Social, RBT12, DAS
   - Fornecedores (CNPJ, nome, total compras)
   - Clientes (CNPJ, nome, faturamento)
   - Dados de exemplo já estão pré-carregados

2. **Calcular** (Botão "Calcular Cenários")
   - Backend processa dados
   - Calcula 3 cenários
   - Gera recomendação

3. **Visualizar Resultado** (Aba "Resultado")
   - 3 cards com valores
   - Recomendação destacada
   - Tabelas detalhadas
   - Download JSON

---

## 🔄 Fluxo de Requisição

```
Frontend (HTML/JS)
       ↓
    [POST] /api/calcular
       ↓
Backend (FastAPI)
  ├─ Valida dados
  ├─ Calcula 2026
  ├─ Calcula 2027 Simples
  ├─ Calcula 2027 Híbrido
  ├─ Compara e recomenda
  └─ Salva resultado JSON
       ↓
    [JSON Response]
       ↓
Frontend mostra resultado
```

---

## 📁 Estrutura de Pastas

```
motor-tributario-web/
├── main.py                  # Backend FastAPI
├── index.html              # Frontend (SPA)
├── requirements.txt        # Dependências Python
├── docker-compose.yml      # Orquestração Docker
├── Dockerfile              # Build image Docker
├── nginx.conf              # Config servidor web
├── .env.example            # Variáveis de ambiente
├── .env                    # (Criar localmente)
├── uploads/                # PDFs uploadados (auto-criado)
├── reports/                # JSONs de resultado (auto-criado)
└── README.md               # Este arquivo
```

---

## 🔗 URLs Principais

| URL | Descrição |
|-----|-----------|
| `http://localhost:3000` | Dashboard Frontend |
| `http://localhost:8000` | API Backend |
| `http://localhost:8000/docs` | Swagger UI (testes API) |
| `http://localhost:8000/health` | Health check |

---

## 📝 Exemplos de Requisição

### Calcular Cenários

```bash
curl -X POST http://localhost:8000/api/calcular \
  -H "Content-Type: application/json" \
  -d '{
    "empresa": {
      "cnpj": "04.286.335/0001-79",
      "razao_social": "WASHINGTON L LOPES COSMOPOLIS",
      "cidade": "Cosmópolis",
      "uf": "SP",
      "regime": "Simples Nacional",
      "anexo": "III",
      "rbt12": 2236444.92,
      "das": 18607.42
    },
    "fornecedores": [
      {
        "cnpj": "10.567.953/0001-90",
        "razao_social": "AUTO POSTO MP FERNANDES",
        "compras": 145907.57
      }
    ],
    "clientes": [
      {
        "cnpj": "06.980.064/0001-XX",
        "razao_social": "NACIONAL GÁS BUTANO DISTRIBUIDORA LTDA",
        "faturamento": 1948000
      }
    ],
    "cbs_estimada": 8.80
  }'
```

### Obter Resultado

```bash
curl http://localhost:8000/api/resultado/{simulacao_id}
```

---

## 🚀 Próximas Fases (Roadmap)

### Fase 2 — Features Importantes (1-2 semanas)
- [x] Parser automático de PDFs (PGDAS, Entradas, Saídas, Serviços)
- [x] Gráficos interativos (Chart.js)
- [x] Memória de cálculo ("Ver como foi calculado")
- [x] Simulação sensibilidade (CBS, faturamento, compras)
- [x] Relatório PDF profissional
- [x] Análise detalhada de fornecedores e clientes

### Fase 3 — Enterprise (2-3 semanas)
- [ ] Autenticação de usuários (JWT)
- [ ] Multi-cliente (histórico de simulações)
- [ ] Dashboard com lista de clientes
- [ ] Export Excel
- [ ] Monitoramento de legislação (alerta quando CBS publicada)
- [ ] Mobile responsivo otimizado
- [ ] PWA (Progressive Web App)

---

## 🌐 Deploy na Nuvem

### Opção 1: Vercel (Frontend) + Render (Backend)

```bash
# 1. Frontend no Vercel
cd frontend
vercel deploy

# 2. Backend no Render
# Conectar repo GitHub ao Render
# Selecionar "Python"
# Build: pip install -r requirements.txt
# Start: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Opção 2: AWS Elastic Beanstalk

```bash
# 1. Criar aplicação
eb create motor-app

# 2. Deploy
eb deploy
```

### Opção 3: Railway.app

```bash
# Deploy automático do GitHub
# Conectar repo ao Railway
# Configurar variáveis .env
# Automático!
```

---

## 🔐 Segurança (Produção)

Para deploy em produção:

1. **Variáveis de Ambiente**
   - Alterar `SECRET_KEY` em .env
   - Usar `DEBUG=False`

2. **CORS**
   - Alterar `CORS_ORIGINS` para domínio real

3. **Banco de Dados**
   - Trocar SQLite por PostgreSQL

4. **HTTPS**
   - Usar certificado SSL/TLS
   - Nginx redirecionar HTTP → HTTPS

5. **Rate Limiting**
   - Implementar em FastAPI (Fase 2)

---

## 🐛 Troubleshooting

### Problema: CORS error na requisição

**Solução:**
```bash
# Verifique se backend está rodando
curl http://localhost:8000/health

# Verifique CORS_ORIGINS em .env
# Deve incluir http://localhost:3000
```

### Problema: Porta 8000 já está em uso

```bash
# Mude a porta em docker-compose.yml ou .env
# Ou encerre processo:
lsof -i :8000
kill -9 <PID>
```

### Problema: Frontend não conecta com API

**Debug:**
1. Abra DevTools (F12) → Network
2. Veja requisições para `/api/calcular`
3. Verifique resposta (status, erro)
4. Confirme URL base correta em index.html

---

## 📊 Exemplo de Resposta

```json
{
  "simulacao_id": "a1b2c3d4-e5f6-7890",
  "timestamp": "2026-09-16T17:45:32",
  "empresa": {
    "cnpj": "04286335000179",
    "razao_social": "WASHINGTON L LOPES COSMOPOLIS",
    "rbt12": 2236444.92,
    "das": 18607.42
  },
  "cenario_2026_real": 18607.42,
  "cenario_2027_simples_puro": 18607.42,
  "cenario_2027_hibrido": 86873.14,
  "recomendacao": "MANTER_SIMPLES_NACIONAL",
  "economia_anual": 68265.72,
  "confianca": "ALTA",
  "observacoes": [
    "Economia significativa: R$ 68.265,72",
    "⚠️ Concentração crítica: 89% do faturamento em um único cliente",
    "CBS utilizada: 8.80% (estimada)"
  ]
}
```

---

## 📞 Suporte

Para dúvidas ou bugs:

1. Verifique logs (`docker-compose logs backend`)
2. Teste manualmente requisições via Swagger (http://localhost:8000/docs)
3. Verifique console do navegador (F12 → Console)

---

## 📄 Licença

Uso interno — Desenvolvido para Priscila Videschi

---

## 🎉 Pronto para Começar!

```bash
docker-compose up
# Acessa: http://localhost:3000
```

**Qualquer dúvida ou problema, avise!**

---

**Última atualização:** 16 de setembro de 2026  
**Versão:** 0.4.0 (MVP)  
**Status:** ✅ Pronto para uso local
