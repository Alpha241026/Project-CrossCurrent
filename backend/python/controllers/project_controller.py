from services.project_service import ProjectService
from flask import request,jsonify

class ProjectController:

    #receive the ProjectService object (dependency injection)
    def __init__(self, service: ProjectService):
        self.service = service
        
    #handle POST /projects requests
    def create_project(self):
        data = request.get_json() #read JSON body sent by the frontend
        name = data["name"] #extract the project name from the request.
        project = self.service.create_project(name) #ask service layer to create the project
        return jsonify(project.__dict__),201 #convert Project object to JSON & return HTTP 201 (Created)
        
    #handle GET /projects requests
    def get_projects(self):
        projects = self.service.get_projects() #ask service layer for all existing projects
        projlist = [] #convert Project objects into dictionaries for JSON serialization
        for proj in projects:
            projlist.append(proj.__dict__)
        return jsonify(projlist),200 #return the project list as JSON with HTTP 200 (OK)