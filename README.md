# TenisMatchAPI

## 📋 Sobre o Projeto

TenisMatchAPI é uma aplicação full-stack que utiliza Machine Learning para realizar matching de tênis com base em diferentes características como estilo, marca, cores e preço. O sistema oferece uma API REST completa e um dashboard interativo para visualização de métricas e gerenciamento de dados.

## 🚀 Tecnologias Utilizadas

### Backend
- Python 3.8+
- FastAPI
- SQLAlchemy
- Scikit-learn
- Pandas
- NumPy
- SQLite
- Swagger UI (OpenAPI)

### Frontend
- React
- TypeScript
- Tailwind CSS
- Recharts
- Radix UI Components
- Vite

## 🛠️ Configuração do Ambiente

### Pré-requisitos
- Python 3.8 ou superior
- Node.js 16 ou superior
- npm ou yarn
- Git

### Backend

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/tenismatch.git
cd tenismatch
```

2. Crie e ative o ambiente virtual:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
cd backend
pip install -r requirements.txt
```

### Frontend

1. Instale as dependências:
```bash
cd frontend
npm install
```

2. Configure o Tailwind:
```bash
npx tailwindcss init -p
```

## 🚦 Executando o Projeto

### Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
O servidor estará disponível em: http://localhost:8000

### Documentação da API
A documentação interativa da API está disponível em:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

A documentação inclui:
- Descrição detalhada de todos os endpoints
- Schemas com exemplos
- Interface interativa para testes
- Modelos de requisição e resposta

### Frontend
```bash
cd frontend
npm run dev
```
A aplicação estará disponível em: http://localhost:5173

## 📁 Estrutura do Projeto

```
tenismatch/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas/
│   │   │   └── tennis.py
│   │   ├── api/
│   │   │   └── routes.py
│   │   └── ml/
│   │       ├── dataset.py
│   │       └── training.py
│   ├── tests/
│   ├── venv/
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   └── utils/
    ├── public/
    └── package.json
```

## 🔍 Funcionalidades Principais

1. **Gerenciamento de Dados**
   - Upload/Download de datasets CSV
   - Validação automática de dados
   - Pré-processamento de features

2. **Machine Learning**
   - Treinamento automatizado de modelos
   - Otimização de hiperparâmetros
   - Avaliação de performance

3. **Dashboard**
   - Visualização de métricas em tempo real
   - Gráficos interativos de performance
   - Análise de distribuição de dados

4. **API REST**
   - Endpoints para CRUD completo
   - Documentação interativa com Swagger UI e ReDoc
   - Sistema de validação robusto
   - Exemplos e schemas detalhados
   - Interface de teste integrada

## 📊 Modelo de Machine Learning

O sistema utiliza um RandomForestClassifier com as seguintes características:

- Features principais:
  - Estilo do tênis (ESP, CAS, VIN, SOC, FAS)
  - Marca (Nike, Adidas, Vans, Converse, New Balance)
  - Cores (BLK, WHT, COL, NEU)
  - Preço

- Métricas monitoradas:
  - Acurácia
  - Precisão
  - Recall
  - Matriz de Confusão

## 🧪 Testes

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## 📈 Monitoramento

O sistema inclui monitoramento de:
- Performance do modelo
- Tempos de resposta da API
- Uso de recursos
- Logs estruturados

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Backend
DATABASE_URL=sqlite:///./sql_app.db
MODEL_PATH=./models/tenis_match_model.joblib
LOG_LEVEL=INFO

# Frontend
VITE_API_URL=http://localhost:8000
```

🔑 Usuários Padrão
O sistema vem com dois usuários pré-configurados para testes:

Administrador

Email: admin@tenismatch.com
Senha: abc123
Acesso total ao sistema


Testador

Email: tester@tenismatch.com
Senha: abc123
Acesso limitado para testes



📊 Sistema de Logging

Implementado com Loguru
Logs salvos em: ./logs/api.log
Rotação automática: 500MB
Retenção: 10 dias
Compressão em zip
Debug em desenvolvimento, Info em produção

Adicionar na seção "Instalando as dependências":
bashCopypip install loguru  # Necessário para o sistema de logging
pip install -r requirements.txt
Atualizar a seção "Testes" para:
🧪 Testes
Backend
O sistema inclui testes automatizados completos:
bashCopy# Testes unitários
pytest

# Testes de endpoint
python test_endpoints.py
Para mais detalhes sobre os testes de endpoint, consulte:

Guia_Swagger.md: Tutorial interativo da API
Guia_Testes_Endpoint.md: Documentação dos testes automatizados



## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

- Abra uma issue
- Envie um email para support@tenismatch.com
- Consulte a documentação completa em: https://docs.tenismatch.com
- Explore a documentação da API em: http://localhost:8000/docs

## 🔄 Próximos Passos

- [ ] Implementação de autenticação JWT
- [ ] Integração com CI/CD
- [ ] Cache com Redis
- [ ] Containerização com Docker
- [ ] Deploy automático
- [ ] Testes E2E