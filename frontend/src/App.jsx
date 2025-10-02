import EnergyCalculator from './components/EnergyCalculator'
import Footer from './components/Footer'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      <div className="flex-grow">
        <div className="container mx-auto px-4 py-8">
          <header className="text-center mb-8">
            <div className="flex items-center justify-center gap-3 mb-2">
              <svg
                className="w-12 h-12 text-yellow-500"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" />
              </svg>
              <h1 className="text-4xl font-bold text-gray-800">
                Calculadora de Conta de Energia
              </h1>
            </div>
            <p className="text-gray-600">
              Calcule o valor estimado da sua conta de energia elétrica
            </p>
          </header>
          <EnergyCalculator />
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default App
