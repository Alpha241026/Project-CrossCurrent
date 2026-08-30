from flask import request, jsonify

from services.execute_service import execute_request

#receives request data from the frontend and delegates execution to the service
def execute():
    data = request.get_json() #read the JSON payload sent by the frontend
    
    #extract request details from the payload
    method = data.get("method")
    url = data.get("url")
    params = data.get("params")
    headers = data.get("headers")
    body = data.get("body")
    
    result = execute_request(method,url,params,headers,body) #let the service execute the HTTP request
    
    return jsonify(result) #return the service result back to the frontend as JSON
