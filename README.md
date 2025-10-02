# ⚡ Calculadora de Conta de Energia

Aplicação full-stack para calcular o valor estimado da conta de energia elétrica com base no CEP, consumo em kWh e bandeira tarifária vigente, utilizando **dados oficiais da ANEEL** obtidos via API.

> 🎯 **Dados Reais:** Este projeto utiliza a API de Dados Abertos da ANEEL para obter tarifas homologadas vigentes de distribuidoras de todo o Brasil.

## ✨ Funcionalidades

- ✅ Cálculo automático do valor da conta de energia
- 📍 Identificação da distribuidora por CEP
- 🚦 Inclusão da bandeira tarifária mensal no cálculo
- 📊 Comparação com estados mais barato e mais caro
- 💰 Valores baseados em tarifas oficiais da ANEEL
- 📱 Interface responsiva e moderna

## 🛠️ Tecnologias

### Frontend
- React 18
- Vite
- Tailwind CSS
- Axios

### Backend
- Python 3
- Flask
- Flask-CORS
- Requests

### Dados
- API ViaCEP para busca de localização
- Tarifas da ANEEL (outubro 2025)
- Bandeiras tarifárias atualizadas

## 📋 Pré-requisitos

- Node.js 18+ e npm
- Python 3.8+
- pip

## 🚀 Instalação e Execução

### Backend

```bash
# Navegar para a pasta do backend
cd backend

# Instalar dependências
pip install -r requirements.txt

# Executar o servidor
python app.py
```

O backend estará rodando em `http://localhost:5000`

### Frontend

```bash
# Navegar para a pasta do frontend
cd frontend

# Instalar dependências
npm install

# Executar o servidor de desenvolvimento
npm run dev
```

O frontend estará rodando em `http://localhost:3000`

## 📁 Estrutura do Projeto

```
CalculadoraEnergia/
├── backend/
│   ├── data/
│   │   ├── tarifas.json      # Tarifas por estado/distribuidora
│   │   └── bandeira.json     # Bandeira tarifária vigente
│   ├── app.py                # API Flask
│   └── requirements.txt      # Dependências Python
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── EnergyCalculator.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── energia.json              # Especificação do projeto
```

## 🔌 API Endpoints

### POST /calculate

Calcula o valor da conta de energia.

**Request:**
```json
{
  "cep": "01310100",
  "consumo": 150
}
```

**Response:**
```json
{
  "distribuidora": "Enel São Paulo",
  "estado": "SP",
  "tarifa": 0.73234,
  "bandeira": "Vermelha Patamar 1",
  "valor_bandeira": 6.69,
  "valor_total": 116.54,
  "comparacao": {
    "mais_barato": {
      "estado": "DF",
      "tarifa": 0.68234
    },
    "mais_caro": {
      "estado": "AM",
      "tarifa": 0.92341
    }
  },
  "ultima_atualizacao_dados": "outubro de 2025"
}
```

## 📊 Fonte dos Dados

✅ **DADOS OFICIAIS DA ANEEL:** O projeto utiliza tarifas **REAIS** obtidas diretamente da API de Dados Abertos da ANEEL.

- **Tarifas**: API de Dados Abertos da ANEEL (Tarifas Homologadas Vigentes)
- **Bandeiras Tarifárias**: Valores oficiais da ANEEL
- **CEP**: API ViaCEP para identificação do estado
- **Atualização**: Automática via script `sync_aneel_data.py`

### Fontes Oficiais:
- **API da ANEEL:** https://dadosabertos.aneel.gov.br/
- **Dataset de Tarifas:** https://dadosabertos.aneel.gov.br/dataset/tarifas-distribuidoras-energia-eletrica
- **Bandeiras Tarifárias:** https://www.aneel.gov.br/bandeiras-tarifarias
- **Resource ID:** fcf2906c-7c32-4b9b-a637-054e7a5234f4

## 🎨 Interface

A interface possui:
- Formulário para entrada de CEP e consumo
- Validação e formatação automática do CEP
- Exibição detalhada dos resultados
- Comparação com tarifas de outros estados
- Informações sobre a bandeira tarifária
- Design responsivo e moderno com Tailwind CSS

## 🔄 Atualização de Dados

### Sincronização Automática com API da ANEEL (Recomendado) ⭐

Execute o script para buscar dados oficiais diretamente da API:

```bash
cd backend
python sync_aneel_data.py
```

**O que o script faz:**
- ✅ Busca tarifas homologadas vigentes da API da ANEEL
- ✅ Filtra apenas tarifas residenciais (Grupo B1)
- ✅ Converte automaticamente de R$/MWh para R$/kWh
- ✅ Mapeia distribuidoras para estados
- ✅ Cria backup automático dos dados anteriores
- ✅ Atualiza `tarifas.json` com dados reais

**Frequência recomendada:** Mensal

### Atualização Manual da Bandeira

Para atualizar apenas a bandeira tarifária:

```bash
cd backend
python update_data.py
# Escolha opção 1 - Atualizar Bandeira Tarifária
```

Consulte a bandeira vigente em: https://www.aneel.gov.br/bandeiras-tarifarias

## 🚀 Deploy

### Frontend (Vercel)
```bash
cd frontend
npm run build
# Deploy a pasta dist/ para Vercel
```

### Backend (Render)
1. Crie um novo Web Service no Render
2. Conecte o repositório
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Environment: Python 3

## 📝 Notas Importantes

### ⚠️ Sobre os Valores Calculados

- **Dados OFICIAIS da ANEEL** - Tarifas homologadas vigentes
- **NÃO inclui impostos** - ICMS (18-33%), PIS/COFINS (~3-4%)
- **NÃO inclui taxas adicionais** - Iluminação pública, encargos setoriais
- **Valor final pode ser 25-40% maior** devido aos impostos estaduais e federais

### 📅 Manutenção dos Dados

- **Tarifas**: Execute `sync_aneel_data.py` mensalmente para atualizar via API
- **Bandeira tarifária**: Atualize mensalmente via `update_data.py`
- **Automático**: Os dados vêm diretamente da API da ANEEL (sempre atualizados)

### 🔍 Transparência dos Dados

**Fonte:** API de Dados Abertos da ANEEL
- Dataset: Tarifas Homologadas das Distribuidoras de Energia Elétrica
- Valores em R$/kWh (convertidos de R$/MWh)
- Subgrupo B1 (Residencial)
- Modalidade: Convencional

Para conferir os dados oficiais:
- [Portal de Dados Abertos da ANEEL](https://dadosabertos.aneel.gov.br/)
- [Site oficial da ANEEL](https://www.aneel.gov.br/)

## 📄 Licença

Este projeto é livre para uso educacional e pessoal.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.
