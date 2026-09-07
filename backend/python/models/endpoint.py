from dataclasses import dataclass
from datetime import datetime

@dataclass
class Endpoint:
    id: int
    project_id: int
    name: str
    method: str
    url: str
    params: dict
    headers: dict
    body: dict | None #type hinting with union types; body attribute can either be a dictionary or none
    
    #optional endpoint metadata stored alongside the request configuration
    description: str | None = None
    
    #populated by PostgreSQL when the endpoint is created/read from the database
    created_at: datetime | None = None
    updated_at: datetime | None = None