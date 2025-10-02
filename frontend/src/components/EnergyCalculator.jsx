import { useState } from 'react'
import axios from 'axios'

const EnergyCalculator = () => {
  const [cep, setCep] = useState('')
  const [consumo, setConsumo] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const formatCep = (value) => {
    const numbers = value.replace(/\D/g, '')
    if (numbers.length <= 5) {
      return numbers
    }
    return `${numbers.slice(0, 5)}-${numbers.slice(5, 8)}`
  }

  const handleCepChange = (e) => {
    const formatted = formatCep(e.target.value)
    setCep(formatted)
  }

  const handleCalculate = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post('/api/calculate', {
        cep: cep.replace('-', ''),
        consumo: parseFloat(consumo)
      })

      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'Erro ao calcular. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

  const getBandeiraColor = (bandeira) => {
    if (bandeira.includes('Verde')) return 'bg-green-100 text-green-800'
    if (bandeira.includes('Amarela')) return 'bg-yellow-100 text-yellow-800'
    if (bandeira.includes('Vermelha')) return 'bg-red-100 text-red-800'
    return 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <form onSubmit={handleCalculate} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="cep" className="block text-sm font-medium text-gray-700 mb-2">
                CEP
              </label>
              <input
                type="text"
                id="cep"
                value={cep}
                onChange={handleCepChange}
                placeholder="00000-000"
                maxLength="9"
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
              />
            </div>

            <div>
              <label htmlFor="consumo" className="block text-sm font-medium text-gray-700 mb-2">
                Consumo (kWh)
              </label>
              <input
                type="number"
                id="consumo"
                value={consumo}
                onChange={(e) => setConsumo(e.target.value)}
                placeholder="150"
                min="0"
                step="0.01"
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Calculando...' : 'Calcular'}
          </button>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        )}

        {result && (
          <div className="mt-8 space-y-6">
            <div className="border-t pt-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Resultado</h2>

              <div className="grid md:grid-cols-2 gap-4 mb-6">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Distribuidora</p>
                  <p className="text-lg font-semibold text-gray-800">{result.distribuidora}</p>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Estado</p>
                  <p className="text-lg font-semibold text-gray-800">{result.estado}</p>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Tarifa (R$/kWh)</p>
                  <p className="text-lg font-semibold text-gray-800">
                    {formatCurrency(result.tarifa)}
                  </p>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Bandeira Tarifária</p>
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getBandeiraColor(result.bandeira)}`}>
                    {result.bandeira}
                  </span>
                </div>
              </div>

              <div className="bg-primary-50 border-2 border-primary-200 p-6 rounded-lg mb-6">
                <div className="flex justify-between items-center mb-2">
                  <p className="text-gray-700">Valor da Energia</p>
                  <p className="text-lg font-semibold text-gray-800">
                    {formatCurrency(result.valor_total - result.valor_bandeira)}
                  </p>
                </div>
                <div className="flex justify-between items-center mb-2">
                  <p className="text-gray-700">Valor da Bandeira</p>
                  <p className="text-lg font-semibold text-gray-800">
                    {formatCurrency(result.valor_bandeira)}
                  </p>
                </div>
                <div className="border-t border-primary-300 mt-3 pt-3 flex justify-between items-center">
                  <p className="text-xl font-bold text-gray-800">Valor Total Estimado</p>
                  <p className="text-3xl font-bold text-primary-700">
                    {formatCurrency(result.valor_total)}
                  </p>
                </div>
              </div>

              {result.comparacao && (
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold text-gray-800 mb-4">Comparação Nacional</h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="border-l-4 border-green-500 pl-4">
                      <p className="text-sm text-gray-600 mb-1">Estado Mais Barato</p>
                      <p className="font-semibold text-gray-800">{result.comparacao.mais_barato.estado}</p>
                      <p className="text-sm text-gray-600">{formatCurrency(result.comparacao.mais_barato.tarifa)}/kWh</p>
                    </div>
                    <div className="border-l-4 border-red-500 pl-4">
                      <p className="text-sm text-gray-600 mb-1">Estado Mais Caro</p>
                      <p className="font-semibold text-gray-800">{result.comparacao.mais_caro.estado}</p>
                      <p className="text-sm text-gray-600">{formatCurrency(result.comparacao.mais_caro.tarifa)}/kWh</p>
                    </div>
                  </div>
                </div>
              )}

              <p className="text-xs text-gray-500 mt-4 text-center">
                Última atualização dos dados: {result.ultima_atualizacao_dados}
              </p>
            </div>
          </div>
        )}
      </div>

      <div className="mt-8 bg-amber-50 border border-amber-300 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-amber-900 mb-3">⚠️ Informações Importantes</h3>
        <ul className="space-y-2 text-sm text-gray-700">
          <li className="flex items-start">
            <span className="font-semibold text-amber-800 mr-2">•</span>
            <span><strong>Dados oficiais:</strong> Tarifas obtidas da API de Dados Abertos da ANEEL (tarifas homologadas vigentes)</span>
          </li>
          <li className="flex items-start">
            <span className="font-semibold text-amber-800 mr-2">•</span>
            <span><strong>Impostos NÃO inclusos:</strong> O cálculo NÃO inclui ICMS (18-33%), PIS/COFINS (~3-4%), que são adicionados pela distribuidora</span>
          </li>
          <li className="flex items-start">
            <span className="font-semibold text-amber-800 mr-2">•</span>
            <span><strong>Taxas não inclusas:</strong> Iluminação pública, bandeiras de escassez hídrica, multas ou encargos adicionais</span>
          </li>
          <li className="flex items-start">
            <span className="font-semibold text-amber-800 mr-2">•</span>
            <span><strong>Bandeira tarifária:</strong> Valor adicional mensal definido pela ANEEL conforme condições de geração</span>
          </li>
        </ul>
      </div>

      <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-xs text-blue-800 text-center">
          💡 <strong>Dica:</strong> O valor final na sua conta pode ser até 30-40% maior devido aos impostos estaduais e federais
        </p>
      </div>
    </div>
  )
}

export default EnergyCalculator
