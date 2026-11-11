from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from functools import lru_cache

class Settings(BaseSettings):
    """
    Configuración global del Backend.
    Lee automáticamente las variables de entorno inyectadas por Docker.
    """
    
    # RCON Config
    rcon_host: str = Field(default="minecraft", description="Host del contenedor de Minecraft")
    rcon_port: int = Field(default=25575, description="Puerto RCON del servidor")
    rcon_password: str = Field(..., description="Contraseña RCON obligatoria")
    
    # Docker Config
    container_name: str = Field(default="mc-server", description="Nombre del contenedor a monitorizar")
    
    # Rutas de archivos compartidos (Volúmenes)
    server_properties_path: str = Field(
        default="/server-data/server.properties", 
        description="Ruta montada del archivo server.properties"
    )

    api_key: str = Field(..., description="API Key estática para proteger los endpoints")

    # Configuración de Pydantic para ignorar variables extra que Docker pueda inyectar
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    """
    Patrón Singleton usando caché de Python. 
    Asegura que el archivo de configuración se lee y valida solo 1 vez al arrancar la API.
    """
    return Settings()