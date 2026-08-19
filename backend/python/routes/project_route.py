from flask import Blueprint
from controllers.project_controller import ProjectController


#register all project-related routes with the Flask app
def register_project_routes(app, controller: ProjectController):

    #blueprint groups all project routes together
    project_routes = Blueprint("projects", __name__)

    #forward POST /projects to the controller
    @project_routes.post("/projects")
    def create_project():
        return controller.create_project()

    #forward GET /projects to the controller
    @project_routes.get("/projects")
    def get_projects():
        return controller.get_projects()

    #forward PATCH /projects/{id} to the controller
    @project_routes.patch("/projects/<int:id>")
    def update_project(id):
        return controller.update_project(id)

    #forward DELETE /projects/{id} to the controller
    @project_routes.delete("/projects/<int:id>")
    def delete_project(id):
        return controller.delete_project(id)

    #attach this blueprint to the Flask application
    app.register_blueprint(project_routes)