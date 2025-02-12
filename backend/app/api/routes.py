# /backend/app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io

from app.database.session import get_db
from app.database.models import TenisData, ModelMetrics
from app.schemas.tennis import (
    TenisCreate, TenisResponse, ModelMetricsComplete,
    BatchPredictionRequest, PredictionResponse
)
from app.ml.dataset import DatasetPreparation
from app.ml.training import ModelTraining

router = APIRouter(
    prefix="/tennis",
    tags=["Tênis"],
    responses={404: {"description": "Item não encontrado"}}
)

@router.post(
    "/upload-csv",
    response_model=dict,
    summary="Upload de Dataset CSV",
    description="""
    Realiza o upload de um arquivo CSV contendo dados de tênis.
    
    O arquivo deve conter as seguintes colunas:
    - tenis_estilo: ESP, CAS, VIN, SOC, FAS
    - tenis_marca: Nike, Adidas, Vans, Converse, New Balance
    - tenis_cores: BLK, WHT, COL, NEU
    - tenis_preco: valor numérico positivo
    - match_success: 0 ou 1
    """,
    response_description="Mensagem de sucesso com quantidade de registros importados"
)
async def upload_csv(
    file: UploadFile = File(..., description="Arquivo CSV com dados de tênis"),
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
    description="Exporta todos os registros do banco de dados em formato CSV",
    response_description="Arquivo CSV contendo todos os registros"
)
async def export_csv(db: Session = Depends(get_db)):
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
    description="""
    Treina um novo modelo de Machine Learning usando os dados disponíveis.
    
    Requer no mínimo 100 registros no banco de dados.
    Retorna métricas completas do treinamento.
    """,
    response_description="Métricas detalhadas do modelo treinado"
)
async def train_model(db: Session = Depends(get_db)):
    records = db.query(TenisData).all()
    if len(records) < 100:
        raise HTTPException(400, "Dados insuficientes para treinamento (mínimo 100 registros)")
    
    data = [record.to_dict() for record in records]
    prep = DatasetPreparation()
    X, y = prep.prepare_features(data)
    
    trainer = ModelTraining()
    metrics, feature_importance = trainer.train_model(X, y)
    
    trainer.save_model()
    
    db_metrics = ModelMetrics(
        accuracy=metrics.accuracy,
        precision=metrics.precision,
        recall=metrics.recall,
        f1_score=metrics.f1_score
    )
    db.add(db_metrics)
    db.commit()
    
    return metrics

@router.post(
    "/predict",
    response_model=List[PredictionResponse],
    summary="Realizar Predições",
    description="""
    Realiza predições de match para uma lista de tênis.
    
    Para cada tênis, retorna:
    - Probabilidade de match
    - Predição (0 ou 1)
    - Score de confiança
    """,
    response_description="Lista de predições para cada tênis"
)
async def predict(
    request: BatchPredictionRequest,
    db: Session = Depends(get_db)
):
    prep = DatasetPreparation()
    X = prep.prepare_features(request.dict()['records'])
    
    trainer = ModelTraining()
    trainer.load_model()
    predictions, probabilities = trainer.predict(X)
    
    results = []
    for pred, prob in zip(predictions, probabilities):
        results.append(PredictionResponse(
            match_prediction=int(pred),
            match_probability=float(prob[1]),
            confidence_score=float(max(prob))
        ))
    
    return results

@router.get(
    "/metrics",
    response_model=List[ModelMetricsComplete],
    summary="Obter Métricas do Modelo",
    description="Retorna o histórico completo de métricas dos modelos treinados",
    response_description="Lista de métricas de todos os treinamentos realizados"
)
async def get_metrics(db: Session = Depends(get_db)):
    metrics = db.query(ModelMetrics).order_by(ModelMetrics.training_date.desc()).all()
    return [metric.to_dict() for metric in metrics]