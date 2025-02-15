# /backend/app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from fastapi.responses import Response  
from datetime import datetime
import numpy as np


from app.database.session import get_db
from app.database.models import TenisData, ModelMetrics, User
from app.schemas.tennis import (
    TenisCreate, TenisResponse, ModelMetricsComplete,
    BatchPredictionRequest, PredictionResponse
)
from app.ml.dataset import DatasetPreparation
from app.ml.training import ModelTraining
from app.api.deps import get_current_user, verify_api_key

router = APIRouter(
    prefix="/tennis",
    tags=["Tênis"],
    responses={404: {"description": "Item não encontrado"}}
)

# Rota pública para baixar template
@router.get(
    "/template-csv",
    summary="Download Template CSV",
    description="Fornece um arquivo CSV modelo com o formato correto para upload",
    response_class=Response
)
async def get_template_csv():
    """Gera um template CSV com dados de exemplo"""
    # Cria dados de exemplo
    data = [
        {
            "tenis_estilo": "ESP",
            "tenis_marca": "Nike",
            "tenis_cores": "BLK",
            "tenis_preco": 299.99,
            "match_success": 1
        },
        {
            "tenis_estilo": "CAS",
            "tenis_marca": "Adidas",
            "tenis_cores": "WHT",
            "tenis_preco": 249.99,
            "match_success": 0
        },
        {
            "tenis_estilo": "VIN",
            "tenis_marca": "Vans",
            "tenis_cores": "COL",
            "tenis_preco": 199.99,
            "match_success": 1
        },
        {
            "tenis_estilo": "SOC",
            "tenis_marca": "Converse",
            "tenis_cores": "NEU",
            "tenis_preco": 179.99,
            "match_success": 0
        },
        {
            "tenis_estilo": "FAS",
            "tenis_marca": "New Balance",
            "tenis_cores": "BLK",
            "tenis_preco": 289.99,
            "match_success": 1
        }
    ]
    
    # Converte para DataFrame e depois para CSV
    df = pd.DataFrame(data)
    csv_content = df.to_csv(index=False)
    
    # Retorna como arquivo para download
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=template_tenis.csv"
        }
    )

# Rotas protegidas (requerem autenticação)
@router.post(
    "/upload-csv",
    response_model=dict,
    summary="Upload de Dataset CSV",
    description="Realiza o upload de um arquivo CSV contendo dados de tênis"
)
async def upload_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Arquivo deve ser CSV")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        required_cols = ['tenis_estilo', 'tenis_marca', 'tenis_cores', 'tenis_preco', 'match_success']
        if not all(col in df.columns for col in required_cols):
            raise HTTPException(400, "CSV não contém todas as colunas necessárias")
        
        records = []
        for _, row in df.iterrows():
            record = TenisData(
                tenis_estilo=row['tenis_estilo'],
                tenis_marca=row['tenis_marca'],
                tenis_cores=row['tenis_cores'],
                tenis_preco=row['tenis_preco'],
                match_success=row['match_success']
            )
            records.append(record)
        
        db.bulk_save_objects(records)
        db.commit()
        
        return {"message": f"Importados {len(records)} registros com sucesso"}
        
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get(
    "/export-csv",
    summary="Exportar Dataset CSV",
    description="Exporta todos os registros do banco de dados"
)
async def export_csv(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = db.query(TenisData).all()
    data = [record.to_dict() for record in records]
    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

@router.post(
    "/train",
    response_model=ModelMetricsComplete,
    summary="Treinar Modelo",
    description="Treina um novo modelo usando os dados disponíveis"
)
async def train_model(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = db.query(TenisData).all()
    if len(records) < 5:
        raise HTTPException(400, "Dados insuficientes para treinamento (mínimo 100 registros)")
    
    data = [record.to_dict() for record in records]
    prep = DatasetPreparation()
    X, y = prep.prepare_features(data)
    
    trainer = ModelTraining()
    metrics, feature_importance = trainer.train_model(X, y)
    
    trainer.save_model()
    
    # Adiciona a data de treinamento
    metrics.training_date = datetime.utcnow()
    
    # Salva métricas no banco
    db_metrics = ModelMetrics(
        accuracy=metrics.accuracy,
        precision=metrics.precision,
        recall=metrics.recall,
        f1_score=metrics.f1_score,
        training_date=metrics.training_date
    )
    db.add(db_metrics)
    db.commit()
    
    return metrics

@router.post(
    "/predict",
    response_model=List[PredictionResponse],
    summary="Realizar Predições",
    description="Realiza predições de match para uma lista de tênis"
)
async def predict(
    request: BatchPredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        prep = DatasetPreparation()
        records = request.dict()['records']
        
        # Prepara features
        features = prep.prepare_features(records)
        
        # Carrega modelo e faz predições
        trainer = ModelTraining()
        trainer.load_model()
        predictions, probabilities = trainer.predict(features)
        
        # Formata resultados
        results = []
        for i in range(len(predictions)):
            prob = probabilities[i]
            results.append(PredictionResponse(
                match_prediction=int(predictions[i]),
                match_probability=float(prob[1]),
                confidence_score=float(np.max(prob))
            ))
        
        return results
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao realizar predições: {str(e)}\n{error_details}"
        )

@router.get(
    "/metrics",
    response_model=List[ModelMetricsComplete],
    summary="Obter Métricas do Modelo",
    description="Retorna o histórico de métricas dos modelos treinados"
)
async def get_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    metrics = db.query(ModelMetrics).order_by(ModelMetrics.training_date.desc()).all()
    return [metric.to_dict() for metric in metrics]
