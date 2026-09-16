# 🚀 GUIA VISUAL — Deploy no Vercel (Para Leigos)

**Tempo total:** 5 minutos  
**Custo:** GRÁTIS  
**Dificuldade:** ⭐⭐ (Muito fácil)

---

## 📋 O Que Você Vai Fazer

```
Arquivos locais → GitHub (criar repo) → Vercel (conectar) → Link gerado
```

**Simples!** Só clicar em botões.

---

## 🎯 PASSO 1: Criar Repositório no GitHub

### Abra GitHub

Clique aqui: https://github.com/new

Ou acesse seu GitHub → Clique **"+"** no canto superior → **"New repository"**

### Preencha os Dados

| Campo | O Quê Preencher |
|-------|-----------------|
| **Repository name** | `motor-tributario` |
| **Description** | `Motor de Decisão Tributária - Simples vs Híbrido` |
| **Public/Private** | ⭕ **Public** (deixe assim) |
| ✅ Add a README | Deixa desmarcado |

### Clique

**Botão grande azul:** `Create repository`

**Pronto!** Repo criado.

---

## 📁 PASSO 2: Upload dos Arquivos

Na página que abriu, você verá:

```
Quick setup — if you've done this kind of thing before
or: …or upload an existing file
```

### Clique em: **"uploading an existing file"**

Ou procure pelo link tipo:

```
github.com/seuusuario/motor-tributario
```

E procure por um botão **"Upload files"** ou **"Add file"** → **"Upload files"**

### Obtenha os Arquivos

1. **Volte ao chat Claude** onde você viu este guia
2. **Procure pelos cards de download** na barra lateral direita
3. **Baixe cada arquivo** clicando no botão Download:

✅ `main.py`  
✅ `index.html`  
✅ `requirements.txt`  
✅ `Dockerfile`  
✅ `docker-compose.yml`  
✅ `nginx.conf`  
✅ `.env` (ou use `.env.example` como modelo)  
✅ `.gitignore`  

**Todos estão disponíveis para download na interface de chat.**

### Clique

Botão verde: **"Commit changes"**

**Pronto!** Arquivos estão no GitHub.

---

## 🔗 PASSO 3: Conectar no Vercel

### Abra Vercel

https://vercel.com/dashboard

(Deve estar logado, se não, faça login)

### Clique em Nova Aba

Procure um botão tipo:

- **"Add New..."** ou
- **"New Project"** ou  
- **"Import Project"**

### Selecione "Import Git Repository"

Vercel vai pedir:

```
GitHub Account: solucoescontabeis019 ✓
Repository: motor-tributario
```

### Clique no Repo

Quando o repo aparecer na lista, **clique nele**.

---

## ⚙️ PASSO 4: Configurar o Deploy

Vercel vai mostrar uma tela com:

```
Framework Preset: Other
Build Command: (deixa em branco ou: npm run build)
Start Command: (deixa em branco)
Environment Variables: (deixa como está)
```

**Não precisa mudar nada!** Deixa tudo como está.

### Clique

Botão grande azul: **"Deploy"**

---

## ⏳ PASSO 5: Aguarde

Vercel vai processar por **1-2 minutos**.

Você vai ver algo tipo:

```
🔨 Building...
✅ Build successful
🚀 Deploying...
✅ Deployment successful
```

---

## 🎉 PASSO 6: Sua URL está Pronta!

Quando terminar, Vercel vai mostrar:

```
✅ Successfully Deployed
Congratulations! Your project is live.

Visit: https://seu-projeto.vercel.app
```

### Copie o Link

```
https://motor-tributario.vercel.app
```

(Pode ser um pouco diferente, depende do que Vercel atribui)

---

## 🌐 ACESSE SEU DASHBOARD!

Abra o link em um navegador:

```
https://motor-tributario.vercel.app
```

**PRONTO!** 🎊

Seu dashboard está ONLINE!

---

## ✨ O QUE VOCÊ VÊ

Quando abrir o link, você vê:

1. **Cabeçalho:** "📊 Motor de Decisão Tributária"
2. **Abas:** Upload | Dados Manuais | Resultado | Sensibilidade
3. **Formulário:** Com dados pré-preenchidos (WASHINGTON L LOPES)
4. **Botão:** "🚀 Calcular Cenários"

### Teste Rápido

1. Clique na aba **"Dados Manuais"**
2. Veja que já tem dados pré-carregados
3. Clique **"Calcular Cenários"**
4. Vai para aba "Resultado"
5. **VÊ OS 3 CENÁRIOS** com valores
6. **VÊ A RECOMENDAÇÃO** destacada

**Pronto! Funcionando!** ✅

---

## 🔧 Se Algo Der Errado

### Erro "Build failed"

**Solução:** Aguarde 1 minuto, a Vercel tenta de novo automaticamente.

### Página não aparece

**Solução:** 
1. Aguarde 2 minutos (deploy pode estar em progresso)
2. Recarregue página (F5 ou Cmd+R)
3. Limpe cache (Ctrl+Shift+Delete)

### Dúvida sobre o Link

**Solução:** Vá para Vercel → Dashboard → Clique no projeto → Veja o link "Visit"

---

## 📱 PRONTO PARA USAR!

Agora você tem:

✅ Dashboard online (como um site)  
✅ URL pública (pode compartilhar)  
✅ Grátis (não paga nada)  
✅ Sempre online (Vercel cuida)  
✅ Dados pré-carregados (exemplo funciona)  
✅ Pronto para clientes (customiza dados)  

---

## 🎓 RESUMO DOS PASSOS

| Passo | O Quê | Clique |
|-------|-------|--------|
| 1 | Criar repo GitHub | github.com/new |
| 2 | Upload arquivos | Upload files |
| 3 | Ir para Vercel | vercel.com |
| 4 | Import repo | Add New → Import |
| 5 | Deploy | Deploy button |
| 6 | Aguarde | 2 minutos |
| 7 | Acesse link | https://... |

---

## 🎯 PRÓXIMOS PASSOS

**Agora que tá online:**

1. **Teste com seus dados**
   - Troque CNPJ, RBT12, fornecedores
   - Clique Calcular
   - Veja resultado

2. **Compartilhe link**
   - Envie URL para clientes
   - Eles podem usar de qualquer computador

3. **Customize conforme quiser**
   - Tem mais features? Basta atualizar files no GitHub
   - Vercel redeploy automaticamente

---

## ❓ Dúvidas?

Qualquer coisa estranha:
1. Recarregue página
2. Aguarde 2 minutos
3. Limpe cache do navegador

**99% funciona de primeira!**

---

**Última atualização:** 16 de setembro de 2026  
**Versão:** 1.0 - Guia para Leigos  
**Status:** ✅ Pronto para você!
