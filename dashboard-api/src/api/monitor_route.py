from fastapi import APIRouter, Depends

from src.core.config import get_settings, Settings
from src.infrastructure.docker_client import DockerClientImpl
from src.infrastructure.rcon_client import RconClientImpl
from src.services.monitor_service import ServerMonitorService
from src.domain.models import ServerStatus

router = APIRouter(prefix="/status", tags=["Monitor"])

def get_monitor_service(settings: Settings = Depends(get_settings)) -> ServerMonitorService:
    docker_client = DockerClientImpl()
    rcon_client = RconClientImpl(
        host=settings.rcon_host,
        port=settings.rcon_port,
        password=settings.rcon_password
    )
    return ServerMonitorService(docker_client=docker_client, rcon_client=rcon_client, container_name=settings.container_name)

@router.get("", response_model=ServerStatus)
def get_server_status(monitor_service: ServerMonitorService = Depends(get_monitor_service)):
    return monitor_service.get_full_status()