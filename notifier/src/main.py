import os
import signal
import logging

from typing import Optional

from src.core.monitor import TunnelMonitor
from src.infrastructure.providers.ngrok import NgrokProvider
from src.infrastructure.notifiers.discord import DiscordNotifier
from src.infrastructure.notifiers.null import NullNotifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main() -> None:
    api_url: str = os.getenv("NGROK_API_URL", "http://ngrok:4040/api/tunnels")
    webhook_url: Optional[str] = os.getenv("DISCORD_WEBHOOK_URL")
    interval: int = int(os.getenv("CHECK_INTERVAL", "10"))

    # Patrón Null Object
    provider = NgrokProvider(api_url=api_url)
    if webhook_url:
        notifier = DiscordNotifier(webhook_url=webhook_url)
    else:
        logger.warning("DISCORD_WEBHOOK_URL no definida. Operando en modo silencioso (NullNotifier).")
        notifier = NullNotifier()
    
    monitor = TunnelMonitor(provider=provider, notifier=notifier, interval=interval)
    
    # Graceful Shutdown Handles
    def handle_signal(sig):
        logger.info(f"Señal {sig} recibida. Apagando monitor limpiamente...")
        monitor.stop()

    signal.signal(signal.SIGTERM, handle_signal) # Enviada por Docker al hacer docker stop
    signal.signal(signal.SIGINT, handle_signal)  # Enviada por Ctrl+C
    
    monitor.start()

if __name__ == "__main__":
    main()