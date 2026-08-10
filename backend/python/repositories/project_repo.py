from models.project import Project #importing Project type model from models.project.py

class ProjectRepository: #stores Project objects in memory
    def __init__(self):
        self.projects = [] #attaching projects list attribute to objects / in-memory storage

    def create_project(self,project: Project): #method for creating/appending new project of type Project
        self.projects.append(project)
        
    def get_projects(self) -> list[Project]: #method for returning list of existing projects
        return self.projects