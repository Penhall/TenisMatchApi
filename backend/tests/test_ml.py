# /backend/tests/test_ml.py
import pytest
import numpy as np
from app.ml.dataset import DatasetPreparation
from app.ml.training import ModelTraining

def test_dataset_preparation():
    prep = DatasetPreparation()
    
    # Teste geração de dados sintéticos
    data = prep.generate_synthetic_data(n_samples=100)
    assert len(data) == 100
    assert all(isinstance(d, dict) for d in data)
    assert all('tenis_estilo' in d for d in data)
    
    # Teste preparação de features
    X, y = prep.prepare_features(data)
    assert len(X) == 100
    assert len(y) == 100
    assert X.shape[1] == 4  # 4 features

def test_model_training():
    # Preparar dados
    prep = DatasetPreparation()
    data = prep.generate_synthetic_data(n_samples=200)
    X, y = prep.prepare_features(data)
    
    # Treinar modelo
    trainer = ModelTraining()
    metrics, feature_importance = trainer.train_model(X, y)
    
    # Verificar métricas
    assert 0 <= metrics.accuracy <= 1
    assert 0 <= metrics.precision <= 1
    assert 0 <= metrics.recall <= 1
    assert 0 <= metrics.f1_score <= 1
    
    # Verificar ROC
    assert len(metrics.roc_curve_data) > 0
    assert all(0 <= point.fpr <= 1 for point in metrics.roc_curve_data)
    assert all(0 <= point.tpr <= 1 for point in metrics.roc_curve_data)
    
    # Verificar matriz de confusão
    assert len(metrics.confusion_matrix) == 2
    assert all(isinstance(item.actual_positive, int) for item in metrics.confusion_matrix)
    assert all(isinstance(item.actual_negative, int) for item in metrics.confusion_matrix)

def test_model_prediction():
    # Preparar modelo
    prep = DatasetPreparation()
    data = prep.generate_synthetic_data(n_samples=200)
    X, y = prep.prepare_features(data)
    
    trainer = ModelTraining()
    trainer.train_model(X, y)
    
    # Fazer predições
    test_data = prep.generate_synthetic_data(n_samples=10)
    X_test = prep.prepare_features(test_data)
    predictions, probabilities = trainer.predict(X_test)
    
    # Verificar predições
    assert len(predictions) == 10
    assert all(isinstance(p, (int, np.int64)) for p in predictions)
    assert all(p in [0, 1] for p in predictions)
    
    # Verificar probabilidades
    assert probabilities.shape == (10, 2)
    assert all(0 <= p <= 1 for p in probabilities.flatten())

def test_model_save_load(tmp_path):
    # Preparar modelo
    prep = DatasetPreparation()
    data = prep.generate_synthetic_data(n_samples=200)
    X, y = prep.prepare_features(data)
    
    trainer = ModelTraining()
    metrics_original, _ = trainer.train_model(X, y)
    
    # Salvar modelo
    model_path = tmp_path / "test_model.joblib"
    trainer.save_model(str(model_path))
    
    # Carregar modelo
    new_trainer = ModelTraining()
    new_trainer.load_model(str(model_path))
    
    # Verificar predições iguais
    X_test = prep.prepare_features(prep.generate_synthetic_data(10))
    pred1, prob1 = trainer.predict(X_test)
    pred2, prob2 = new_trainer.predict(X_test)
    
    np.testing.assert_array_equal(pred1, pred2)
    np.testing.assert_array_almost_equal(prob1, prob2)