import threading
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
        self._stop_event = threading.Event()

    def _check_tunnel(self) -> None:
        url: Optional[str] = self.provider.get_tunnel_url()
        if url and url != self.last_url:
            clean_url: str = url.replace("tcp://", "")
            message: str = f"**Servidor de Minecraft Activo**\nConéctate usando esta IP: `{clean_url}`"
            self.notifier.notify(message)
            self.last_url = url

    def start(self) -> None:
        logger.info("Iniciando monitorización del túnel...")
        while not self._stop_event.is_set():
            self._check_tunnel()
            self._stop_event.wait(self.interval)
        logger.info("Monitorización detenida de forma segura.")

    def stop(self) -> None:
        self._stop_event.set()