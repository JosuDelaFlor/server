from fastapi import Depends
from src.core.config import get_settings, Settings
from src.infrastructure.docker_client import DockerClientImpl
from src.infrastructure.rcon_client import RconClientImpl
from src.infrastructure.file_repository import FileServerConfigRepositoryImpl
from src.services.monitor_service import ServerMonitorService
from src.services.management_service import ServerManagementService

def get_monitor_service(settings: Settings = Depends(get_settings)) -> ServerMonitorService:
    return ServerMonitorService(
        docker_client=DockerClientImpl(), 
        rcon_client=RconClientImpl(
            host=settings.rcon_host,
            port=settings.rcon_port,
            password=settings.rcon_password
        ), 
        container_name=settings.container_name
    )

def get_management_service(settings: Settings = Depends(get_settings)) -> ServerManagementService:
    return ServerManagementService(
        rcon_client=RconClientImpl(
            host=settings.rcon_host,
            port=settings.rcon_port,
            password=settings.rcon_password
        ),
        config_repo=FileServerConfigRepositoryImpl(file_path=settings.server_properties_path),
        docker_client=DockerClientImpl(),
        container_name=settings.container_name
    )