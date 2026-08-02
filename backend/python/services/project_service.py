from models.project import Project
from repositories.project_repo import ProjectRepository


class ProjectService:

    #receive the repository object and keep using the same one
    def __init__(self, repo: ProjectRepository):
        self.repository = repo

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