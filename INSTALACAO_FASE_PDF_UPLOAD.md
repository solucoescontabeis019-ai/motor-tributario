# 🚀 Motor de Decisão Tributária — Versão com Upload de PDFs

## ✅ O que foi implementado:

### 1. **Backend FastAPI atualizado (main.py v0.5.0)**
- ✅ Endpoints de upload e processamento de PDFs
- ✅ Integração com pdf_parser.py
- ✅ Extração automática de dados estruturados
- ✅ Armazenamento de resultados

### 2. **Frontend atualizado (index.html v2.1)**
- ✅ Interface drag-and-drop para PDFs
- ✅ Processamento em tempo real
- ✅ Preview dos dados extraídos
- ✅ Preenchimento automático do formulário

### 3. **PDF Parser (pdf_parser.py)**
- ✅ Leitura de PGDAS-D
- ✅ Extração de Entradas (compras)
- ✅ Extração de Saídas (vendas)
- ✅ Extração de Serviços
- ✅ Normalização de CNPJ e valores

---

## 📋 Arquivos a usar:

```
main.py                    ← Backend com novos endpoints
index.html                 ← Frontend com upload
pdf_parser.py              ← Parser de PDFs
requirements.txt           ← Dependências Python
Dockerfile                 ← Container Docker
```

---

## 🔄 Fluxo de funcionamento:

```
1. Usuário arrasta PDFs
         ↓
2. Upload para servidor
         ↓
3. Processamento automático
         ↓
4. Extração de dados estruturados
         ↓
5. Preview no navegador
         ↓
6. Clique em "Usar Dados Extraídos"
         ↓
7. Preenchimento automático do formulário
         ↓
8. Cálculo dos 3 cenários tributários
```

---

## 🚀 Como fazer o deploy:

### Opção 1: Render.com (Recomendado — como antes)

1. **Fazer push dos arquivos no GitHub:**
   ```bash
   git add main.py index.html pdf_parser.py requirements.txt Dockerfile
   git commit -m "Adicionar upload de PDFs com extração automática"
   git push origin main
   ```

2. **Render.com redeploy automaticamente**
   - Acesse seu dashboard em render.com
   - Clique em "Deploy" ou aguarde auto-deploy

3. **Testar em:** https://seu-app.onrender.com

### Opção 2: Rodar localmente para teste

```bash
# Instalar dependências
pip install -r requirements.txt --break-system-packages

# Rodar servidor
python main.py

# Abrir no navegador
http://localhost:8000
```

---

## 📊 Dados de teste disponíveis:

Você já tem 6 PDFs para testar:
- `Simples Nacional WAS.pdf` (PGDAS-D)
- `Entradas.pdf` (lista de fornecedores)
- `Saídas.pdf` (lista de clientes)
- `Serviços.pdf` (receita de serviços)
- `RELAÇÃO DE FORNECEDORES.pdf`
- `RELAÇÃO DE CLIENTES.pdf`

---

## ✨ Novos recursos:

### ✅ Na aba "Upload":
1. **Área drag-and-drop** — Arraste PDFs aqui
2. **Processamento automático** — Sistema extrai dados sozinho
3. **Preview estruturado** — Mostra o que foi extraído:
   - CNPJ, Razão Social, RBT12, DAS
   - Lista de fornecedores com valores
   - Lista de clientes com valores
   - Quantidade de itens
   - Botão "Ver itens" para expandir tabela

4. **Botão "Usar Dados Extraídos"** — Preenche o formulário automaticamente
5. **Validação de erros** — Se houver falha em algum PDF, mostra o erro

---

## 🔍 Detalhes técnicos:

### Novos endpoints:

**POST /api/upload**
- Recebe: lista de PDFs
- Retorna: upload_id + lista de arquivos

**POST /api/processar-pdfs?upload_id=XXX**
- Processa PDFs de um upload
- Extrai dados estruturados
- Retorna lista com dados de cada PDF

**GET /api/dados-extraidos/{upload_id}**
- Obtém dados extraídos anteriormente
- Retorna JSON com todas as extrações

---

## 📝 Exemplo de resposta de extração:

```json
{
  "arquivo": "Simples Nacional WAS.pdf",
  "tipo": "PGDAS",
  "sucesso": true,
  "dados": {
    "cnpj": "04.286.335/0001-79",
    "razao_social": "WASHINGTON L LOPES COSMOPOLIS",
    "rbt12": 2236444.92,
    "das": 18607.42,
    "periodo": "08/2026"
  }
}
```

---

## 🐛 Se algo não funcionar:

### "Upload não funciona"
1. Verifique se os arquivos estão em .pdf
2. Reinicie o servidor
3. Limpe cache do navegador (Ctrl+Shift+Del)

### "Dados não aparecem"
1. Verifique se PDF tem tabelas legíveis
2. Tente com os PDFs de teste primeiro
3. Veja console do navegador (F12) para erros

### "Erro ao processar"
1. Pode ser PDF com imagem/scaneado
2. Tente outro PDF
3. Comunique para que eu melhore o parser

---

## 🎯 Próximas fases:

- ✅ **Fase atual:** Upload + Extração de PDFs
- 🔵 **Fase 2:** Consulta de CNPJ (validar regime)
- 🔵 **Fase 3:** Cálculo avançado de créditos
- 🔵 **Fase 4:** Relatório PDF para download
- 🔵 **Fase 5:** Banco de dados PostgreSQL

---

## ✅ Checklist de testes:

- [ ] Upload de PDF funciona
- [ ] Preview mostra dados extraídos
- [ ] Clique em "Usar Dados Extraídos" preenche formulário
- [ ] Cálculo dos 3 cenários funciona
- [ ] Resultado aparece na aba "Resultado"

---

## 📞 Suporte:

Se der erro no upload:
1. Confira que é PDF real (não imagem)
2. Veja o console (F12 → Console)
3. Copie a mensagem de erro
4. Comunique para que eu corrija

---

**Versão:** 0.5.0  
**Data:** 2026-09-17  
**Status:** ✅ Pronto para deploy
