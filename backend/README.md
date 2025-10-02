# Backend - Calculadora de Energia

API Flask para cálculo de conta de energia elétrica.

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
python app.py
```

O servidor estará disponível em `http://localhost:5000`

## Endpoints

### GET /health
Verifica se o servidor está online.

**Response:**
```json
{
  "status": "ok"
}
```

### POST /calculate
Calcula o valor da conta de energia.

**Request:**
```json
{
  "cep": "01310100",
  "consumo": 150
}
```

**Response:** Ver documentação principal

## Estrutura de Dados

### tarifas.json
Contém as tarifas de todas as distribuidoras do Brasil.

### bandeira.json
Contém a bandeira tarifária vigente e valores por kWh.

## Atualização de Dados

Para atualizar os dados, edite os arquivos JSON em `data/`.
