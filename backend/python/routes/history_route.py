import os

import requests
from flask import Blueprint, jsonify


GO_SERVICE_URL = os.getenv("GO_SERVICE_URL", "http://localhost:8080")

history_routes = Blueprint("history", __name__)


@history_routes.get("/history/endpoint/<int:endpoint_id>")
def get_execution_history(endpoint_id):
    try:
        response = requests.get(
            f"{GO_SERVICE_URL}/executions/endpoint/{endpoint_id}",
            timeout=5
        )

        return (
            response.content,
            response.status_code,
            {
                "Content-Type": response.headers.get(
                    "Content-Type",
                    "application/json"
                )
            }
        )

    except requests.RequestException as error:
        return jsonify({
            "error": "Execution history service unavailable.",
            "details": str(error)
        }), 502