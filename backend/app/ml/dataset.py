# /backend/app/ml/dataset.py
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple, Optional, Union
from sklearn.preprocessing import LabelEncoder, StandardScaler

class DatasetPreparation:
    def __init__(self):
        self.styles = ['ESP', 'CAS', 'VIN', 'SOC', 'FAS']
        self.brands = ['Nike', 'Adidas', 'Vans', 'Converse', 'New Balance']
        self.colors = ['BLK', 'WHT', 'COL', 'NEU']
        
        self.style_encoder = LabelEncoder()
        self.brand_encoder = LabelEncoder()
        self.color_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        
        # Fit encoders with possible values
        self.style_encoder.fit(self.styles)
        self.brand_encoder.fit(self.brands)
        self.color_encoder.fit(self.colors)
        
        # Flag para controlar se o scaler já foi fitted
        self._is_scaler_fitted = False
    
    def prepare_features(
        self,
        data: Union[List[Dict[str, Any]], pd.DataFrame]
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.Series]]:
        """
        Prepara features para treinamento ou predição
        """
        # Converte para DataFrame se não for
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data.copy()
        
        # Encoding categórico
        X = pd.DataFrame({
            'tenis_estilo': self.style_encoder.transform(df['tenis_estilo']),
            'tenis_marca': self.brand_encoder.transform(df['tenis_marca']),
            'tenis_cores': self.color_encoder.transform(df['tenis_cores']),
        })
        
        # Normalização do preço
        price_values = df['tenis_preco'].values.reshape(-1, 1)
        if not self._is_scaler_fitted:
            X['tenis_preco'] = self.scaler.fit_transform(price_values)
            self._is_scaler_fitted = True
        else:
            X['tenis_preco'] = self.scaler.transform(price_values)
        
        if 'match_success' not in df.columns:            
            return X
        
        y = df['match_success']
        return X, y
    
    @staticmethod
    def generate_synthetic_data(n_samples: int = 1000) -> List[Dict[str, Any]]:
        """
        Gera dataset sintético para testes e desenvolvimento
        """
        prep = DatasetPreparation()
        data = []
        
        for _ in range(n_samples):
            record = {
                'tenis_estilo': np.random.choice(prep.styles),
                'tenis_marca': np.random.choice(prep.brands),
                'tenis_cores': np.random.choice(prep.colors),
                'tenis_preco': float(np.random.randint(100, 1000)),
                'match_success': 1 if np.random.random() < 0.5 else 0
            }
            
            prob = prep._calculate_match_probability(record)
            record['match_success'] = 1 if np.random.random() < prob else 0
            
            data.append(record)
        
        return data
    
    def _calculate_match_probability(self, record: Dict[str, Any]) -> float:
        """
        Calcula probabilidade de match baseado em regras de negócio
        """
        prob = 0.5  # Probabilidade base
        
        # Ajusta baseado no estilo
        style_probs = {
            'ESP': 0.7,  # Esportivo tem alta chance
            'CAS': 0.6,  # Casual também
            'VIN': 0.5,  # Vintage médio
            'SOC': 0.4,  # Social menor
            'FAS': 0.6   # Fashion bom
        }
        prob += style_probs.get(record['tenis_estilo'], 0)
        
        # Ajusta baseado na marca
        brand_probs = {
            'Nike': 0.1,
            'Adidas': 0.1,
            'Vans': 0.05,
            'Converse': 0.05,
            'New Balance': 0.05
        }
        prob += brand_probs.get(record['tenis_marca'], 0)
        
        # Ajusta baseado no preço
        if record['tenis_preco'] < 200:
            prob -= 0.1
        elif record['tenis_preco'] > 800:
            prob -= 0.05
        
        # Normaliza probabilidade
        return min(max(prob / 2, 0), 1)