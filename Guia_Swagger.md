# Guia de Teste da API TenisMatch via Swagger UI

Este guia explica como testar todos os endpoints da API usando a interface Swagger UI.

## Acessando a Documentação

1. Inicie o servidor: `uvicorn app.main:app --reload`
2. Acesse: http://localhost:8000/docs

## Sequência de Testes

### 1. Autenticação

#### 1.1 Obter Token de Acesso
1. Expanda o endpoint `/api/v1/auth/token`
2. Clique em "Try it out"
3. Preencha os campos:
   ```
   username: admin@tenismatch.com
   password: abc123
   ```
4. Clique em "Execute"
5. Copie o `access_token` da resposta

#### 1.2 Autorizar Swagger
1. Clique no botão "Authorize" no topo da página
2. No campo "bearerAuth", digite: `Bearer {seu-token}`
3. Clique em "Authorize"

### 2. Template CSV

1. Expanda o endpoint `/api/v1/tennis/template-csv`
2. Clique em "Try it out"
3. Execute e salve o CSV retornado

### 3. Upload de Dados

1. Expanda o endpoint `/api/v1/tennis/upload-csv`
2. Clique em "Try it out"
3. Selecione o arquivo CSV baixado no passo anterior
4. Execute e verifique a resposta

### 4. Treinamento do Modelo

1. Expanda o endpoint `/api/v1/tennis/train`
2. Clique em "Try it out"
3. Execute e observe as métricas retornadas

### 5. Predições

1. Expanda o endpoint `/api/v1/tennis/predict`
2. Clique em "Try it out"
3. Insira um payload de exemplo:
   ```json
   {
     "records": [
       {
         "tenis_estilo": "ESP",
         "tenis_marca": "Nike",
         "tenis_cores": "BLK",
         "tenis_preco": 299.99,
         "match_success": 1
       }
     ]
   }
   ```
4. Execute e observe as predições

### 6. Outros Endpoints

#### 6.1 Exportar CSV
1. Expanda `/api/v1/tennis/export-csv`
2. Execute para baixar todos os dados

#### 6.2 Métricas do Modelo
1. Expanda `/api/v1/tennis/metrics`
2. Execute para ver o histórico de treinamentos

## Notas Importantes

1. **Autenticação**: 
   - Alguns endpoints são protegidos e requerem token
   - O token expira após 30 minutos
   - Você pode usar tanto o usuário admin quanto o tester

2. **Ordem dos Testes**:
   - Siga a ordem sugerida acima
   - O treinamento requer ao menos 100 registros no banco
   - As predições requerem um modelo treinado

3. **Códigos de Erro Comuns**:
   - 401: Token inválido ou expirado
   - 400: Dados inválidos
   - 422: Erro de validação dos dados
   - 500: Erro interno do servidor

4. **Dicas**:
   - Mantenha o token atualizado
   - Verifique o formato correto dos dados
   - Observe as respostas de erro para debugar problemas