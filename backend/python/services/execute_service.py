import ipaddress
import os
import socket
from urllib.parse import urlparse
import requests

GO_SERVICE_URL = os.getenv("GO_SERVICE_URL", "http://localhost:8080")

def is_safe_target_url(url):
    try:
        parsed = urlparse(url)

        # Only allow normal HTTP(S) requests.
        if parsed.scheme not in ("http", "https"):
            return False

        # A hostname is required.
        hostname = parsed.hostname

        if not hostname:
            return False

        hostname = hostname.lower()

        # Block obvious local hostnames.
        blocked_hostnames = {
            "localhost",
            "localhost.localdomain",
            "ip6-localhost",
            "ip6-loopback",
        }

        if hostname in blocked_hostnames or hostname.endswith(".localhost"):
            return False

        # If the hostname itself is an IP address, inspect it directly.
        try:
            ip = ipaddress.ip_address(hostname)

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_multicast
                or ip.is_reserved
                or ip.is_unspecified
            ):
                return False

            return True

        except ValueError:
            # It's a hostname rather than an IP address.
            pass

        # Resolve the hostname and make sure none of its addresses
        # point to an internal/local network.
        addresses = socket.getaddrinfo(
            hostname,
            parsed.port or (443 if parsed.scheme == "https" else 80),
            type=socket.SOCK_STREAM,
        )

        for address in addresses:
            resolved_ip = ipaddress.ip_address(address[4][0])

            if (
                resolved_ip.is_private
                or resolved_ip.is_loopback
                or resolved_ip.is_link_local
                or resolved_ip.is_multicast
                or resolved_ip.is_reserved
                or resolved_ip.is_unspecified
            ):
                return False

        return True

    except (ValueError, socket.gaierror, OSError):
        return False


#sends the completed execution record to the Go history service
def save_execution_to_go(execution):

    try:
        response = requests.post(
            f"{GO_SERVICE_URL}/executions",
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

    if not is_safe_target_url(url):
            return {
                "status": None,
                "body": None,
                "error": "Target URL is not allowed."
            }

    #store the time taken by the external API request for execution history
    response = None

    try:

        if method == "GET": #sending GET request
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=15,
                allow_redirects=False
            )

        elif method == "POST": #sending POST request with a JSON body
            response = requests.post(
                url,
                params=params,
                headers=headers,
                json=body,
                timeout=15,
                allow_redirects=False
            )

        elif method == "PATCH": #sending PATCH request with a JSON body
            response = requests.patch(
                url,
                params=params,
                headers=headers,
                json=body,
                timeout=15,
                allow_redirects=False
            )

        elif method == "DELETE": #sending DELETE request with an optional JSON body
            response = requests.delete(
                url,
                params=params,
                headers=headers,
                json=body,
                timeout=15,
                allow_redirects=False
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