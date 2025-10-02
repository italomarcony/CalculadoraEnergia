from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests

app = Flask(__name__)
CORS(app)

# Caminho para os dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'backend', 'data')

# Cache para dados
_tarifas_cache = None
_bandeira_cache = None

# Carregar dados de tarifas
def load_tarifas():
    global _tarifas_cache
    if _tarifas_cache is None:
        tarifa_path = os.path.join(DATA_DIR, 'tarifas.json')
        with open(tarifa_path, 'r', encoding='utf-8') as f:
            _tarifas_cache = json.load(f)
    return _tarifas_cache

# Carregar bandeira tarifária atual
def load_bandeira():
    global _bandeira_cache
    if _bandeira_cache is None:
        bandeira_path = os.path.join(DATA_DIR, 'bandeira.json')
        with open(bandeira_path, 'r', encoding='utf-8') as f:
            _bandeira_cache = json.load(f)
    return _bandeira_cache

@app.route('/calculate', methods=['POST'])
@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        cep = data.get('cep', '').replace('-', '').strip()
        consumo = float(data.get('consumo', 0))

        if not cep or consumo <= 0:
            return jsonify({'error': 'CEP e consumo são obrigatórios'}), 400

        # Buscar estado pela API ViaCEP
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')

        if response.status_code != 200:
            return jsonify({'error': 'CEP inválido'}), 400

        cep_data = response.json()

        if 'erro' in cep_data:
            return jsonify({'error': 'CEP não encontrado'}), 404

        estado = cep_data.get('uf')

        # Carregar dados de tarifas e bandeira
        tarifas = load_tarifas()
        bandeira_data = load_bandeira()

        # Buscar tarifa do estado
        tarifa_estado = None
        for tarifa in tarifas['tarifas']:
            if tarifa['estado'] == estado:
                tarifa_estado = tarifa
                break

        if not tarifa_estado:
            return jsonify({'error': 'Estado não encontrado na base de dados'}), 404

        # Calcular valor
        tarifa_kwh = tarifa_estado['tarifa']
        valor_energia = consumo * tarifa_kwh

        # Adicionar valor da bandeira
        bandeira = bandeira_data['bandeira_atual']
        valor_bandeira_kwh = bandeira_data['valor_kwh']
        valor_bandeira_total = consumo * valor_bandeira_kwh

        valor_total = valor_energia + valor_bandeira_total

        # Encontrar estados mais barato e mais caro
        tarifas_ordenadas = sorted(tarifas['tarifas'], key=lambda x: x['tarifa'])
        mais_barato = tarifas_ordenadas[0]
        mais_caro = tarifas_ordenadas[-1]

        return jsonify({
            'distribuidora': tarifa_estado['distribuidora'],
            'estado': estado,
            'tarifa': tarifa_kwh,
            'bandeira': bandeira,
            'valor_bandeira': valor_bandeira_total,
            'valor_total': valor_total,
            'comparacao': {
                'mais_barato': {
                    'estado': mais_barato['estado'],
                    'tarifa': mais_barato['tarifa']
                },
                'mais_caro': {
                    'estado': mais_caro['estado'],
                    'tarifa': mais_caro['tarifa']
                }
            },
            'ultima_atualizacao_dados': tarifas['ultima_atualizacao']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'API is running'})

# Handler para Vercel serverless
if __name__ != '__main__':
    # Vercel WSGI Handler
    from werkzeug.wrappers import Request, Response

    @Request.application
    def application(request):
        return app.wsgi_app(request.environ, lambda *args: None)
