import time
import logging

from typing import Optional
from src.core.interfaces import ITunnelProvider, INotifier

logger = logging.getLogger(__name__)

class TunnelMonitor:
    def __init__(self, provider: ITunnelProvider, notifier: INotifier, interval: int) -> None:
        self.provider: ITunnelProvider = provider
        self.notifier: INotifier = notifier
        self.interval: int = interval
        self.last_url: Optional[str] = None

    def start(self) -> None:
        logger.info("Iniciando monitorización del túnel...")
        while True:
            url: Optional[str] = self.provider.get_tunnel_url()
            if url and url != self.last_url:
                clean_url: str = url.replace("tcp://", "")
                message: str = f"**Servidor de Minecraft Activo**\nConéctate usando esta IP: `{clean_url}`"
                
                self.notifier.notify(message)
                self.last_url = url
                
            time.sleep(self.interval)