from dataclasses import dataclass

@dataclass
class Endpoint:
    id: int
    project_id: int
    name: str
    method: str
    url: str
    body: dict | None #type hinting with union types; body attribute can either be a dictionary or none