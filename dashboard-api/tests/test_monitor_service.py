from src.services.monitor_service import ServerMonitorService
from src.core.interfaces import IDockerClient, IRconClient
from src.domain.models import ContainerStats

class MockDockerClient(IDockerClient):
    def get_container_stats(self, name: str) -> ContainerStats:
        return ContainerStats(status="running", cpu_percent=15.0, memory_usage_mb=1024.0, memory_limit_mb=4096.0)
        
    def restart_container(self, name: str) -> bool:
        return True

class MockRconClient(IRconClient):
    def execute_command(self, command: str) -> str:
        if command == "list":
            return "There are 2 of a max of 20 players online: Josu, Notch"
        return ""

def test_get_full_status_when_server_is_online():
    # Inyectamos los mocks puramente en memoria
    service = ServerMonitorService(
        docker_client=MockDockerClient(),
        rcon_client=MockRconClient(),
        container_name="test-server"
    )
    
    status = service.get_full_status()
    
    # Validamos que la lógica de negocio procesa bien los datos crudos
    assert status.online is True
    assert status.players_online == 2
    assert status.max_players == 20
    assert len(status.players) == 2
    assert status.players[0].name == "Josu"
    assert status.container.cpu_percent == 15.0