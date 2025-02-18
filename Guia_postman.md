# Guia de Uso do Postman - TenisMatch API

## 📥 Instalação do Postman

### Download
1. Acesse: https://www.postman.com/downloads/
2. Escolha a versão adequada para seu sistema operacional:
   - Windows: Baixe e execute o instalador (.exe)
   - Mac: Baixe o arquivo .dmg
   - Linux: Baixe o arquivo .tar.gz

### Instalação
#### Windows
1. Execute o arquivo baixado
2. Siga o assistente de instalação
3. Aguarde a conclusão

#### Mac
1. Abra o arquivo .dmg baixado
2. Arraste o Postman para a pasta Applications
3. Execute pela primeira vez (pode exigir aprovação de segurança)

#### Linux
1. Extraia o arquivo .tar.gz
2. Execute o Postman a partir da pasta extraída

### Primeiro Acesso
1. Inicie o Postman
2. Opções de início:
   - Criar conta gratuita (recomendado para sincronização)
   - Pular login (Skip and take me to Postman)

## 🛠️ Configuração Inicial

### Criar Collection
1. Clique em "+" (New) no topo
2. Selecione "Collection"
3. Configure:
   - Nome: TenisMatch API
   - Descrição: API para matching de tênis
4. Clique em "Create"

### Variáveis de Ambiente
1. Clique em "Environments" no menu lateral
2. Clique em "+" (New Environment)
3. Configure:
   - Nome: TenisMatch Local
   - Variáveis:
     - baseUrl: http://localhost:8000
     - token: [deixe vazio por enquanto]
4. Salve a configuração

### Importar Collection
Caso tenha recebido um arquivo de collection:
1. Clique em "Import" no topo
2. Arraste o arquivo ou clique para selecionar
3. Confirme a importação


# Guia de Endpoints - TenisMatch API

## 🔑 Autenticação

### Obter Token
1. Crie nova requisição:
   - Método: POST
   - URL: {{baseUrl}}/api/v1/auth/token
   - Descrição: Obter token de acesso

2. Configure o Body:
   - Tipo: x-www-form-urlencoded
   - Campos:
     ```
     username: admin@tenismatch.com
     password: abc123
     ```

3. Envie a requisição
   - Copie o "access_token" da resposta
   - Salve nas variáveis de ambiente:
     - Vá em "Environments"
     - Cole o token na variável "token"

### Verificar Autenticação
1. Crie nova requisição:
   - Método: GET
   - URL: {{baseUrl}}/api/v1/auth/me
   
2. Configure Headers:
   ```
   Authorization: Bearer {{token}}
   ```

## 📁 Operações com Arquivos

### Download Template CSV
1. Nova requisição:
   - Método: GET
   - URL: {{baseUrl}}/api/v1/tennis/template-csv
   - Sem autenticação necessária

2. Salve a resposta:
   - Clique em "Save Response"
   - "Save as file"
   - Use para testes de upload

### Upload CSV
1. Nova requisição:
   - Método: POST
   - URL: {{baseUrl}}/api/v1/tennis/upload-csv

2. Headers:
   ```
   Authorization: Bearer {{token}}
   ```

3. Body:
   - Tipo: form-data
   - Campos:
     - Key: file (selecione tipo File)
     - Value: selecione seu arquivo CSV

### Dicas para Upload
- Não defina Content-Type manualmente
- Certifique-se que o arquivo está no formato correto
- Verifique se o token está atualizado

# Guia de Testes - TenisMatch API

## 🧪 Testando Endpoints

### Treinamento do Modelo
1. Nova requisição:
   - Método: POST
   - URL: {{baseUrl}}/api/v1/tennis/train
   
2. Headers:
   ```
   Authorization: Bearer {{token}}
   ```

### Predições
1. Nova requisição:
   - Método: POST
   - URL: {{baseUrl}}/api/v1/tennis/predict

2. Headers:
   ```
   Authorization: Bearer {{token}}
   Content-Type: application/json
   ```

3. Body (raw JSON):
   ```json
   {
     "records": [
       {
         "tenis_estilo": "ESP",
         "tenis_marca": "Nike",
         "tenis_cores": "BLK",
         "tenis_preco": 299.99,
         "match_success": 0
       }
     ]
   }
   ```

## 🔍 Troubleshooting

### Erros Comuns

1. **Token Inválido (401)**
   - Gere um novo token
   - Verifique se copiou o token completo
   - Confirme o formato "Bearer [token]"

2. **Erro no Upload (422)**
   - Verifique o formato do arquivo
   - Confirme se selecionou tipo "File"
   - Não defina Content-Type manualmente

3. **Erro nas Predições (500)**
   - Verifique o formato do JSON
   - Confirme se o modelo foi treinado
   - Valide os valores das features

### Dicas Gerais
1. Use o ambiente (Environment) para variáveis
2. Mantenha o token atualizado
3. Verifique os logs do servidor
4. Teste primeiro no /auth/me
5. Use a collection para organizar requisições

## 📋 Checklist de Testes

1. [ ] Autenticação funcionando
2. [ ] Download do template ok
3. [ ] Upload de arquivo ok
4. [ ] Treinamento concluído
5. [ ] Predições funcionando

## 🔄 Fluxo de Teste Completo

1. Gerar token
2. Verificar autenticação
3. Baixar template
4. Fazer upload
5. Treinar modelo
6. Testar predições