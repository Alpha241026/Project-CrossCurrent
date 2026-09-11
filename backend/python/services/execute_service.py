import requests


#sends the completed execution record to the Go history service
def save_execution_to_go(execution):

    try:
        response = requests.post(
            "http://localhost:8080/executions",
            json=execution,
            timeout=2
        )

        #raise an exception if the Go service returns an error status
        response.raise_for_status()

    except requests.RequestException as error:
        #history persistence should not prevent a successful API request from reaching the frontend
        print("execution history persistence failed:", error)


#executes an HTTP request to target API and prepares its execution history record
def execute_request(endpoint_id, method, url, params, headers, body):

    params = params or {}
    headers = headers or {}

    #store the time taken by the external API request for execution history
    response = None

    try:

        if method == "GET": #sending GET request
            response = requests.get(
                url,
                params=params,
                headers=headers
            )

        elif method == "POST": #sending POST request with a JSON body
            response = requests.post(
                url,
                params=params,
                headers=headers,
                json=body
            )

        elif method == "PATCH": #sending PATCH request with a JSON body
            response = requests.patch(
                url,
                params=params,
                headers=headers,
                json=body
            )

        elif method == "DELETE": #sending DELETE request with an optional JSON body
            response = requests.delete(
                url,
                params=params,
                headers=headers,
                json=body
            )

        else:
            raise ValueError(f"unsupported HTTP method: {method}")

        try:
            res_body = response.json()
        except ValueError:
            #use the raw response text when the target API does not return JSON
            res_body = response.text

        #return only the data needed by the frontend
        result = {
            "status": response.status_code,
            "body": res_body
        }

        #prepare the completed request for permanent execution history
        execution = {
            "endpoint_id": endpoint_id,
            "status_code": response.status_code,
            "response_time": int(response.elapsed.total_seconds() * 1000),
            "response_headers": dict(response.headers),
            "response_body": res_body
        }

        #persist history separately so a Go service failure does not hide a successful API response
        save_execution_to_go(execution)

        return result

    except requests.RequestException as error:

        #prepare failed requests as execution history instead of losing the failure information
        execution = {
            "endpoint_id": endpoint_id,
            "status_code": None,
            "response_time": None,
            "response_headers": {},
            "response_body": None,
            "error_message": str(error)
        }

        #attempt to preserve failed request information in execution history
        save_execution_to_go(execution)

        return {
            "status": None,
            "body": None,
            "error": str(error)
        }