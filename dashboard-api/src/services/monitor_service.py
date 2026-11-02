import re

from typing import List

from src.core.interfaces import IDockerClient, IRconClient
from src.domain.models import ServerStatus, Player
from src.domain.exceptions import DomainError

class ServerMonitorService:
    """Orquesta la infraestructura para cumplir con los casos de uso del Dashboard"""

    def __init__(self, docker_client: IDockerClient, rcon_client: IRconClient, container_name: str = "mc-server"):
        # Inyección de dependencias (DIP)
        self.docker = docker_client
        self.rcon = rcon_client
        self.container_name = container_name

    def get_full_status(self) -> ServerStatus:
        """Obtiene el estado unificado del servidor (Sistema + Juego)"""
        
        # 1. Consultar infraestructura (Docker)
        container_stats = self.docker.get_container_stats(self.container_name)
        
        is_online = container_stats.status == "running"
        players_online = 0
        max_players = 0
        players_list: List[Player] = []

        # 2. Si el contenedor está corriendo, consultamos al juego (RCON)
        if is_online:
            try:
                rcon_response = self.rcon.execute_command("list")
                players_online, max_players, players_list = self._parse_player_list(rcon_response)
            except DomainError:
                # Si falla RCON (ej. servidor arrancando), asumimos 0 jugadores temporalmente
                pass

        # 3. Empaquetar y devolver el modelo de Dominio
        return ServerStatus(
            online=is_online,
            players_online=players_online,
            max_players=max_players,
            players=players_list,
            container=container_stats
        )

    def _parse_player_list(self, rcon_response: str) -> tuple[int, int, List[Player]]:
        """
        Parsea la respuesta del comando 'list' de Minecraft.
        Ejemplo de respuesta esperada: "There are 2 of a max of 20 players online: Josu, Notch"
        """
        if not rcon_response:
            return 0, 0, []

        try:
            # Extraer números usando expresiones regulares
            match = re.search(r"There are (\d+) of a max of (\d+)", rcon_response)
            if not match:
                return 0, 0, []

            current = int(match.group(1))
            maximum = int(match.group(2))
            
            players = []
            if current > 0 and ":" in rcon_response:
                # Extraer los nombres después de los dos puntos
                names_str = rcon_response.split(":")[1].strip()
                names = [name.strip() for name in names_str.split(",") if name.strip()]
                players = [Player(name=name) for name in names]

            return current, maximum, players
            
        except Exception:
            return 0, 0, []