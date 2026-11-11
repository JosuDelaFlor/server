from typing import Dict
from src.core.interfaces import IRconClient, IServerConfigRepository, IDockerClient
from src.domain.models import ConfigUpdateRecord
from src.core.logger import get_logger

logger = get_logger(__name__)

class ServerManagementService:
    # 1. Inyectamos IDockerClient y el nombre del contenedor
    def __init__(self, rcon_client: IRconClient, config_repo: IServerConfigRepository, docker_client: IDockerClient, container_name: str):
        self.rcon = rcon_client
        self.config = config_repo
        self.docker = docker_client
        self.container_name = container_name

    def execute_command(self, command: str) -> str:
        clean_command = command.lstrip('/')
        return self.rcon.execute_command(clean_command)

    def get_properties(self) -> Dict[str, str]:
        return self.config.get_properties()

    def update_property(self, record: ConfigUpdateRecord) -> bool:
        return self.config.update_property(record.key, record.value)

    # 2. Nuevo método para actualizar en lote
    def update_properties_bulk(self, properties: Dict[str, str]) -> bool:
        success = True
        for key, value in properties.items():
            if not self.config.update_property(key, str(value)):
                success = False
        return success

    # 3. Nuevo método para reiniciar
    def restart_server(self) -> bool:
        logger.info(f"Reiniciando contenedor {self.container_name} desde el Dashboard...")
        return self.docker.restart_container(self.container_name)