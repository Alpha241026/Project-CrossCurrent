from dataclasses import dataclass #minimal data model (like Go structs) which avoids constructor boilerplate of standard classes
from datetime import datetime

@dataclass
class Project: 
    id: int 
    name: str
    
    #optional project metadata stored alongside the core project fields
    description: str | None = None
    
    #populated by PostgreSQL when the project is created/read from the database
    created_at: datetime | None = None
    updated_at: datetime | None = None