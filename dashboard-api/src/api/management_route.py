from fastapi import APIRouter, Depends
from typing import Dict
from pydantic import BaseModel

from src.core.config import get_settings, Settings
from src.infrastructure.file_repository import FileServerConfigRepositoryImpl
from src.infrastructure.rcon_client import RconClientImpl
from src.services.management_service import ServerManagementService
from src.domain.models import ConfigUpdateRecord

router = APIRouter(prefix="/management", tags=["Management"])

class CommandRequest(BaseModel):
    command: str

def get_management_service(settings: Settings = Depends(get_settings)) -> ServerManagementService:
    rcon_client = RconClientImpl(
        host=settings.rcon_host,
        port=settings.rcon_port,
        password=settings.rcon_password
    )
    config_repo = FileServerConfigRepositoryImpl(file_path=settings.server_properties_path)
    return ServerManagementService(rcon_client=rcon_client, config_repo=config_repo)

@router.post("/command")
def execute_server_command(
    request: CommandRequest, 
    management_service: ServerManagementService = Depends(get_management_service)
):
    response = management_service.execute_command(request.command)
    return {"result": response}

@router.get("/properties", response_model=Dict[str, str])
def get_server_properties(management_service: ServerManagementService = Depends(get_management_service)):
    return management_service.get_properties()

@router.put("/properties")
def update_server_property(
    record: ConfigUpdateRecord, 
    management_service: ServerManagementService = Depends(get_management_service)
):
    success = management_service.update_property(record)
    return {"success": success, "updated_key": record.key}