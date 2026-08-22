import requests

#executes an HTTP request to target API
def execute_request(method,url,body):

    if method=="GET": #sending GET request
        response = requests.get(url)
    elif method == "POST": #sending POST request with a JSON body
        response = requests.post(url, json=body)
    elif method == "PATCH": #sending PATCH request with a JSON body
        response = requests.patch(url, json=body)
    elif method == "DELETE": #sedning DELETE request with a optional JSON body
        response = requests.delete(url, json=body)
    
    try :
        res_body = response.json()
    except ValueError:
        res_body = response.text
    #return only the data needed by the frontend
    return {
    "status": response.status_code,
    "body": res_body
    }