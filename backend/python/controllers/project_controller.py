from services.project_service import ProjectService
from flask import request, jsonify


class ProjectController:

    #receive the ProjectService object (dependency injection)
    def __init__(self, service: ProjectService):
        self.service = service


    #handle POST /projects requests
    def create_project(self):
        data = request.get_json()  #read JSON body sent by the frontend
        name = data["name"]  #extract the project name from the request
        description = data.get("description")  #extract the optional project description
        project = self.service.create_project(name, description)  #ask service layer to create the project
        return jsonify(project.__dict__), 201  #convert Project object to JSON & return HTTP 201 (Created)


    #handle GET /projects requests
    def get_projects(self):
        projects = self.service.get_projects()  #ask service layer for all existing projects
        projlist = []  #convert Project objects into dictionaries for JSON serialization

        for proj in projects:
            projlist.append(proj.__dict__)

        return jsonify(projlist), 200  #return the project list as JSON with HTTP 200 (OK)


    #handle PATCH /projects/{id} requests
    def update_project(self, id: int):
        data = request.get_json()  #read JSON body sent by frontend
        name = data["name"]  #extract project name from the request
        description = data.get("description")  #extract the optional project description
        project = self.service.update_project(id, name, description)  #ask service layer to update the project
        return jsonify(project.__dict__), 200  #return updated Project object & return HTTP 200 (OK/Updated)


    #handle DELETE /projects/{id} requests
    def delete_project(self, id: int):
        self.service.delete_project(id)  #ask service layer to delete the project
        return jsonify({"message": "Project deleted"}), 200  #returning successful deletion JSON message with HTTP 200 (OK/Deleted)