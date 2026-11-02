from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router as api_router

def create_app() -> FastAPI:
    """Fábrica de la aplicación FastAPI (Factory Pattern)"""
    
    app = FastAPI(
        title="Minecraft Dashboard API",
        description="API RESTful para la gestión y monitorización del servidor Minecraft",
        version="1.0.0"
    )

    # Configuración estricta de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",   # Entorno de desarrollo React (Vite)
            "http://127.0.0.1:3000"
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Registro de rutas (Endpoints)
    app.include_router(api_router)

    @app.get("/health", tags=["Health"])
    def health_check():
        """Endpoint ultra ligero para comprobar si la API está viva"""
        return {"status": "healthy"}

    return app

# Instancia global que será servida por Uvicorn
app = create_app()