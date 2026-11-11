from pydantic import BaseModel
from typing import Dict

class CommandRequestSchema(BaseModel):
    command: str

class ConfigUpdateRequestSchema(BaseModel):
    key: str
    value: str

class ConfigUpdateResponseSchema(BaseModel):
    success: bool
    updated_key: str

class BulkConfigUpdateRequestSchema(BaseModel):
    properties: Dict[str, str]