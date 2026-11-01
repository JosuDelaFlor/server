import logging

from src.core.interfaces import INotifier

logger = logging.getLogger(__name__)

class NullNotifier(INotifier):
    def notify(self, message: str) -> None:
        logger.info(f"[NullNotifier] Webhook no configurado. Mensaje interceptado: {message}")