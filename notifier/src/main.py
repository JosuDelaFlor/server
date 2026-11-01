import os
import sys
import logging

from typing import Optional

from src.core.monitor import TunnelMonitor
from src.infrastructure.providers.ngrok import NgrokProvider
from src.infrastructure.notifiers.discord import DiscordNotifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main() -> None:
    api_url: str = os.getenv("NGROK_API_URL", "http://ngrok:4040/api/tunnels")
    webhook_url: Optional[str] = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        logger.error("La variable de entorno DISCORD_WEBHOOK_URL es obligatoria.")
        sys.exit(1)
        
    try:
        interval: int = int(os.getenv("CHECK_INTERVAL", "10"))
    except ValueError:
        logger.warning("CHECK_INTERVAL inválido. Usando 10 segundos por defecto.")
        interval = 10

    provider = NgrokProvider(api_url=api_url)
    notifier = DiscordNotifier(webhook_url=webhook_url)
    
    monitor = TunnelMonitor(provider=provider, notifier=notifier, interval=interval)
    
    try:
        monitor.start()
    except KeyboardInterrupt:
        logger.info("Monitor detenido manualmente por señal del sistema.")

if __name__ == "__main__":
    main()