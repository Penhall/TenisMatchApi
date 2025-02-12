# /backend/app/schemas/tennis.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TenisBase(BaseModel):
    tenis_estilo: str = Field(..., description="Estilo do tênis (ESP, CAS, VIN, SOC, FAS)")
    tenis_marca: str = Field(..., description="Marca do tênis")
    tenis_cores: str = Field(..., description="Cores predominantes (BLK, WHT, COL, NEU)")
    tenis_preco: float = Field(..., ge=0, description="Preço do tênis")
    match_success: int = Field(..., ge=0, le=1, description="Indicador de match (0 ou 1)")

class TenisCreate(TenisBase):
    pass

class TenisResponse(TenisBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ModelMetricsBase(BaseModel):
    accuracy: float = Field(..., ge=0, le=1)
    precision: float = Field(..., ge=0, le=1)
    recall: float = Field(..., ge=0, le=1)
    f1_score: float = Field(..., ge=0, le=1)

class ModelMetricsCreate(ModelMetricsBase):
    pass

class ModelMetricsResponse(ModelMetricsBase):
    id: int
    training_date: datetime

    class Config:
        from_attributes = True

class ROCPoint(BaseModel):
    fpr: float
    tpr: float

class ConfusionMatrixItem(BaseModel):
    name: str
    actual_positive: int
    actual_negative: int

class ModelMetricsComplete(ModelMetricsBase):
    roc_curve_data: List[ROCPoint]
    confusion_matrix: List[ConfusionMatrixItem]
    training_date: datetime

class BatchPredictionRequest(BaseModel):
    records: List[TenisBase]

class PredictionResponse(BaseModel):
    match_probability: float
    match_prediction: int  # 0 ou 1
    confidence_score: float