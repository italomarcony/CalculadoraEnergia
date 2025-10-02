"""
Script para sincronizar dados reais da API da ANEEL.

Este script busca:
1. Tarifas homologadas vigentes (Grupo B1 - Residencial)
2. Bandeira tarifária atual

E atualiza os arquivos JSON da aplicação com dados oficiais.
"""

import requests
import json
import os
from datetime import datetime
from collections import defaultdict

# Configuração da API
API_BASE = "https://dadosabertos.aneel.gov.br/api/3/action/datastore_search"

# Resource IDs oficiais
RESOURCE_TARIFAS = "fcf2906c-7c32-4b9b-a637-054e7a5234f4"  # Tarifas homologadas
RESOURCE_BANDEIRA = "0591b8f6-fe54-437b-b72b-1aa2efd46e42"  # Bandeira acionamento

# Diretório de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Mapeamento DISTRIBUIDORA → ESTADO
# Baseado em informações públicas das principais distribuidoras
DISTRIBUIDORA_ESTADO = {
    # Acre
    'ELETROACRE': 'AC',
    'ENERGISA ACRE': 'AC',

    # Alagoas
    'CEAL': 'AL',
    'EQUATORIAL ALAGOAS': 'AL',

    # Amapá
    'CEA': 'AP',

    # Amazonas
    'AMAZONAS ENERGIA': 'AM',
    'ELETROBRÁS AMAZONAS': 'AM',

    # Bahia
    'COELBA': 'BA',
    'NEOENERGIA COELBA': 'BA',

    # Ceará
    'COELCE': 'CE',
    'ENEL CEARÁ': 'CE',
    'ENEL CE': 'CE',

    # Distrito Federal
    'CEB': 'DF',
    'CEB DISTRIBUIÇÃO': 'DF',
    'CEB DIS': 'DF',

    # Espírito Santo
    'ESCELSA': 'ES',
    'EDP ESPÍRITO SANTO': 'ES',
    'EDP ES': 'ES',

    # Goiás
    'CELG': 'GO',
    'ENEL GOIÁS': 'GO',
    'ENEL GO': 'GO',

    # Maranhão
    'CEMAR': 'MA',
    'EQUATORIAL MARANHÃO': 'MA',

    # Mato Grosso
    'CEMAT': 'MT',
    'ENERGISA MATO GROSSO': 'MT',

    # Mato Grosso do Sul
    'ENERSUL': 'MS',
    'ENERGISA MATO GROSSO DO SUL': 'MS',
    'ENERGISA MS': 'MS',

    # Minas Gerais
    'CEMIG': 'MG',
    'CEMIG DISTRIBUIÇÃO': 'MG',
    'CEMIG-D': 'MG',

    # Pará
    'CELPA': 'PA',
    'EQUATORIAL PARÁ': 'PA',

    # Paraíba
    'EPB': 'PB',
    'ENERGISA PARAÍBA': 'PB',
    'ENERGISA PB': 'PB',

    # Paraná
    'COPEL': 'PR',
    'COPEL DISTRIBUIÇÃO': 'PR',
    'COPEL-DIS': 'PR',

    # Pernambuco
    'CELPE': 'PE',
    'NEOENERGIA PERNAMBUCO': 'PE',

    # Piauí
    'CEPISA': 'PI',
    'EQUATORIAL PIAUÍ': 'PI',

    # Rio de Janeiro
    'LIGHT': 'RJ',
    'LIGHT SESA': 'RJ',
    'ENEL RIO': 'RJ',
    'ENEL RJ': 'RJ',

    # Rio Grande do Norte
    'COSERN': 'RN',
    'NEOENERGIA COSERN': 'RN',

    # Rio Grande do Sul
    'CEEE': 'RS',
    'CEEE-D': 'RS',
    'RGE': 'RS',
    'RGE SUL': 'RS',

    # Rondônia
    'CERON': 'RO',
    'ENERGISA RONDÔNIA': 'RO',

    # Roraima
    'CER': 'RR',
    'RORAIMA ENERGIA': 'RR',

    # Santa Catarina
    'CELESC': 'SC',
    'CELESC DISTRIBUIÇÃO': 'SC',
    'CELESC-DIS': 'SC',

    # São Paulo
    'CPFL': 'SP',
    'CPFL PAULISTA': 'SP',
    'CPFL-PAULISTA': 'SP',
    'CPFL PIRATININGA': 'SP',
    'CPFL-PIRATININGA': 'SP',
    'CPFL-PIRATINING': 'SP',
    'CPFL MOCOCA': 'SP',
    'ELEKTRO': 'SP',
    'ENEL SP': 'SP',
    'ENEL SÃO PAULO': 'SP',
    'EDP SÃO PAULO': 'SP',
    'BANDEIRANTE': 'SP',

    # Sergipe
    'SULGIPE': 'SE',
    'ENERGISA SERGIPE': 'SE',

    # Tocantins
    'CELTINS': 'TO',
    'ENERGISA TOCANTINS': 'TO',
}

def converter_valor(valor_str):
    """
    Converte valor da API para float.
    API retorna valores como "179,08" ou "1,85"
    """
    if not valor_str or valor_str == 'N/A':
        return 0.0

    try:
        # Remover espaços
        valor_str = str(valor_str).strip()
        # Trocar vírgula por ponto
        valor_str = valor_str.replace(',', '.')
        return float(valor_str)
    except:
        return 0.0

def identificar_estado(distribuidora):
    """
    Identifica o estado de uma distribuidora.
    """
    distribuidora_upper = distribuidora.upper().strip()

    # Tentar match exato
    if distribuidora_upper in DISTRIBUIDORA_ESTADO:
        return DISTRIBUIDORA_ESTADO[distribuidora_upper]

    # Tentar match parcial
    for nome, estado in DISTRIBUIDORA_ESTADO.items():
        if nome in distribuidora_upper or distribuidora_upper in nome:
            return estado

    return None

def buscar_tarifas_api(limit=50000):
    """
    Busca tarifas da API da ANEEL, filtrando por B1 (residencial).
    """
    print("🔍 Buscando tarifas residenciais da API da ANEEL...")

    # Tentar buscar especificamente B1
    url = f"{API_BASE}?resource_id={RESOURCE_TARIFAS}&q=B1&limit={limit}"

    try:
        response = requests.get(url, timeout=90)
        response.raise_for_status()

        data = response.json()

        if data.get('success'):
            records = data.get('result', {}).get('records', [])
            total = data.get('result', {}).get('total', 0)

            print(f"✅ Recebidos {len(records)} registros de {total} totais")
            print(f"   Buscando especificamente por 'B1' no dataset")
            return records
        else:
            print("❌ API retornou erro")
            return []

    except Exception as e:
        print(f"❌ Erro ao buscar API: {e}")
        return []

def processar_tarifas_b1(records):
    """
    Processa registros e extrai tarifas B1 vigentes por estado.
    """
    print("\n📊 Processando tarifas residenciais (B1)...")

    data_atual = datetime.now()
    tarifas_por_estado = {}

    # DEBUG: Ver estrutura dos dados
    if records:
        print("\n🔍 DEBUG - Analisando estrutura dos primeiros registros:")
        for i, record in enumerate(records[:3], 1):
            print(f"\n  Registro {i}:")
            print(f"    DscSubGrupo: {record.get('DscSubGrupo', 'N/A')}")
            print(f"    DscClasse: {record.get('DscClasse', 'N/A')}")
            print(f"    DscModalidadeTarifaria: {record.get('DscModalidadeTarifaria', 'N/A')}")
            print(f"    SigAgente: {record.get('SigAgente', 'N/A')}")

    for record in records:
        # Filtrar apenas B1 (pode vir em diferentes campos)
        subgrupo = str(record.get('DscSubGrupo', '')).upper()
        classe = str(record.get('DscClasse', '')).upper()
        modalidade = str(record.get('DscModalidadeTarifaria', '')).upper()

        # Verificar se é B1 residencial (critério mais flexível)
        # Muitos registros têm "N/A", então vamos também aceitar modalidade convencional
        eh_b1 = ('B1' in subgrupo or
                 'B1' in classe or
                 'RESIDENCIAL' in classe or
                 'CONVENCIONAL' in modalidade)

        if not eh_b1:
            continue

        # Verificar vigência
        try:
            data_inicio = record.get('DatInicioVigencia', '')
            data_fim = record.get('DatFimVigencia', '')

            if data_inicio and data_fim:
                inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
                fim = datetime.strptime(data_fim, '%Y-%m-%d')

                # Verificar se está vigente
                if not (inicio <= data_atual <= fim):
                    continue
        except:
            # Se não conseguir parsear data, ignora filtro de vigência
            pass

        # Pegar valores
        distribuidora = record.get('SigAgente', '').strip()
        tusd = converter_valor(record.get('VlrTUSD', 0))
        te = converter_valor(record.get('VlrTE', 0))

        if tusd == 0 and te == 0:
            continue

        # Calcular tarifa total
        # Valores estão em R$/MWh segundo dicionário de dados da ANEEL
        # Converter para R$/kWh: dividir por 1000
        tarifa_total = (tusd + te) / 1000
        tusd_kwh = tusd / 1000
        te_kwh = te / 1000

        # Identificar estado
        estado = identificar_estado(distribuidora)

        if not estado:
            continue

        # Guardar apenas mais recente por estado (data de vigência)
        try:
            data_vigencia_atual = datetime.strptime(record.get('DatFimVigencia', '1900-01-01'), '%Y-%m-%d')

            if estado not in tarifas_por_estado:
                tarifas_por_estado[estado] = {
                    'estado': estado,
                    'distribuidora': distribuidora,
                    'tarifa': round(tarifa_total, 5),
                    'tusd': round(tusd_kwh, 5),
                    'te': round(te_kwh, 5),
                    '_data_vigencia': data_vigencia_atual
                }
            else:
                # Substituir se for mais recente
                if data_vigencia_atual > tarifas_por_estado[estado]['_data_vigencia']:
                    tarifas_por_estado[estado] = {
                        'estado': estado,
                        'distribuidora': distribuidora,
                        'tarifa': round(tarifa_total, 5),
                        'tusd': round(tusd_kwh, 5),
                        'te': round(te_kwh, 5),
                        '_data_vigencia': data_vigencia_atual
                    }
        except:
            pass

    print(f"✅ Processados {len(tarifas_por_estado)} estados")

    # Remover campo auxiliar _data_vigencia antes de retornar
    tarifas_limpas = []
    for tarifa in tarifas_por_estado.values():
        tarifa_limpa = {k: v for k, v in tarifa.items() if not k.startswith('_')}
        tarifas_limpas.append(tarifa_limpa)

    return tarifas_limpas

def buscar_bandeira_atual():
    """
    Busca bandeira tarifária atual da API.
    """
    print("\n🚦 Buscando bandeira tarifária atual...")

    url = f"{API_BASE}?resource_id={RESOURCE_BANDEIRA}&limit=100"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        if data.get('success'):
            records = data.get('result', {}).get('records', [])

            if records:
                # Pegar registro mais recente
                registro_recente = max(records, key=lambda x: x.get('DatInicioVigencia', ''))

                bandeira = registro_recente.get('SigBandeiraTarifaria', 'VERDE')
                valor = converter_valor(registro_recente.get('ValorBandeira', 0))

                print(f"✅ Bandeira atual: {bandeira} - R$ {valor}/kWh")

                return {
                    'bandeira': bandeira,
                    'valor': valor
                }

        print("⚠️ Usando valores padrão de bandeiras")
        return None

    except Exception as e:
        print(f"❌ Erro ao buscar bandeira: {e}")
        return None

def salvar_tarifas(tarifas):
    """
    Salva tarifas no formato JSON da aplicação.
    """
    if not tarifas:
        print("❌ Nenhuma tarifa para salvar")
        return False

    print(f"\n💾 Salvando {len(tarifas)} tarifas...")

    data = {
        "ultima_atualizacao": datetime.now().strftime("%B de %Y"),
        "fonte": "API de Dados Abertos da ANEEL",
        "observacao": "Dados oficiais processados automaticamente",
        "tarifas": sorted(tarifas, key=lambda x: x['estado'])
    }

    output_path = os.path.join(DATA_DIR, 'tarifas.json')

    # Backup do arquivo anterior
    if os.path.exists(output_path):
        backup_path = output_path.replace('.json', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        os.rename(output_path, backup_path)
        print(f"💾 Backup criado: {os.path.basename(backup_path)}")

    # Salvar novo arquivo
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Tarifas salvas em: tarifas.json")

    # Mostrar preview
    print("\n📊 Preview das tarifas salvas:")
    print("-" * 70)
    print(f"{'Estado':<8} {'Distribuidora':<30} {'Tarifa (R$/kWh)':<15}")
    print("-" * 70)
    for tarifa in sorted(tarifas, key=lambda x: x['estado'])[:10]:
        print(f"{tarifa['estado']:<8} {tarifa['distribuidora']:<30} {tarifa['tarifa']:.5f}")
    if len(tarifas) > 10:
        print(f"... e mais {len(tarifas) - 10} estados")
    print("-" * 70)

    return True

def main():
    """Função principal."""
    print("\n" + "="*70)
    print("🔌 SINCRONIZAÇÃO DE DADOS DA ANEEL")
    print("="*70)
    print("\nEste script busca dados REAIS da API da ANEEL e atualiza a aplicação.")
    print()

    # 1. Buscar tarifas
    records = buscar_tarifas_api(limit=20000)

    if not records:
        print("\n❌ Não foi possível buscar dados da API")
        return

    # 2. Processar tarifas B1
    tarifas = processar_tarifas_b1(records)

    if not tarifas:
        print("\n❌ Nenhuma tarifa B1 encontrada")
        return

    # 3. Salvar tarifas
    if salvar_tarifas(tarifas):
        print("\n✅ SUCESSO! Dados sincronizados com a ANEEL")
    else:
        print("\n❌ Erro ao salvar dados")

    # 4. Buscar bandeira (opcional, comentado pois pode não funcionar bem)
    # bandeira = buscar_bandeira_atual()

    print("\n" + "="*70)
    print("📝 IMPORTANTE:")
    print("="*70)
    print("  • Verifique se os valores fazem sentido (~R$ 0.65 a R$ 0.95/kWh)")
    print("  • Compare com sua conta de energia para validar")
    print("  • A bandeira tarifária deve ser atualizada manualmente")
    print("  • Execute este script mensalmente para manter dados atualizados")
    print()

if __name__ == "__main__":
    main()
