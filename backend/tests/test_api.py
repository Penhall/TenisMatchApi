# /backend/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
import pandas as pd
import io
from app.main import app
from app.database.session import get_db, Base, engine
from app.ml.dataset import DatasetPreparation

# Setup test client
client = TestClient(app)

# Fixture para banco de dados de teste
@pytest.fixture(autouse=True)
def test_db():
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    yield
    # Limpar tabelas após cada teste
    Base.metadata.drop_all(bind=engine)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_upload_csv():
    # Criar dados sintéticos
    data = DatasetPreparation.generate_synthetic_data(100)
    df = pd.DataFrame(data)
    
    # Converter para CSV
    csv_file = io.StringIO()
    df.to_csv(csv_file, index=False)
    csv_file.seek(0)
    
    # Fazer upload
    files = {"file": ("test.csv", csv_file, "text/csv")}
    response = client.post("/api/v1/upload-csv", files=files)
    
    assert response.status_code == 200
    assert "message" in response.json()

def test_export_csv():
    # Primeiro fazer upload de alguns dados
    data = DatasetPreparation.generate_synthetic_data(100)
    df = pd.DataFrame(data)
    csv_file = io.StringIO()
    df.to_csv(csv_file, index=False)
    csv_file.seek(0)
    files = {"file": ("test.csv", csv_file, "text/csv")}
    client.post("/api/v1/upload-csv", files=files)
    
    # Testar exportação
    response = client.get("/api/v1/export-csv")
    assert response.status_code == 200
    
    # Verificar se o CSV exportado é válido
    exported_df = pd.read_csv(io.StringIO(response.text))
    assert len(exported_df) == 100
    assert all(col in exported_df.columns for col in df.columns)

def test_train_model():
    # Preparar dados de treinamento
    data = DatasetPreparation.generate_synthetic_data(200)
    df = pd.DataFrame(data)
    csv_file = io.StringIO()
    df.to_csv(csv_file, index=False)
    csv_file.seek(0)
    files = {"file": ("test.csv", csv_file, "text/csv")}
    client.post("/api/v1/upload-csv", files=files)
    
    # Treinar modelo
    response = client.post("/api/v1/train")
    assert response.status_code == 200
    
    metrics = response.json()
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "roc_curve_data" in metrics
    assert "confusion_matrix" in metrics

def test_predict():
    # Primeiro treinar o modelo
    data = DatasetPreparation.generate_synthetic_data(200)
    df = pd.DataFrame(data)
    csv_file = io.StringIO()
    df.to_csv(csv_file, index=False)
    csv_file.seek(0)
    files = {"file": ("test.csv", csv_file, "text/csv")}
    client.post("/api/v1/upload-csv", files=files)
    client.post("/api/v1/train")
    
    # Fazer predição
    test_data = {
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
    
    response = client.post("/api/v1/predict", json=test_data)
    assert response.status_code == 200
    
    predictions = response.json()
    assert len(predictions) == 1
    assert "match_prediction" in predictions[0]
    assert "match_probability" in predictions[0]
    assert "confidence_score" in predictions[0]

def test_get_metrics():
    # Primeiro treinar o modelo para gerar métricas
    data = DatasetPreparation.generate_synthetic_data(200)
    df = pd.DataFrame(data)
    csv_file = io.StringIO()
    df.to_csv(csv_file, index=False)
    csv_file.seek(0)
    files = {"file": ("test.csv", csv_file, "text/csv")}
    client.post("/api/v1/upload-csv", files=files)
    client.post("/api/v1/train")
    
    # Buscar métricas
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    
    metrics = response.json()
    assert len(metrics) > 0
    assert "accuracy" in metrics[0]
    assert "precision" in metrics[0]
    assert "recall" in metrics[0]
    assert "f1_score" in metrics[0]