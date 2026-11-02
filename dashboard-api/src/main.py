from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- Importamos nuestros routers modulares ---
from src.api.monitor_route import router as monitor_router
from src.api.management_route import router as management_router

def create_app() -> FastAPI:
    app = FastAPI(title="Minecraft Dashboard API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Registramos las rutas con el prefijo global de API ---
    app.include_router(monitor_router, prefix="/api/v1")
    app.include_router(management_router, prefix="/api/v1")

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "healthy"}

    return app

app = create_app()