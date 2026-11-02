from abc import ABC, abstractmethod
from typing import Dict
from src.domain.models import ContainerStats

class IDockerClient(ABC):
    """Contrato para interactuar con el motor de Docker"""
    
    @abstractmethod
    def get_container_stats(self, container_name: str) -> ContainerStats:
        pass
        
    @abstractmethod
    def restart_container(self, container_name: str) -> bool:
        pass

class IRconClient(ABC):
    """Contrato para enviar comandos al servidor en caliente"""
    
    @abstractmethod
    def execute_command(self, command: str) -> str:
        pass

class IServerConfigRepository(ABC):
    """Contrato para leer y escribir archivos del juego (La fuente de verdad)"""
    
    @abstractmethod
    def get_properties(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def update_property(self, key: str, value: str) -> bool:
        pass