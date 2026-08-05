from flask import Blueprint

from controllers.execute_controller import execute

#blueprint for request execution routes
execute_bp = Blueprint("execute", __name__)

#route for executing http requests
@execute_bp.route("/execute",methods=["POST"])
def execute_route():
    return execute() #forward the request to the controller

def register_execute_routes(app):
    app.register_blueprint(execute_bp) #registration helper for app.py