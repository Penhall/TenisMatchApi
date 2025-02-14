# test_endpoints.py
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_root():
    """Testa o endpoint raiz"""
    response = requests.get("http://localhost:8000/")
    print("\nRoot Check:", response.json())
    assert response.status_code == 200, f"Status code: {response.status_code}"
    return True

def get_token(email: str, password: str) -> str:
    """Obtém token de autenticação"""
    print(f"\nTentando autenticar com {email}...")
    response = requests.post(
        f"{BASE_URL}/auth/token",
        data={"username": email, "password": password}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("Token obtido com sucesso!")
        print(f"Token: {token[:30]}...")  # Mostra parte do token para debug
        return token
    else:
        print(f"Erro ao obter token: {response.status_code}")
        print(response.json())
        return None

def test_auth():
    """Testa autenticação com os dois usuários padrão"""
    users = [
        {"email": "admin@tenismatch.com", "password": "abc123"},
        {"email": "tester@tenismatch.com", "password": "abc123"}
    ]
    
    tokens = []
    for user in users:
        token = get_token(user["email"], user["password"])
        assert token is not None, f"Falha ao obter token para {user['email']}"
        tokens.append(token)
        
        # Testa endpoint /me com o token
        headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }
        print(f"\nTentando acessar /me com token...")
        print(f"Headers: {headers}")
        
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        assert response.status_code == 200, f"Falha ao obter dados do usuário: {response.status_code}"
        print(f"Dados do usuário {user['email']}:", response.json())
    
    return tokens[0]  # Retorna o token do admin para outros testes

def test_template_csv(token):
    """Testa download do template CSV"""
    print("\nBaixando template CSV...")
    response = requests.get(f"{BASE_URL}/tennis/template-csv")
    assert response.status_code == 200, f"Falha ao baixar template: {response.status_code}"
    print("Template CSV obtido com sucesso")
    
    # Salva o template para usar no upload
    with open("template.csv", "w", newline='') as f:
        f.write(response.text)
    
    # Verifica as colunas
    import pandas as pd
    try:
        df = pd.read_csv("template.csv")
        print("\nColunas presentes no template:")
        print(df.columns.tolist())
        print("\nPrimeiras linhas do template:")
        print(df.head())
        return True
    except Exception as e:
        print(f"Erro ao ler CSV: {str(e)}")
        return False

def test_upload_csv(token):
    """Testa upload do CSV"""
    print("\nRealizando upload do CSV...")
    headers = {"Authorization": f"Bearer {token}"}
    
    files = {"file": ("template.csv", open("template.csv", "rb"), "text/csv")}
    response = requests.post(
        f"{BASE_URL}/tennis/upload-csv",
        headers=headers,
        files=files
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    assert response.status_code == 200, f"Falha no upload: {response.status_code}"
    print("Upload CSV:", response.json())
    return True

def test_train_model(token):
    """Testa treinamento do modelo"""
    print("\nIniciando treinamento do modelo...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(
        f"{BASE_URL}/tennis/train",
        headers=headers
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    assert response.status_code == 200, f"Falha no treinamento: {response.status_code}"
    print("Treinamento concluído:", response.json())
    return True

def test_predict(token):
    """Testa predições"""
    print("\nRealizando predições...")
    headers = {
        "Authorization": f"Bearer {token}",  # Garantindo que o token está sendo enviado
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    test_data = {
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
    
    print(f"Headers sendo enviados: {headers}")
    print(f"Dados sendo enviados: {test_data}")
    
    response = requests.post(
        f"{BASE_URL}/tennis/predict",
        headers=headers,
        json=test_data
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    assert response.status_code == 200, f"Falha nas predições: {response.status_code}"
    print("Predições:", response.json())
    return True

def main():
    """Executa todos os testes"""
    print("Iniciando testes da API...")
    time.sleep(1)
    
    try:
        # Testa endpoint raiz
        test_root()
        
        # Testa autenticação e obtém token
        admin_token = test_auth()
        
        # Se a autenticação funcionar, continua com os outros testes
        if admin_token:
            test_template_csv(admin_token)
            test_upload_csv(admin_token)
            test_train_model(admin_token)
            test_predict(admin_token)  # Passando o token obtido anteriormente
            print("\nTodos os testes completados com sucesso! ✨")
        
    except AssertionError as e:
        print("\n❌ Erro nos testes:", str(e))
    except Exception as e:
        print("\n❌ Erro inesperado:", str(e))
    finally:
        print("\nTestes concluídos.")
        

if __name__ == "__main__":
    main()