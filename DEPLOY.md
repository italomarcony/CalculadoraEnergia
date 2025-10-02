# 🚀 Deploy na Vercel

Este guia mostra como fazer o deploy da Calculadora de Energia na Vercel.

## 📋 Pré-requisitos

1. Conta na [Vercel](https://vercel.com) (gratuita)
2. Projeto no GitHub (já configurado)

## 🔧 Configuração do Projeto

O projeto já está configurado para deploy na Vercel com:

- ✅ **Serverless Functions**: API Flask convertida para `/api/index.py`
- ✅ **Frontend React**: Build otimizado com Vite
- ✅ **Configuração**: Arquivo `vercel.json` pronto
- ✅ **Dependências**: `requirements.txt` criado

## 📦 Estrutura para Deploy

```
CalculadoraEnergia/
├── api/
│   └── index.py          # Flask serverless function
├── frontend/
│   ├── src/
│   ├── dist/             # Build do Vite (gerado)
│   └── package.json
├── backend/
│   └── data/
│       ├── tarifas.json  # Dados da ANEEL
│       └── bandeira.json # Bandeira tarifária
├── vercel.json           # Configuração da Vercel
└── requirements.txt      # Dependências Python
```

## 🚀 Passos para Deploy

### Opção 1: Via Dashboard da Vercel (Recomendado)

1. **Acesse** [vercel.com](https://vercel.com) e faça login

2. **Clique** em "Add New Project"

3. **Importe** o repositório:
   - Selecione "Import Git Repository"
   - Escolha: `italomarcony/CalculadoraEnergia`

4. **Configure o projeto**:
   - **Framework Preset**: Vite
   - **Root Directory**: `./` (deixe em branco)
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`

5. **Variáveis de Ambiente** (se necessário):
   - Não há variáveis secretas neste projeto

6. **Deploy**: Clique em "Deploy"

### Opção 2: Via Vercel CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Fazer login
vercel login

# Deploy (na pasta do projeto)
vercel

# Deploy em produção
vercel --prod
```

## 🔄 Deploy Automático

Após o primeiro deploy, a Vercel irá:

- ✅ Fazer deploy automático a cada `git push` na branch `main`
- ✅ Criar preview deployments para pull requests
- ✅ Atualizar o site em segundos

## 🌐 URLs Após Deploy

Você receberá duas URLs:

1. **Production**: `https://calculadora-energia.vercel.app` (ou domínio customizado)
2. **Preview**: URLs únicas para cada branch/PR

## 🧪 Testar Localmente Antes do Deploy

```bash
# Backend (Flask)
cd backend
python app.py

# Frontend (Vite)
cd frontend
npm install
npm run dev
```

Acesse: `http://localhost:3000`

## 🔍 Troubleshooting

### Erro: "Build failed"
- Verifique se `frontend/package.json` tem o script `vercel-build`
- Confirme que `requirements.txt` está na raiz do projeto

### Erro: "API não responde"
- Verifique se os arquivos de dados estão em `backend/data/`
- Confirme que `api/index.py` está importando corretamente

### Erro: "Routes not working"
- Verifique `vercel.json` - rotas devem estar corretas
- API deve estar em `/api/*` e frontend em `/`

## 📊 Monitoramento

Após o deploy, você pode:

- Ver logs em tempo real no dashboard da Vercel
- Monitorar performance e analytics
- Configurar domínio customizado
- Ativar HTTPS automático (já incluído)

## 🔒 Segurança

- ✅ HTTPS automático
- ✅ Headers de segurança configurados
- ✅ CORS configurado corretamente
- ✅ Sem credenciais expostas

## 📝 Notas Importantes

1. **Dados estáticos**: As tarifas da ANEEL estão em arquivos JSON estáticos
2. **Atualização**: Para atualizar tarifas, rode `sync_aneel_data.py` localmente e faça commit
3. **Limite gratuito**: Vercel oferece 100GB de banda por mês (gratuito)
4. **Serverless**: A API roda como serverless function (cold start ~1s)

## 🆘 Suporte

- [Documentação Vercel](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- Issues: Abra no [repositório do projeto](https://github.com/italomarcony/CalculadoraEnergia/issues)

---

**Feito com ❤️ por [Ítalo Marcony](https://github.com/italomarcony)**
