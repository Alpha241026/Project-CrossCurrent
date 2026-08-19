from flask import Blueprint
from controllers.endpoint_controller import EndpointController


#register all endpoint-related routes with the Flask app
def register_endpoint_routes(app, controller: EndpointController):

    #blueprint groups all endpoint routes together
    endpoint_routes = Blueprint("endpoints", __name__)

    #forward POST /projects/{project_id}/endpoints to the controller
    @endpoint_routes.post("/projects/<int:project_id>/endpoints")
    def create_endpoint(project_id):
        return controller.create_endpoint(project_id)

    #forward GET /projects/{project_id}/endpoints to the controller
    @endpoint_routes.get("/projects/<int:project_id>/endpoints")
    def get_endpoints(project_id):
        return controller.get_endpoints(project_id)

    #forward GET /endpoints/{endpoint_id} to the controller
    @endpoint_routes.get("/endpoints/<int:endpoint_id>")
    def get_endpoint_by_id(endpoint_id):
        return controller.get_endpoint_by_id(endpoint_id)

    #forward PATCH /endpoints/{endpoint_id} to the controller
    @endpoint_routes.patch("/endpoints/<int:endpoint_id>")
    def update_endpoint(endpoint_id):
        return controller.update_endpoint(endpoint_id)

    #forward DELETE /endpoints/{endpoint_id} to the controller
    @endpoint_routes.delete("/endpoints/<int:endpoint_id>")
    def delete_endpoint(endpoint_id):
        return controller.delete_endpoint(endpoint_id)

    #attach this blueprint to the Flask application
    app.register_blueprint(endpoint_routes)