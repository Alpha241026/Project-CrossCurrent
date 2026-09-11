from flask import request, jsonify

from services.execute_service import execute_request


#receives request data from the frontend and delegates execution to the service
def execute():
    data = request.get_json() #read the JSON payload sent from the frontend

    #extract request details from the payload
    endpoint_id = data.get("endpoint_id")
    method = data.get("method")
    url = data.get("url")
    params = data.get("params")
    headers = data.get("headers")
    body = data.get("body")

    #let the service execute the HTTP request and save its execution history
    result = execute_request(
        endpoint_id,
        method,
        url,
        params,
        headers,
        body
    )

    return jsonify(result) #return the service result back to the frontend as JSON