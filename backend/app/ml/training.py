# /backend/app/ml/training.py
import os
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    roc_curve,
    auc,
    confusion_matrix
)
import joblib
import numpy as np
from typing import Dict, Any, Tuple, List
from datetime import datetime
from app.core.config import settings
from app.schemas.tennis import ModelMetricsComplete, ROCPoint, ConfusionMatrixItem

class ModelTraining:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
    def train_model(self, X, y) -> Tuple[ModelMetricsComplete, Dict[str, Any]]:
        """
        Treina o modelo e retorna métricas completas
        """
        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Treina modelo
        self.model.fit(X_train, y_train)
        
        # Faz predições
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]
        
        # Calcula métricas básicas
        metrics_dict = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred)),
            "recall": float(recall_score(y_test, y_pred)),
            "f1_score": float(f1_score(y_test, y_pred))
        }
        
        # Calcula curva ROC
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        
        # Prepara dados da curva ROC
        roc_data = [
            ROCPoint(fpr=float(f), tpr=float(t))
            for f, t in zip(fpr, tpr)
        ]
        
        # Calcula matriz de confusão
        cm = confusion_matrix(y_test, y_pred)
        cm_data = [
            ConfusionMatrixItem(
                name="Predicted Positive",
                actual_positive=int(cm[1][1]),
                actual_negative=int(cm[0][1])
            ),
            ConfusionMatrixItem(
                name="Predicted Negative",
                actual_positive=int(cm[1][0]),
                actual_negative=int(cm[0][0])
            )
        ]
        
        # Feature importance
        feature_importance = dict(zip(
            X.columns,
            self.model.feature_importances_
        ))
        
        # Cria objeto de métricas completo
        metrics = ModelMetricsComplete(
            **metrics_dict,
            roc_curve_data=roc_data,
            confusion_matrix=cm_data,
            training_date=datetime.utcnow()  # Adicionando a data de treinamento
        )
        
        return metrics, feature_importance
    
    def predict(self, X) -> Tuple[np.ndarray, np.ndarray]:
        """
        Faz predições usando o modelo treinado
        """
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        return predictions, probabilities
    
    def save_model(self, filename: str = None):
        """
        Salva o modelo treinado, criando o diretório se necessário
        """
        if filename is None:
            filename = settings.MODEL_PATH
            
        # Cria o diretório se não existir
        model_dir = os.path.dirname(filename)
        if model_dir:
            Path(model_dir).mkdir(parents=True, exist_ok=True)
            
        joblib.dump(self.model, filename)
    
    def load_model(self, filename: str = None):
        """
        Carrega um modelo salvo
        """
        if filename is None:
            filename = settings.MODEL_PATH
            
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Arquivo do modelo não encontrado: {filename}")
            
        self.model = joblib.load(filename)
        return self.model