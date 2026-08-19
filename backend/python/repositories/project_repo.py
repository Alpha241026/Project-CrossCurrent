from models.project import Project #importing Project type model from models/project.py

class ProjectRepository: #stores Project objects in memory
    def __init__(self):
        self.projects = [] #attaching projects list attribute to objects / in-memory storage

    def create_project(self, project: Project): #method for creating/appending new project of type Project
        self.projects.append(project)
        
    def get_project_by_id(self,project_id: int) -> Project | None: #method for returning a single project from the list...None if not found
            for pro in self.projects:
                if pro.id==project_id:
                    return pro
            return None
        
    def get_projects(self) -> list[Project]: #method for returning list of existing projects
        return self.projects
    
    def update_project(self, project_id: int, project: Project): #method for updating a project
        for index,pro in enumerate(self.projects):
            if pro.id==project_id:
                self.projects[index]=project
        return None #if no project of given id is found
    
    def delete_project(self, project_id: int): #method for deleting a project
        for pro in self.projects:
            if pro.id==project_id:
                self.projects.remove(pro)
        return None #if no project of given id is found
