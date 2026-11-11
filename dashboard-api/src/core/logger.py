import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """Configura y devuelve un logger estructurado."""
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers si se llama múltiples veces
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Enviar logs a la consola (útil para Docker logs)
        handler = logging.StreamHandler(sys.stdout)
        
        # Formato estructurado: Fecha | Nivel | Módulo | Mensaje
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", 
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger