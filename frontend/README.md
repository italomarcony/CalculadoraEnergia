# Frontend - Calculadora de Energia

Interface React para a calculadora de conta de energia.

## Instalação

```bash
npm install
```

## Execução

```bash
npm run dev
```

O app estará disponível em `http://localhost:3000`

## Build para Produção

```bash
npm run build
```

Os arquivos otimizados estarão na pasta `dist/`

## Componentes

### EnergyCalculator
Componente principal que:
- Recebe CEP e consumo do usuário
- Valida e formata entrada
- Faz requisição para o backend
- Exibe resultados formatados

## Estilização

O projeto usa Tailwind CSS para estilização. Configurações em:
- `tailwind.config.js`
- `postcss.config.js`
- `src/index.css`
