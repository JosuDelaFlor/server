from abc import ABC, abstractmethod
from typing import Optional

class ITunnelProvider(ABC):
    @abstractmethod
    def get_tunnel_url(self) -> Optional[str]:
        pass

class INotifier(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        pass