from flask import Flask

from repositories.project_repo import ProjectRepository
from repositories.endpoint_repo import EndpointRepository

from services.project_service import ProjectService
from services.endpoint_service import EndpointService

from controllers.project_controller import ProjectController
from controllers.endpoint_controller import EndpointController

from routes.project_route import register_project_routes
from routes.endpoint_route import register_endpoint_routes
from routes.execute_route import register_execute_routes


app = Flask(__name__)  #create Flask application instance


#build repository objects
project_repo = ProjectRepository()
endpoint_repo = EndpointRepository()


#build service objects and inject their repository dependencies
project_service = ProjectService(project_repo, endpoint_repo)
endpoint_service = EndpointService(project_repo, endpoint_repo)


#build controller objects and inject their service dependencies
project_controller = ProjectController(project_service)
endpoint_controller = EndpointController(endpoint_service)


#register application routes
register_project_routes(app, project_controller)
register_endpoint_routes(app, endpoint_controller)
register_execute_routes(app)  #register route for executing POST requests


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)  #start the development server