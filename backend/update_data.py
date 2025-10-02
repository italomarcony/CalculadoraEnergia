"""
Script para atualizar dados de tarifas e bandeiras tarifárias.

Este script pode ser executado manualmente ou configurado em um cron job
para atualização automática mensal dos dados.

Fontes oficiais:
- ANEEL: https://dadosabertos.aneel.gov.br/
- Sistema de Bandeiras: https://www.aneel.gov.br/bandeiras-tarifarias
"""

import json
import requests
from datetime import datetime
import os

# Diretório de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def update_bandeira_manual():
    """
    Atualiza a bandeira tarifária manualmente.

    A ANEEL divulga a bandeira vigente mensalmente. Consulte:
    https://www.aneel.gov.br/bandeiras-tarifarias

    Valores de referência (atualizados em 2024):
    - Verde: R$ 0,00/kWh
    - Amarela: R$ 0,01885/kWh
    - Vermelha Patamar 1: R$ 0,04463/kWh
    - Vermelha Patamar 2: R$ 0,07877/kWh
    """

    print("=" * 60)
    print("ATUALIZAÇÃO DA BANDEIRA TARIFÁRIA")
    print("=" * 60)
    print("\nConsulte a bandeira vigente em:")
    print("https://www.aneel.gov.br/bandeiras-tarifarias")
    print("\nBandeiras disponíveis:")
    print("1 - Verde (R$ 0,00/kWh)")
    print("2 - Amarela (R$ 0,01885/kWh)")
    print("3 - Vermelha Patamar 1 (R$ 0,04463/kWh)")
    print("4 - Vermelha Patamar 2 (R$ 0,07877/kWh)")

    opcao = input("\nEscolha a bandeira vigente (1-4): ").strip()

    bandeiras = {
        "1": {"nome": "Verde", "valor": 0.0},
        "2": {"nome": "Amarela", "valor": 0.01885},
        "3": {"nome": "Vermelha Patamar 1", "valor": 0.04463},
        "4": {"nome": "Vermelha Patamar 2", "valor": 0.07877}
    }

    if opcao not in bandeiras:
        print("Opção inválida!")
        return False

    bandeira_escolhida = bandeiras[opcao]
    mes_atual = datetime.now().strftime("%B de %Y")

    bandeira_data = {
        "mes_referencia": mes_atual,
        "bandeira_atual": bandeira_escolhida["nome"],
        "valor_kwh": bandeira_escolhida["valor"],
        "descricao": "Condições de geração atualizadas",
        "bandeiras_disponiveis": {
            "verde": {
                "nome": "Verde",
                "valor_kwh": 0.0,
                "descricao": "Condições favoráveis de geração"
            },
            "amarela": {
                "nome": "Amarela",
                "valor_kwh": 0.01885,
                "descricao": "Condições de geração menos favoráveis"
            },
            "vermelha_1": {
                "nome": "Vermelha Patamar 1",
                "valor_kwh": 0.04463,
                "descricao": "Condições mais custosas de geração"
            },
            "vermelha_2": {
                "nome": "Vermelha Patamar 2",
                "valor_kwh": 0.07877,
                "descricao": "Condições ainda mais custosas de geração"
            }
        }
    }

    # Salvar arquivo
    filepath = os.path.join(DATA_DIR, 'bandeira.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(bandeira_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Bandeira atualizada para: {bandeira_escolhida['nome']}")
    print(f"   Valor: R$ {bandeira_escolhida['valor']:.5f}/kWh")
    print(f"   Mês: {mes_atual}")
    return True

def fetch_aneel_tarifas():
    """
    Tenta buscar tarifas do portal de dados abertos da ANEEL.

    NOTA: A API da ANEEL pode não estar sempre disponível ou pode
    requerer autenticação. Este é um exemplo de como seria a integração.

    Alternativa: Download manual do arquivo CSV de:
    https://dadosabertos.aneel.gov.br/organization/agencia-nacional-de-energia-eletrica-aneel
    """

    print("\n" + "=" * 60)
    print("ATUALIZAÇÃO DE TARIFAS")
    print("=" * 60)
    print("\n⚠️ IMPORTANTE:")
    print("A atualização automática de tarifas requer dados da ANEEL.")
    print("\nOpções:")
    print("1. Acesse: https://dadosabertos.aneel.gov.br/")
    print("2. Procure por 'Tarifas de Energia Elétrica'")
    print("3. Baixe o CSV mais recente")
    print("4. Use o script parse_aneel_csv.py para processar")
    print("\nOu entre em contato com a ANEEL para acesso à API.")

    return False

def update_tarifas_manual():
    """
    Permite atualização manual de uma tarifa específica.
    """
    print("\n" + "=" * 60)
    print("ATUALIZAÇÃO MANUAL DE TARIFA")
    print("=" * 60)

    # Carregar tarifas atuais
    filepath = os.path.join(DATA_DIR, 'tarifas.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("\nEstados disponíveis:")
    for i, tarifa in enumerate(data['tarifas'], 1):
        print(f"{i}. {tarifa['estado']} - {tarifa['distribuidora']} - R$ {tarifa['tarifa']:.5f}/kWh")

    try:
        escolha = int(input("\nEscolha o número do estado para atualizar (0 para cancelar): "))
        if escolha == 0:
            return False

        if escolha < 1 or escolha > len(data['tarifas']):
            print("Opção inválida!")
            return False

        tarifa = data['tarifas'][escolha - 1]
        print(f"\nAtualizando: {tarifa['estado']} - {tarifa['distribuidora']}")
        print(f"Tarifa atual: R$ {tarifa['tarifa']:.5f}/kWh")

        nova_tarifa = float(input("Nova tarifa (R$/kWh): "))
        tarifa['tarifa'] = nova_tarifa

        # Atualizar data
        data['ultima_atualizacao'] = datetime.now().strftime("%B de %Y")

        # Salvar
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Tarifa atualizada com sucesso!")
        print(f"   {tarifa['estado']} - Nova tarifa: R$ {nova_tarifa:.5f}/kWh")
        return True

    except ValueError:
        print("Valor inválido!")
        return False


def main():
    print("\n🔌 SISTEMA DE ATUALIZAÇÃO DE DADOS - CALCULADORA DE ENERGIA\n")

    while True:
        print("\n" + "=" * 60)
        print("MENU PRINCIPAL")
        print("=" * 60)
        print("1. Atualizar Bandeira Tarifária")
        print("2. Atualizar Tarifa de um Estado")
        print("3. Informações sobre Dados Abertos da ANEEL")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            update_bandeira_manual()
        elif opcao == "2":
            update_tarifas_manual()
        elif opcao == "3":
            fetch_aneel_tarifas()
        elif opcao == "0":
            print("\n👋 Até logo!")
            break
        else:
            print("\n❌ Opção inválida!")

if __name__ == "__main__":
    main()
