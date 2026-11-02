from fastapi import APIRouter, Depends

from src.core.config import get_settings, Settings
from src.infrastructure.docker_client import DockerClientImpl
from src.infrastructure.rcon_client import RconClientImpl
from src.services.monitor import ServerMonitorService
from src.domain.models import ServerStatus

router = APIRouter(prefix="/api/v1", tags=["Monitor"])

# --- Inyección de Dependencias (Composition Root local) ---
def get_monitor_service(settings: Settings = Depends(get_settings)) -> ServerMonitorService:
    """
    Construye y provee el servicio de monitorización.
    FastAPI se encarga de llamar a esta función solo cuando un endpoint lo requiere.
    """
    # 1. Instanciamos la infraestructura (clientes)
    docker_client = DockerClientImpl()
    rcon_client = RconClientImpl(
        host=settings.rcon_host,
        port=settings.rcon_port,
        password=settings.rcon_password
    )
    
    # 2. Inyectamos la infraestructura en el servicio (lógica de negocio)
    return ServerMonitorService(
        docker_client=docker_client,
        rcon_client=rcon_client,
        container_name=settings.container_name
    )

# --- Endpoints REST ---
@router.get("/status", response_model=ServerStatus)
def get_server_status(monitor_service: ServerMonitorService = Depends(get_monitor_service)):
    """
    Retorna el estado combinado del contenedor de Docker y los jugadores dentro del juego.
    """
    return monitor_service.get_full_status()