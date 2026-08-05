from flask import Flask
from repositories.project_repo import ProjectRepository
from services.project_service import ProjectService
from controllers.project_controller import ProjectController

from routes.project_route import register_project_routes

from routes.execute_route import execute_bp
from routes.execute_route import register_execute_routes

app = Flask(__name__)

#build the dependency chain
repo = ProjectRepository()
service = ProjectService(repo)
controller = ProjectController(service)

register_project_routes(app,controller) # register all project route
register_execute_routes(app) #register route for executing POST requests

if __name__=="__main__":
    app.run(host="127.0.0.1",port=5000,debug=True) #start the development server