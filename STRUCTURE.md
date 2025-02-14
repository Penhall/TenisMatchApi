# Estrutura do Projeto

> Documentação gerada em: 12/02/2025 15:37

## Estrutura de Arquivos

```bash
O comando 'tree' não foi encontrado. Por favor, instale:
        - Linux: sudo apt-get install tree
        - macOS: brew install tree
        - Windows: winget install tree
```

## Arquivos Principais

### dataset.py

- Classe `DatasetPreparation`
- Responsável por gerar dados de treinamento e preparar datasets
- Implementa cálculos de probabilidade de match

### training.py

- Classe `ModelTraining`
- Gerencia o modelo RandomForestClassifier
- Responsável por treinar, avaliar e fazer predições

## Como Atualizar esta Documentação

1. Execute o script `gerar_estrutura.py`:

```bash
python gerar_estrutura.py
```

1. O arquivo STRUCTURE.md será atualizado automaticamente.