import requests

#executes an HTTP request to target API
def execute_request(method,url,body):

    if method=="GET": #sending GET request
        response = requests.get(url)
    elif method == "POST": #sending POST request with a JSON body
        response = requests.post(url, json=body)
    
    #return only the data needed by the frontend
    return {
    "status": response.status_code,
    "body": response.json()
    }