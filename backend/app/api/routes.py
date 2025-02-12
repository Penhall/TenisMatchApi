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

router = APIRouter()

@router.post("/upload-csv", response_model=dict)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Arquivo deve ser CSV")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validar colunas
        required_cols = ['tenis_estilo', 'tenis_marca', 'tenis_cores', 'tenis_preco', 'match_success']
        if not all(col in df.columns for col in required_cols):
            raise HTTPException(400, "CSV não contém todas as colunas necessárias")
        
        # Converter para registros do banco
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
        
        # Salvar no banco
        db.bulk_save_objects(records)
        db.commit()
        
        return {"message": f"Importados {len(records)} registros com sucesso"}
        
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/export-csv")
async def export_csv(db: Session = Depends(get_db)):
    # Buscar todos os registros
    records = db.query(TenisData).all()
    
    # Converter para DataFrame
    data = [record.to_dict() for record in records]
    df = pd.DataFrame(data)
    
    # Converter para CSV
    output = io.StringIO()
    df.to_csv(output, index=False)
    
    return output.getvalue()

@router.post("/train", response_model=ModelMetricsComplete)
async def train_model(db: Session = Depends(get_db)):
    # Buscar dados de treinamento
    records = db.query(TenisData).all()
    if len(records) < 100:
        raise HTTPException(400, "Dados insuficientes para treinamento (mínimo 100 registros)")
    
    # Preparar dados
    data = [record.to_dict() for record in records]
    prep = DatasetPreparation()
    X, y = prep.prepare_features(data)
    
    # Treinar modelo
    trainer = ModelTraining()
    metrics, feature_importance = trainer.train_model(X, y)
    
    # Salvar modelo
    trainer.save_model()
    
    # Salvar métricas no banco
    db_metrics = ModelMetrics(
        accuracy=metrics.accuracy,
        precision=metrics.precision,
        recall=metrics.recall,
        f1_score=metrics.f1_score
    )
    db.add(db_metrics)
    db.commit()
    
    return metrics

@router.post("/predict", response_model=List[PredictionResponse])
async def predict(
    request: BatchPredictionRequest,
    db: Session = Depends(get_db)
):
    # Preparar dados
    prep = DatasetPreparation()
    X = prep.prepare_features(request.dict()['records'])
    
    # Carregar modelo e fazer predições
    trainer = ModelTraining()
    trainer.load_model()
    predictions, probabilities = trainer.predict(X)
    
    # Preparar resposta
    results = []
    for pred, prob in zip(predictions, probabilities):
        results.append(PredictionResponse(
            match_prediction=int(pred),
            match_probability=float(prob[1]),
            confidence_score=float(max(prob))
        ))
    
    return results

@router.get("/metrics", response_model=List[ModelMetricsComplete])
async def get_metrics(db: Session = Depends(get_db)):
    metrics = db.query(ModelMetrics).order_by(ModelMetrics.training_date.desc()).all()
    return [metric.to_dict() for metric in metrics]