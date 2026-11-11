import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from src.services.monitor_service import ServerMonitorService
from src.api.dependencies import get_monitor_service
from src.core.config import get_settings, Settings
from src.core.logger import get_logger

logger = get_logger(__name__)

# No le ponemos la dependencia global de API Key aquí porque los WS usan Query Params
router = APIRouter(prefix="/ws", tags=["Websocket"])

@router.websocket("/status")
async def websocket_status_endpoint(
    websocket: WebSocket,
    api_key: str = Query(..., description="API Key para autenticación"),
    settings: Settings = Depends(get_settings),
    monitor_service: ServerMonitorService = Depends(get_monitor_service)
):
    # 1. Autenticación manual por Query Parameter
    if api_key != settings.api_key:
        logger.warning("Intento de conexión WebSocket con API Key inválida.")
        await websocket.close(code=1008, reason="Acceso denegado: API Key inválida")
        return

    # 2. Aceptamos la conexión
    await websocket.accept()
    logger.info("Cliente WebSocket conectado al dashboard.")

    try:
        while True:
            # 3. Obtenemos el estado. 
            # (Tranquilo, tu TTL de 5s en monitor_service evita que esto sature Docker)
            status = monitor_service.get_full_status()
            
            # 4. Enviamos el JSON al frontend
            await websocket.send_text(status.model_dump_json())
            
            # 5. Esperamos 5 segundos exactos antes de la siguiente actualización
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        logger.info("Cliente WebSocket desconectado normalmente.")
    except Exception as e:
        logger.error(f"Error inesperado en la conexión WebSocket: {e}", exc_info=True)
        # Asegurarnos de cerrar el socket si hay un error crítico
        try:
            await websocket.close(code=1011)
        except Exception:
            pass