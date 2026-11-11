import socket

from mcrcon import MCRcon
from src.core.interfaces import IRconClient
from src.domain.exceptions import RconConnectionError, RconAuthenticationError
from src.core.logger import get_logger

logger = get_logger(__name__)

class RconClientImpl(IRconClient):
    
    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password

    def execute_command(self, command: str) -> str:
        if not self.password:
            logger.error("Intento de conexión RCON sin contraseña configurada.")
            raise RconAuthenticationError("Contraseña RCON no configurada en el Dashboard.")

        try:
            with MCRcon(self.host, self.password, port=self.port) as mcr:
                return mcr.command(command)
                
        except ConnectionRefusedError as e:
            logger.warning(f"Conexión rechazada en {self.host}:{self.port}. Detalle: {e}")
            raise RconConnectionError("Conexión RCON rechazada (¿Está el servidor apagado?)")
        except socket.timeout as e:
            logger.warning(f"Timeout RCON en {self.host}:{self.port}. Detalle: {e}")
            raise RconConnectionError("Timeout al conectar por RCON (Servidor saturado o apagado)")
        except Exception as e:
            logger.exception(f"Error inesperado ejecutando comando RCON '{command}': {e}")
            raise RconConnectionError(f"Error inesperado en RCON: {str(e)}")