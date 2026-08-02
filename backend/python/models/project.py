from dataclasses import dataclass #minimal data model (like Go structs) which avoids constructor boilerplate of standard classes

@dataclass
class Project: 
    id: int 
    name: str