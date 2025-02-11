@echo off
echo Criando estrutura do projeto TenisMatchAPI...

:: Criar estrutura de diretórios
mkdir backend
mkdir backend\app
mkdir backend\app\api
mkdir backend\app\core
mkdir backend\app\database
mkdir backend\app\models
mkdir backend\app\ml
mkdir backend\app\schemas
mkdir backend\tests
mkdir frontend
mkdir frontend\src
mkdir frontend\src\components
mkdir frontend\src\pages
mkdir frontend\src\services
mkdir frontend\public
mkdir data

:: Criar arquivos do backend
echo # /backend/requirements.txt > backend\requirements.txt
echo # /backend/app/main.py > backend\app\main.py
echo # /backend/app/api/routes.py > backend\app\api\routes.py
echo # /backend/app/core/config.py > backend\app\core\config.py
echo # /backend/app/database/session.py > backend\app\database\session.py
echo # /backend/app/database/models.py > backend\app\database\models.py
echo # /backend/app/ml/dataset.py > backend\app\ml\dataset.py
echo # /backend/app/ml/training.py > backend\app\ml\training.py
echo # /backend/app/schemas/tennis.py > backend\app\schemas\tennis.py
echo # /backend/tests/test_api.py > backend\tests\test_api.py
echo # /backend/tests/test_ml.py > backend\tests\test_ml.py

:: Criar arquivos do frontend
echo # /frontend/package.json > frontend\package.json
echo # /frontend/src/App.jsx > frontend\src\App.jsx
echo # /frontend/src/main.jsx > frontend\src\main.jsx
echo # /frontend/src/components/MLDashboard.jsx > frontend\src\components\MLDashboard.jsx
echo # /frontend/src/pages/Home.jsx > frontend\src\pages\Home.jsx
echo # /frontend/src/services/api.js > frontend\src\services\api.js
echo # /frontend/index.html > frontend\index.html

:: Criar arquivos de configuração do projeto
echo # /.gitignore > .gitignore
echo node_modules/ > .gitignore
echo __pycache__/ >> .gitignore
echo .env >> .gitignore
echo .venv >> .gitignore
echo *.pyc >> .gitignore
echo *.pyo >> .gitignore
echo *.pyd >> .gitignore
echo .Python >> .gitignore
echo build/ >> .gitignore
echo develop-eggs/ >> .gitignore
echo dist/ >> .gitignore
echo downloads/ >> .gitignore
echo eggs/ >> .gitignore
echo .eggs/ >> .gitignore
echo lib/ >> .gitignore
echo lib64/ >> .gitignore
echo parts/ >> .gitignore
echo sdist/ >> .gitignore
echo var/ >> .gitignore
echo *.egg-info/ >> .gitignore
echo .installed.cfg >> .gitignore
echo *.egg >> .gitignore
echo *.sqlite >> .gitignore
echo .env.local >> .gitignore
echo .env.development.local >> .gitignore
echo .env.test.local >> .gitignore
echo .env.production.local >> .gitignore
echo npm-debug.log* >> .gitignore
echo yarn-debug.log* >> .gitignore
echo yarn-error.log* >> .gitignore

:: Criar README.md
echo # TenisMatch API > README.md
echo. >> README.md
echo ## Descrição >> README.md
echo Aplicação web para análise de compatibilidade de tênis usando Machine Learning. >> README.md
echo. >> README.md
echo ## Estrutura do Projeto >> README.md
echo ```text >> README.md
echo TenisMatchAPI/ >> README.md
echo ├── backend/           # API FastAPI >> README.md
echo ├── frontend/          # Interface React >> README.md
echo └── data/             # Dados e modelos >> README.md
echo ``` >> README.md
echo. >> README.md
echo ## Instalação >> README.md
echo 1. Clone o repositório >> README.md
echo 2. Instale as dependências do backend: `pip install -r backend/requirements.txt` >> README.md
echo 3. Instale as dependências do frontend: `cd frontend && npm install` >> README.md
echo. >> README.md
echo ## Executando o Projeto >> README.md
echo 1. Inicie o backend: `cd backend && uvicorn app.main:app --reload` >> README.md
echo 2. Inicie o frontend: `cd frontend && npm run dev` >> README.md

:: Criar arquivo de ambiente exemplo
echo # Backend >> .env.example
echo DATABASE_URL=sqlite:///./tennis_match.db >> .env.example
echo API_PORT=8000 >> .env.example
echo DEBUG=True >> .env.example
echo. >> .env.example
echo # Frontend >> .env.example
echo VITE_API_URL=http://localhost:8000 >> .env.example

:: Criar requirements.txt inicial
type nul > backend\requirements.txt
echo fastapi==0.104.1 > backend\requirements.txt
echo uvicorn==0.24.0 >> backend\requirements.txt
echo pandas==2.1.3 >> backend\requirements.txt
echo numpy==1.26.2 >> backend\requirements.txt
echo scikit-learn==1.3.2 >> backend\requirements.txt
echo python-multipart==0.0.6 >> backend\requirements.txt
echo joblib==1.3.2 >> backend\requirements.txt
echo pydantic==2.5.2 >> backend\requirements.txt
echo sqlalchemy==2.0.23 >> backend\requirements.txt
echo pytest==7.4.3 >> backend\requirements.txt

:: Criar package.json inicial
echo { > frontend\package.json
echo   "name": "tenis-match-frontend", >> frontend\package.json
echo   "private": true, >> frontend\package.json
echo   "version": "0.1.0", >> frontend\package.json
echo   "type": "module", >> frontend\package.json
echo   "scripts": { >> frontend\package.json
echo     "dev": "vite", >> frontend\package.json
echo     "build": "vite build", >> frontend\package.json
echo     "preview": "vite preview" >> frontend\package.json
echo   }, >> frontend\package.json
echo   "dependencies": { >> frontend\package.json
echo     "react": "^18.2.0", >> frontend\package.json
echo     "react-dom": "^18.2.0", >> frontend\package.json
echo     "recharts": "^2.10.1", >> frontend\package.json
echo     "axios": "^1.6.2", >> frontend\package.json
echo     "papaparse": "^5.4.1" >> frontend\package.json
echo   }, >> frontend\package.json
echo   "devDependencies": { >> frontend\package.json
echo     "@types/react": "^18.2.37", >> frontend\package.json
echo     "@types/react-dom": "^18.2.15", >> frontend\package.json
echo     "@vitejs/plugin-react": "^4.2.0", >> frontend\package.json
echo     "vite": "^5.0.0" >> frontend\package.json
echo   } >> frontend\package.json
echo } >> frontend\package.json

echo Estrutura do projeto criada com sucesso!
echo Para começar:
echo 1. Execute: python -m venv venv
echo 2. Execute: venv\Scripts\activate
echo 3. Execute: pip install -r backend\requirements.txt
echo 4. Execute: cd frontend ^& npm install