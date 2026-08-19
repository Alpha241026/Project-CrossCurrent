from repositories.project_repo import ProjectRepository
from models.endpoint import Endpoint
from repositories.endpoint_repo import EndpointRepository


class EndpointService:

    #receive the repository objects and keep using the same ones
    def __init__(self, pro_repo: ProjectRepository, repo: EndpointRepository):
        self.repository = repo
        self.project_repository = pro_repo


    #business logic for creating an endpoint
    def create_endpoint(self, project_id: int, name: str, method: str, url: str, body: dict | None) -> Endpoint:

        #reject empty or whitespace-only endpoint names
        if name.strip() == "":
            raise ValueError("Endpoint name cannot be empty")

        #reject empty or whitespace-only URLs
        if url.strip() == "":
            raise ValueError("URL cannot be empty")

        #allow only HTTP methods currently supported by Chimera
        if method not in ["GET", "POST"]:
            raise ValueError("Unsupported HTTP method")

        #check whether the parent project exists
        existing_pro = self.project_repository.get_project_by_id(project_id)

        #reject endpoint creation for a nonexistent project
        if existing_pro is None:
            raise ValueError("Project doesn't exist")

        #get existing endpoints to generate a new global ID
        existing_endpoints = self.repository.get_endpoints()

        #generate the next endpoint ID
        new_id = max((endpoint.id for endpoint in existing_endpoints), default=0) + 1

        #create the Endpoint object
        endpoint = Endpoint(
            id=new_id,
            project_id=project_id,
            name=name,
            method=method,
            url=url,
            body=body
        )

        #ask the repository to store the endpoint
        self.repository.create_endpoint(endpoint)

        #return the created endpoint
        return endpoint


    #return all endpoints belonging to a project
    def get_endpoints(self, project_id: int) -> list[Endpoint]:
        return self.repository.get_endpoints_by_project(project_id)


    #return one endpoint by its ID
    def get_endpoint_by_id(self, endpoint_id: int) -> Endpoint:

        #ask the repository to find the endpoint
        endpoint = self.repository.get_endpoint_by_id(endpoint_id)

        #reject requests for nonexistent endpoints
        if endpoint is None:
            raise ValueError("Endpoint doesn't exist")

        #return the found endpoint
        return endpoint


    #business logic for updating an existing endpoint
    def update_endpoint(self, endpoint_id: int, name: str, method: str, url: str, body: dict | None) -> Endpoint:

        #reject empty or whitespace-only endpoint names
        if name.strip() == "":
            raise ValueError("Endpoint name cannot be empty")

        #reject empty or whitespace-only URLs
        if url.strip() == "":
            raise ValueError("URL cannot be empty")

        #allow only HTTP methods currently supported by Chimera
        if method not in ["GET", "POST"]:
            raise ValueError("Unsupported HTTP method")

        #find the existing endpoint
        existing_endpoint = self.repository.get_endpoint_by_id(endpoint_id)

        #reject updates for nonexistent endpoints
        if existing_endpoint is None:
            raise ValueError("Endpoint doesn't exist")

        #create the updated Endpoint object while preserving its project
        endpoint = Endpoint(
            id=endpoint_id,
            project_id=existing_endpoint.project_id,
            name=name,
            method=method,
            url=url,
            body=body
        )

        #replace the existing endpoint in the repository
        self.repository.update_endpoint(endpoint_id, endpoint)

        #return the updated endpoint
        return endpoint


    #business logic for deleting an existing endpoint
    def delete_endpoint(self, endpoint_id: int):

        #find the existing endpoint
        existing_endpoint = self.repository.get_endpoint_by_id(endpoint_id)

        #reject deletion of a nonexistent endpoint
        if existing_endpoint is None:
            raise ValueError("Endpoint doesn't exist")

        #remove the endpoint from the repository
        self.repository.delete_endpoint(endpoint_id)