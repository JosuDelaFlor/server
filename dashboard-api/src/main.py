from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.api.monitor_route import router as monitor_router
from src.api.management_route import router as management_router
from src.domain.exceptions import DomainError

from src.domain.exceptions import DomainError
from src.core.logger import get_logger

logger = get_logger("api_gateway")

def create_app() -> FastAPI:
    app = FastAPI(title="Minecraft Dashboard API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        # Registramos como warning porque es un error de negocio controlado, no un crash del servidor
        logger.warning(f"Petición fallida [{request.method} {request.url.path}] - Motivo: {str(exc)}")
        
        return JSONResponse(
            status_code=400,
            content={"success": False, "detail": str(exc)}
        )

    # Añadir un capturador para errores 500 imprevistos
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"Error crítico no controlado en [{request.method} {request.url.path}]", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": "Error interno del servidor."}
        )

    # --- Registramos las rutas con el prefijo global de API ---
    app.include_router(monitor_router, prefix="/api/v1")
    app.include_router(management_router, prefix="/api/v1")

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        """Atrapa cualquier error de negocio y lo devuelve como HTTP 400"""
        return JSONResponse(
            status_code=400,
            content={"success": False, "detail": str(exc)}
        )
    
    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "healthy"}

    return app

app = create_app()