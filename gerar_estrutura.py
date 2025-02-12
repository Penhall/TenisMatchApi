import os
import subprocess
from datetime import datetime

def executar_tree():
    """
    Executa o comando tree e retorna o resultado
    Ignora diretórios e arquivos específicos
    """
    try:
        # Comando tree com flags para ignorar arquivos específicos
        comando = ['tree', '-I', 'venv|env|virtualenv|.venv|ENV|virtual|python-env|__pycache__|*.pyc|.git|.pytest_cache|.idea|.vscode|*.egg-info|dist|build|*.log|*.sqlite3|.env|node_modules|coverage|htmlcov|.coverage|.tox|.mypy_cache|.ruff_cache|.python-version|Pipfile.lock', '-a']
        
        # Executa o comando e captura a saída
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        # Retorna o resultado se o comando foi bem sucedido
        if resultado.returncode == 0:
            return resultado.stdout
        else:
            return f"Erro ao executar tree: {resultado.stderr}"
            
    except FileNotFoundError:
        return """O comando 'tree' não foi encontrado. Por favor, instale:
        - Linux: sudo apt-get install tree
        - macOS: brew install tree
        - Windows: winget install tree"""

def gerar_documentacao():
    """
    Gera o arquivo markdown com a estrutura do projeto
    """
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    estrutura = executar_tree()
    
    with open('STRUCTURE.md', 'w', encoding='utf-8') as f:
        # Cabeçalho
        f.write('# Estrutura do Projeto\n\n')
        f.write(f'> Documentação gerada em: {data_atual}\n\n')
        
        # Estrutura do projeto
        f.write('## Estrutura de Arquivos\n\n')
        f.write('```\n')
        f.write(estrutura)
        f.write('```\n\n')
        
        # Arquivos principais
        f.write('## Arquivos Principais\n\n')
        
        # dataset.py
        f.write('### dataset.py\n')
        f.write('- Classe `DatasetPreparation`\n')
        f.write('- Responsável por gerar dados de treinamento e preparar datasets\n')
        f.write('- Implementa cálculos de probabilidade de match\n\n')
        
        # training.py
        f.write('### training.py\n')
        f.write('- Classe `ModelTraining`\n')
        f.write('- Gerencia o modelo RandomForestClassifier\n')
        f.write('- Responsável por treinar, avaliar e fazer predições\n\n')
        
        # Instruções de atualização
        f.write('## Como Atualizar esta Documentação\n\n')
        f.write('1. Execute o script `gerar_estrutura.py`:\n')
        f.write('```bash\npython gerar_estrutura.py\n```\n\n')
        f.write('2. O arquivo STRUCTURE.md será atualizado automaticamente\n')

if __name__ == '__main__':
    print("Gerando documentação da estrutura do projeto...")
    gerar_documentacao()
    print("Documentação gerada com sucesso em STRUCTURE.md")