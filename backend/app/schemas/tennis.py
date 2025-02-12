# /backend/app/schemas/tennis.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TenisBase(BaseModel):
    tenis_estilo: str = Field(
        ..., 
        description="Estilo do tênis",
        example="ESP",
        enum=["ESP", "CAS", "VIN", "SOC", "FAS"]
    )
    tenis_marca: str = Field(
        ..., 
        description="Marca do tênis",
        example="Nike",
        enum=["Nike", "Adidas", "Vans", "Converse", "New Balance"]
    )
    tenis_cores: str = Field(
        ..., 
        description="Cores predominantes",
        example="BLK",
        enum=["BLK", "WHT", "COL", "NEU"]
    )
    tenis_preco: float = Field(
        ..., 
        ge=0, 
        description="Preço do tênis",
        example=299.99
    )
    match_success: int = Field(
        ..., 
        ge=0, 
        le=1, 
        description="Indicador de match (0 ou 1)",
        example=1
    )

class TenisCreate(TenisBase):
    """
    Schema para criação de um novo registro de tênis
    """
    pass

class TenisResponse(TenisBase):
    """
    Schema de resposta com dados do tênis e metadados
    """
    id: int = Field(..., description="ID único do registro")
    created_at: datetime = Field(..., description="Data de criação do registro")

    class Config:
        from_attributes = True

class ModelMetricsBase(BaseModel):
    accuracy: float = Field(
        ..., 
        ge=0, 
        le=1, 
        description="Acurácia do modelo",
        example=0.85
    )
    precision: float = Field(
        ..., 
        ge=0, 
        le=1, 
        description="Precisão do modelo",
        example=0.83
    )
    recall: float = Field(
        ..., 
        ge=0, 
        le=1, 
        description="Recall do modelo",
        example=0.82
    )
    f1_score: float = Field(
        ..., 
        ge=0, 
        le=1, 
        description="F1-Score do modelo",
        example=0.84
    )

class ModelMetricsCreate(ModelMetricsBase):
    """
    Schema para criação de métricas do modelo
    """
    pass

class ModelMetricsResponse(ModelMetricsBase):
    """
    Schema de resposta com métricas e metadados
    """
    id: int = Field(..., description="ID único do registro de métricas")
    training_date: datetime = Field(..., description="Data do treinamento")

    class Config:
        from_attributes = True

class ROCPoint(BaseModel):
    fpr: float = Field(..., description="Taxa de Falsos Positivos", example=0.1)
    tpr: float = Field(..., description="Taxa de Verdadeiros Positivos", example=0.9)

class ConfusionMatrixItem(BaseModel):
    name: str = Field(..., description="Nome da classe", example="Classe 0")
    actual_positive: int = Field(..., description="Verdadeiros Positivos", example=150)
    actual_negative: int = Field(..., description="Verdadeiros Negativos", example=50)

class ModelMetricsComplete(ModelMetricsBase):
    """
    Schema completo com todas as métricas do modelo
    """
    roc_curve_data: List[ROCPoint] = Field(..., description="Dados da curva ROC")
    confusion_matrix: List[ConfusionMatrixItem] = Field(..., description="Matriz de confusão")
    training_date: datetime = Field(..., description="Data do treinamento")

class BatchPredictionRequest(BaseModel):
    """
    Schema para requisição de predições em lote
    """
    records: List[TenisBase] = Field(..., description="Lista de registros para predição")

class PredictionResponse(BaseModel):
    """
    Schema de resposta com resultados da predição
    """
    match_probability: float = Field(
        ..., 
        description="Probabilidade de match",
        example=0.85
    )
    match_prediction: int = Field(
        ..., 
        description="Predição final (0 ou 1)",
        example=1
    )
    confidence_score: float = Field(
        ..., 
        description="Score de confiança da predição",
        example=0.92
    )