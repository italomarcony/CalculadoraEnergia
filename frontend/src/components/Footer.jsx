function Footer() {
  return (
    <footer className="mt-16 bg-gradient-to-r from-gray-800 to-gray-900 text-white py-8">
      <div className="container mx-auto px-4">
        {/* Tecnologias */}
        <div className="mb-6">
          <h3 className="text-center text-sm font-semibold mb-4 text-gray-300">
            Tecnologias Utilizadas
          </h3>
          <div className="flex flex-wrap justify-center items-center gap-6">
            {/* React */}
            <a
              href="https://reactjs.org/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:scale-110 transition-transform"
              title="React"
            >
              <img
                src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"
                alt="React"
              />
            </a>

            {/* Vite */}
            <a
              href="https://vitejs.dev/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:scale-110 transition-transform"
              title="Vite"
            >
              <img
                src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white"
                alt="Vite"
              />
            </a>

            {/* Tailwind CSS */}
            <a
              href="https://tailwindcss.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:scale-110 transition-transform"
              title="Tailwind CSS"
            >
              <img
                src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white"
                alt="Tailwind CSS"
              />
            </a>

            {/* Python */}
            <a
              href="https://www.python.org/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:scale-110 transition-transform"
              title="Python"
            >
              <img
                src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"
                alt="Python"
              />
            </a>

            {/* Flask */}
            <a
              href="https://flask.palletsprojects.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:scale-110 transition-transform"
              title="Flask"
            >
              <img
                src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"
                alt="Flask"
              />
            </a>

            {/* API ANEEL */}
            <a
              href="https://dadosabertos.aneel.gov.br/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:scale-110 transition-transform"
              title="API ANEEL"
            >
              <img
                src="https://img.shields.io/badge/API_ANEEL-0066CC?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0wIDE4Yy00LjQxIDAtOC0zLjU5LTgtOHMzLjU5LTggOC04IDggMy41OSA4IDgtMy41OSA4LTggOHoiLz48L3N2Zz4=&logoColor=white"
                alt="API ANEEL"
              />
            </a>

            {/* ViaCEP */}
            <a
              href="https://viacep.com.br/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:scale-110 transition-transform"
              title="ViaCEP"
            >
              <img
                src="https://img.shields.io/badge/ViaCEP-FF6B6B?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzguMTMgMiA1IDUuMTMgNSA5YzAgNS4yNSA3IDEzIDcgMTNzNy03Ljc1IDctMTNjMC0zLjg3LTMuMTMtNy03LTd6bTAgOS41Yy0xLjM4IDAtMi41LTEuMTItMi41LTIuNXMxLjEyLTIuNSAyLjUtMi41IDIuNSAxLjEyIDIuNSAyLjUtMS4xMiAyLjUtMi41IDIuNXoiLz48L3N2Zz4=&logoColor=white"
                alt="ViaCEP"
              />
            </a>
          </div>
        </div>

        {/* Divisor */}
        <div className="border-t border-gray-700 my-6"></div>

        {/* Informações do Desenvolvedor */}
        <div className="text-center">
          <p className="text-lg font-semibold mb-3">Desenvolvedor</p>
          <p className="text-xl font-bold mb-4">Ítalo Marcony</p>

          <div className="flex justify-center gap-4 mb-4">
            {/* LinkedIn */}
            <a
              href="https://www.linkedin.com/in/italomarcony6532/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:scale-110 transition-transform"
              title="LinkedIn"
            >
              <img
                src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"
                alt="LinkedIn"
              />
            </a>

            {/* GitHub */}
            <a
              href="https://github.com/italomarcony"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:scale-110 transition-transform"
              title="GitHub"
            >
              <img
                src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"
                alt="GitHub"
              />
            </a>

            {/* Repositório */}
            <a
              href="https://github.com/italomarcony/CalculadoraEnergia"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:scale-110 transition-transform"
              title="Repositório"
            >
              <img
                src="https://img.shields.io/badge/Repositório-CalculadoraEnergia-blue?style=for-the-badge&logo=github"
                alt="Repositório"
              />
            </a>
          </div>

          <p className="text-sm text-gray-400">
            Feito com ❤️ e ☕ por Ítalo Marcony
          </p>

          <p className="text-xs text-gray-500 mt-3">
            Dados oficiais da{' '}
            <a
              href="https://dadosabertos.aneel.gov.br/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 underline"
            >
              API de Dados Abertos da ANEEL
            </a>
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
