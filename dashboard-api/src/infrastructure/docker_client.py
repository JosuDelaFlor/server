import docker

from docker.errors import NotFound, APIError

from src.core.interfaces import IDockerClient
from src.domain.models import ContainerStats

class DockerClientImpl(IDockerClient):
    """Implementación real para interactuar con el socket de Docker"""
    
    def __init__(self):
        # Conecta automáticamente con /var/run/docker.sock (montado en el docker-compose)
        self.client = docker.from_env()

    def get_container_stats(self, container_name: str) -> ContainerStats:
        try:
            container = self.client.containers.get(container_name)
            
            # stream=False obliga a Docker a dar una lectura puntual y cerrar la conexión
            stats = container.stats(stream=False)
            
            # Cálculo de memoria (MB)
            memory_usage = stats.get('memory_stats', {}).get('usage', 0) / (1024 * 1024)
            memory_limit = stats.get('memory_stats', {}).get('limit', 0) / (1024 * 1024)
            
            # Cálculo de CPU (%)
            cpu_percent = self._calculate_cpu_percent(stats)
            
            return ContainerStats(
                status=container.status,
                cpu_percent=round(cpu_percent, 2),
                memory_usage_mb=round(memory_usage, 2),
                memory_limit_mb=round(memory_limit, 2)
            )
            
        except NotFound:
            return ContainerStats(status="not_found", cpu_percent=0.0, memory_usage_mb=0.0, memory_limit_mb=0.0)
        except APIError:
            return ContainerStats(status="error", cpu_percent=0.0, memory_usage_mb=0.0, memory_limit_mb=0.0)

    def restart_container(self, container_name: str) -> bool:
        try:
            container = self.client.containers.get(container_name)
            container.restart()
            return True
        except (NotFound, APIError):
            return False

    def _calculate_cpu_percent(self, stats: dict) -> float:
        """Fórmula oficial de Docker para calcular el % de CPU"""
        cpu_count = len(stats.get('cpu_stats', {}).get('cpu_usage', {}).get('percpu_usage', []))
        cpu_percent = 0.0
        
        cpu_delta = float(stats['cpu_stats']['cpu_usage']['total_usage']) - float(stats['precpu_stats']['cpu_usage']['total_usage'])
        system_delta = float(stats['cpu_stats']['system_cpu_usage']) - float(stats['precpu_stats']['system_cpu_usage'])
        
        if system_delta > 0.0 and cpu_delta > 0.0:
            cpu_percent = (cpu_delta / system_delta) * cpu_count * 100.0
            
        return cpu_percent