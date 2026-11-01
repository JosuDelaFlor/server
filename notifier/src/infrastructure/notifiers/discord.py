import requests
import logging

from typing import Dict
from src.core.interfaces import INotifier

logger = logging.getLogger(__name__)

class DiscordNotifier(INotifier):
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url: str = webhook_url

    def notify(self, message: str) -> None:
        payload: Dict[str, str] = {"content": message}
        try:
            response: requests.Response = requests.post(self.webhook_url, json=payload, timeout=5)
            response.raise_for_status()
            logger.info("Notificación enviada a Discord exitosamente.")
        except requests.RequestException as e:
            logger.error(f"Error enviando webhook a Discord: {e}")