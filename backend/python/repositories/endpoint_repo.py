from models.endpoint import Endpoint #importing Endpoint type model from models/endpoint.py

class EndpointRepository: #stores Endpoint objects in memory
    def __init__(self):
        self.endpoints = [] #attaching endpoints list attribute to objects / in-memory storage
        
    def create_endpoint(self, endpoint: Endpoint): #method for creating/appending new project of type Endpoint
        self.endpoints.append(endpoint)
        
    def get_endpoints(self) -> list[Endpoint]: #method for internal id generation in service layer
        return self.endpoints

    def get_endpoint_by_id(self, endpoint_id: int) -> Endpoint | None: #method for returning a single endpoint from the list...None if not found
        for endpoint in self.endpoints:
            if endpoint.id==endpoint_id:
                return endpoint
        return None
    
    def get_endpoints_by_project(self, project_id: int) -> list[Endpoint]: #method for returning list of existing endpoints
        project_endpoints = []
        for endpoint in self.endpoints:
            if endpoint.project_id==project_id:
                project_endpoints.append(endpoint)
        return project_endpoints
    
    def update_endpoint(self, endpoint_id: int, endpoint: Endpoint): #method for updating an endpoint
        for index,ep in enumerate(self.endpoints):
            if(ep.id==endpoint_id):
                self.endpoints[index]=endpoint
        return None
    
    def delete_endpoint(self, endpoint_id: int): #method for deleting an endpoint
        for endpoint in self.endpoints:
            if endpoint.id==endpoint_id:
                self.endpoints.remove(endpoint)
        return None 
    
    def delete_endpoints_by_project(self, project_id: int): #method for deleting all endpoints of a project (by filtering to include every other project endpoint than those of the one being deleted)
        self.endpoints = [
            endpoint
            for endpoint in self.endpoints
            if endpoint.project_id != project_id
        ]
