from models.project import Project
from repositories.project_repo import ProjectRepository
from repositories.endpoint_repo import EndpointRepository


class ProjectService:

    #receive the repository objects and keep using the same ones
    #EndpointRepository is still accepted for now because the application
    #wiring already provides it; project deletion is now handled by PostgreSQL
    def __init__(self, repo: ProjectRepository, endpoint_repo: EndpointRepository):
        self.repository = repo
        self.endpoint_repository = endpoint_repo


    #business logic for creating a project
    def create_project(self, name: str, description: str | None) -> Project:

        #reject empty or whitespace-only names
        if name.strip() == "":
            raise ValueError("Project name cannot be empty")

        #PostgreSQL now generates the project ID
        #the repository also fills in the database-generated timestamps
        project = Project(
            id=0,
            name=name,
            description=description
        )

        #ask the repository to store it and return the database-generated data
        return self.repository.create_project(project)


    #return all existing projects
    def get_projects(self) -> list[Project]:

        return self.repository.get_projects()


    #update an existing project name and description
    def update_project(self, id: int, name: str, description: str | None) -> Project:

        #reject empty or whitespace-only names
        if name.strip() == "":
            raise ValueError("Project name cannot be empty")

        #validate the project exists
        existing_project = self.repository.get_project_by_id(id)

        #if no project is found, reject invalid IDs
        if existing_project is None:
            raise ValueError("Project doesn't exist")

        #create the updated Project object while preserving existing metadata
        project = Project(
            id=id,
            name=name,
            description=description,
            created_at=existing_project.created_at,
            updated_at=existing_project.updated_at
        )

        #ask the repository to update the project in PostgreSQL
        updated_project = self.repository.update_project(id, project)

        #return the project returned by PostgreSQL
        return updated_project


    #delete an existing project
    def delete_project(self, id: int):

        #check whether the project exists
        existing_project = self.repository.get_project_by_id(id)

        #if no project is found, reject invalid IDs
        if existing_project is None:
            raise ValueError("Project doesn't exist")

        #PostgreSQL's ON DELETE CASCADE automatically removes
        #endpoints belonging to this project
        self.repository.delete_project(id)