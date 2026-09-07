from services.endpoint_service import EndpointService
from flask import request, jsonify


class EndpointController:
    #receive the EndpointService object (dependency injection)
    def __init__(self, service: EndpointService):
        self.service = service


    #handle POST /projects/{project_id}/endpoints requests
    def create_endpoint(self, project_id: int):
        data = request.get_json()  #read JSON body sent by the frontend
        name = data["name"]  #extract the endpoint name from the request
        method = data["method"]  #extract the method from the request
        url = data["url"]  #extract the url from the request
        description = data.get("description")  #extract the optional endpoint description
        params = data.get("params")  #extract the params from the request the safer way in case its None
        headers = data.get("headers")  #extract the headers from the request the safer way in case its None
        body = data.get("body")  #extract the body from the request the safer way in case its None

        endpoint = self.service.create_endpoint(
            project_id,
            name,
            method,
            url,
            description,
            params,
            headers,
            body
        )  #ask service layer to create the endpoint

        return jsonify(endpoint.__dict__), 201  #convert Endpoint object to JSON & return HTTP 201 (Created)


    #handle GET /projects/{project_id}/endpoints requests
    def get_endpoints(self, project_id):
        endpoints = self.service.get_endpoints(project_id)  #ask service layer for endpoints belonging to this project
        eplist = []  #convert Endpoint objects into dictionaries for JSON serialization

        for ep in endpoints:
            eplist.append(ep.__dict__)

        return jsonify(eplist), 200  #return the endpoint list as JSON with HTTP 200 (OK)


    #handle GET /endpoints/{endpoint_id} requests
    def get_endpoint_by_id(self, endpoint_id: int):
        endpoint = self.service.get_endpoint_by_id(endpoint_id)  #ask service layer for this endpoint
        return jsonify(endpoint.__dict__), 200  #return single Endpoint object with HTTP 200 (OK)


    #handle PATCH /endpoints/{endpoint_id} requests
    def update_endpoint(self, endpoint_id: int):
        data = request.get_json()  #read JSON body sent by frontend
        name = data["name"]  #extract endpoint name from the request
        method = data["method"]  #extract the method from the request
        url = data["url"]  #extract the url from the request
        description = data.get("description")  #extract the optional endpoint description
        params = data.get("params")  #extract the params from the request the safer way in case its None
        headers = data.get("headers")  #extract the headers from the request the safer way in case its None
        body = data.get("body")  #extract the body from the request the safer way in case its None

        endpoint = self.service.update_endpoint(
            endpoint_id,
            name,
            method,
            url,
            description,
            params,
            headers,
            body
        )  #ask service layer to update the endpoint

        return jsonify(endpoint.__dict__), 200  #return updated Endpoint object & return HTTP 200 (OK/Updated)


    #handle DELETE /endpoints/{endpoint_id} requests
    def delete_endpoint(self, endpoint_id: int):
        self.service.delete_endpoint(endpoint_id)  #ask service layer to delete the endpoint
        return jsonify({"message": "Endpoint deleted"}), 200  #returning successful deletion JSON message with HTTP 200 (OK/Deleted)