from models.project import Project
from repositories.project_repo import ProjectRepository
from repositories.endpoint_repo import EndpointRepository

class ProjectService:

    #receive the repository objects and keep using the same ones
    def __init__(self, repo: ProjectRepository, endpoint_repo: EndpointRepository):
        self.repository = repo
        self.endpoint_repository = endpoint_repo


    #business logic for creating a project
    def create_project(self, name: str) -> Project:

        #reject empty or whitespace-only names
        if name.strip() == "":
            raise ValueError("Project name cannot be empty")

        #temporary ID generation until PostgreSQL
        new_id = len(self.repository.get_projects()) + 1

        #create the Project object
        project = Project(id=new_id, name=name)

        #ask the repository to store it
        self.repository.create_project(project)

        #return the created project
        return project


    #return all existing projects
    def get_projects(self) -> list[Project]:
    
        return self.repository.get_projects()


    #update an existing project name
    def update_project(self, id: int, name: str) -> Project:
    
        #reject empty or whitespace-only names
        if name.strip() == "":
            raise ValueError("Project name cannot be empty")

        #validate the project exists
        existing_project = self.repository.get_project_by_id(id)
        
        #if no project is found, reject invalid IDs
        if existing_project is None:
            raise ValueError("Project doesn't exist")
        
        #update Project object
        project = Project(id=id, name=name)
        
        #replace existing project in repository
        self.repository.update_project(id, project)
        
        #return updated project
        return project


    #delete an existing project
    def delete_project(self, id: int):
        
        #check whether project exists
        existing_project = self.repository.get_project_by_id(id)
        
        #if no project is found, reject invalid IDs
        if existing_project is None:
            raise ValueError("Project doesn't exist")
        
        #delete all endpoints belonging to the project
        self.endpoint_repository.delete_endpoints_by_project(id)
        
        #remove project from repository
        self.repository.delete_project(id)