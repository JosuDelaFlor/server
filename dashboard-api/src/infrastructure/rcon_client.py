import socket

from mcrcon import MCRcon

from src.core.interfaces import IRconClient

class RconClientImpl(IRconClient):
    """Implementación real para enviar comandos vía RCON a Minecraft"""
    
    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password

    def execute_command(self, command: str) -> str:
        """
        Abre la conexión, ejecuta el comando, devuelve la respuesta y cierra.
        Si el servidor está apagado o no responde, devuelve un string vacío o mensaje de error controlado.
        """
        if not self.password:
            return "Error: Contraseña RCON no configurada en el Dashboard."

        try:
            # El context manager (with) asegura que la conexión se cierre siempre, 
            # incluso si ocurre una excepción a mitad del comando.
            with MCRcon(self.host, self.password, port=self.port) as mcr:
                response = mcr.command(command)
                return response
                
        except ConnectionRefusedError:
            return "Error: Conexión RCON rechazada (¿Está el servidor apagado?)"
        except socket.timeout:
            return "Error: Timeout al conectar por RCON (Servidor saturado o apagado)"
        except Exception as e:
            return f"Error inesperado en RCON: {str(e)}"