from fastapi import APIRouter, Depends
from typing import Dict

from src.services.management_service import ServerManagementService
from src.domain.models import ConfigUpdateRecord
from src.api.dependencies import get_management_service
from src.api.schemas import CommandRequestSchema, ConfigUpdateRequestSchema, ConfigUpdateResponseSchema

router = APIRouter(prefix="/management", tags=["Management"])

@router.post("/command")
def execute_server_command(
    request: CommandRequestSchema, 
    management_service: ServerManagementService = Depends(get_management_service)
):
    response = management_service.execute_command(request.command)
    return {"result": response}

@router.get("/properties", response_model=Dict[str, str])
def get_server_properties(management_service: ServerManagementService = Depends(get_management_service)):
    return management_service.get_properties()

@router.put("/properties", response_model=ConfigUpdateResponseSchema)
def update_server_property(
    request: ConfigUpdateRequestSchema, 
    management_service: ServerManagementService = Depends(get_management_service)
):
    # Mapeo de DTO (Schema) a Modelo de Dominio
    record = ConfigUpdateRecord(key=request.key, value=request.value)
    success = management_service.update_property(record)
    return ConfigUpdateResponseSchema(success=success, updated_key=record.key)