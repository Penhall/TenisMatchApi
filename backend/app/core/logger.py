# /backend/app/core/logger.py
import logging
import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings

# Configurar diretório de logs
log_path = Path("logs")
log_path.mkdir(exist_ok=True)

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging():
    # Remover handlers padrão
    logging.root.handlers = []
    logging.root.setLevel(logging.INFO)
    
    # Interceptar logs padrão
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    
    # Configurar handler para interceptar logs
    logging.root.addHandler(InterceptHandler())

    # Configurar Loguru
    logger.remove()  # Remover handler padrão
    
    # Adicionar handler para stdout com formatação colorida
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG" if settings.DEBUG else "INFO",
        colorize=True
    )
    
    # Adicionar handler para arquivo
    logger.add(
        log_path / "api.log",
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO"
    )

def get_logger(name: str):
    """
    Retorna um logger configurado para o módulo especificado
    """
    return logger.bind(module=name)