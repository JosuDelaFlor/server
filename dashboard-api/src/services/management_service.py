from typing import Dict

from src.core.interfaces import IRconClient, IServerConfigRepository
from src.domain.models import ConfigUpdateRecord

class ServerManagementService:
    """Orquesta las acciones de administración activa del servidor"""

    def __init__(self, rcon_client: IRconClient, config_repo: IServerConfigRepository):
        self.rcon = rcon_client
        self.config = config_repo

    def execute_command(self, command: str) -> str:
        """Ejecuta un comando en caliente y devuelve la salida de la consola"""
        # Eliminar la barra diagonal inicial si el usuario la pone por costumbre
        clean_command = command.lstrip('/')
        return self.rcon.execute_command(clean_command)

    def get_properties(self) -> Dict[str, str]:
        """Obtiene todas las reglas actuales del servidor"""
        return self.config.get_properties()

    def update_property(self, record: ConfigUpdateRecord) -> bool:
        """Actualiza una regla específica en el archivo"""
        return self.config.update_property(record.key, record.value)