import re

from typing import List
from cachetools import TTLCache

from src.core.interfaces import IDockerClient, IRconClient
from src.domain.models import ServerStatus, Player
from src.domain.exceptions import DomainError
from src.core.logger import get_logger

logger = get_logger(__name__)

# Caché global en memoria: almacena 1 elemento (el estado global) por un máximo de 5 segundos
_status_cache = TTLCache(maxsize=1, ttl=5)

class ServerMonitorService:
    def __init__(self, docker_client: IDockerClient, rcon_client: IRconClient, container_name: str = "mc-server"):
        self.docker = docker_client
        self.rcon = rcon_client
        self.container_name = container_name

    def get_full_status(self) -> ServerStatus:
        # 1. Comprobar si tenemos un estado reciente en caché
        cache_key = "global_status"
        if cache_key in _status_cache:
            logger.info("Retornando estado del servidor desde la caché.")
            return _status_cache[cache_key]

        # 2. Si no hay caché (o expiró), consultamos la infraestructura real
        logger.info("Consultando infraestructura real (Docker + RCON)...")
        container_stats = self.docker.get_container_stats(self.container_name)
        
        is_online = container_stats.status == "running"
        players_online = 0
        max_players = 0
        players_list: List[Player] = []

        if is_online:
            try:
                rcon_response = self.rcon.execute_command("list")
                players_online, max_players, players_list = self._parse_player_list(rcon_response)
            except DomainError as e:
                # El error ya se loguea en RconClientImpl, aquí solo asumimos 0 jugadores temporalmente
                logger.warning(f"Contenedor encendido, pero RCON falló: {e}")

        # 3. Empaquetar el modelo
        status = ServerStatus(
            online=is_online,
            players_online=players_online,
            max_players=max_players,
            players=players_list,
            container=container_stats
        )
        
        # 4. Guardar en caché antes de devolverlo
        _status_cache[cache_key] = status
        return status

    def _parse_player_list(self, rcon_response: str) -> tuple[int, int, List[Player]]:
        if not rcon_response:
            return 0, 0, []

        try:
            match = re.search(r"There are (\d+) of a max of (\d+)", rcon_response)
            if not match:
                return 0, 0, []

            current = int(match.group(1))
            maximum = int(match.group(2))
            
            players = []
            if current > 0 and ":" in rcon_response:
                names_str = rcon_response.split(":")[1].strip()
                names = [name.strip() for name in names_str.split(",") if name.strip()]
                players = [Player(name=name) for name in names]

            return current, maximum, players
            
        except Exception as e:
            logger.error(f"Error parseando la lista de jugadores: {e}")
            return 0, 0, []