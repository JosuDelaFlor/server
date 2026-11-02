from pydantic import BaseModel
from typing import List

class ContainerStats(BaseModel):
    status: str
    cpu_percent: float
    memory_usage_mb: float
    memory_limit_mb: float

class Player(BaseModel):
    name: str

class ServerStatus(BaseModel):
    online: bool
    players_online: int
    max_players: int
    players: List[Player]
    container: ContainerStats

class ConfigUpdateRecord(BaseModel):
    key: str
    value: str