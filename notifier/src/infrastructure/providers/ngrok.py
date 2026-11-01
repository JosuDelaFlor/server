import requests
import logging

from typing import Optional, List, Dict, Any
from src.core.interfaces import ITunnelProvider

logger = logging.getLogger(__name__)

class NgrokProvider(ITunnelProvider):
    def __init__(self, api_url: str) -> None:
        self.api_url: str = api_url

    def get_tunnel_url(self) -> Optional[str]:
        try:
            response: requests.Response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()
            
            data: Dict[str, Any] = response.json()
            tunnels: List[Dict[str, Any]] = data.get('tunnels', [])
            
            for t in tunnels:
                if t.get('proto') == 'tcp':
                    return t.get('public_url')
                    
        except requests.RequestException as e:
            logger.warning(f"Esperando a que la API de Ngrok responda... ({e})")
            
        return None