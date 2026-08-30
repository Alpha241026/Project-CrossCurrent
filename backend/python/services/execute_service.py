import requests

#executes an HTTP request to target API
def execute_request(method,url,params, headers,body):

    params = params or {}
    headers = headers or {}
    
    if method=="GET": #sending GET request
        response = requests.get(url, params=params, headers=headers)
    elif method == "POST": #sending POST request with a JSON body
        response = requests.post(url, params=params, headers=headers, json=body)
    elif method == "PATCH": #sending PATCH request with a JSON body
        response = requests.patch(url, params=params, headers=headers, json=body)
    elif method == "DELETE": #sedning DELETE request with a optional JSON body
        response = requests.delete(url, params=params, headers=headers, json=body)
    
    try :
        res_body = response.json()
    except ValueError:
        res_body = response.text
    #return only the data needed by the frontend
    return {
    "status": response.status_code,
    "body": res_body
    }