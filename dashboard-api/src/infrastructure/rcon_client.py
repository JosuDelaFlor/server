import socket

from mcrcon import MCRcon
from src.core.interfaces import IRconClient
from src.domain.exceptions import RconConnectionError, RconAuthenticationError

class RconClientImpl(IRconClient):
    
    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password

    def execute_command(self, command: str) -> str:
        if not self.password:
            raise RconAuthenticationError("Contraseña RCON no configurada en el Dashboard.")

        try:
            with MCRcon(self.host, self.password, port=self.port) as mcr:
                return mcr.command(command)
                
        except ConnectionRefusedError:
            raise RconConnectionError("Conexión RCON rechazada (¿Está el servidor apagado?)")
        except socket.timeout:
            raise RconConnectionError("Timeout al conectar por RCON (Servidor saturado o apagado)")
        except Exception as e:
            raise RconConnectionError(f"Error inesperado en RCON: {str(e)}")