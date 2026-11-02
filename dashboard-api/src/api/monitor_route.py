from fastapi import APIRouter, Depends
from src.services.monitor_service import ServerMonitorService
from src.domain.models import ServerStatus
from src.api.dependencies import get_monitor_service

router = APIRouter(prefix="/status", tags=["Monitor"])

@router.get("", response_model=ServerStatus)
def get_server_status(monitor_service: ServerMonitorService = Depends(get_monitor_service)):
    return monitor_service.get_full_status()