from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
import socket
import uvicorn
import time

app = FastAPI()
ip_requests = {}
rate_limit = 5  # maximum number of requests allowed per time_window
time_window = 10  # window in seconds

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # get the client's IP address
    client_ip = request.client.host

    # check if client has exceeded the rate limit
    current_time = time.time()
    if client_ip in ip_requests:
        requests_in_window = [t for t in ip_requests[client_ip] if t > current_time - time_window]
        if len(requests_in_window) >= rate_limit:
            return HTMLResponse(content="Too many requests from your IP. Please try again later.", status_code=429)
    else:
        ip_requests[client_ip] = []

    # update the request count and timestamp for the client's IP
    ip_requests[client_ip].append(current_time)

    # simulate a page load delay
    fibonacci(23)

    # Get the hostname of the server
    hostname = socket.gethostname()

    # Render the HTML template with the IP requests data
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>IP Requests Tracker</title>
</head>
<body>
    <h1>IP Requests Tracker</h1>
    <p>Server Hostname: {hostname}</p>
    <h2>IP Requests:</h2>
    <ul>
        {"".join([f"<li>IP: {ip} - Requests: {len(requests)}</li>" for ip, requests in ip_requests.items()])}
    </ul>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)