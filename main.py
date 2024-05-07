from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
import socket

app = FastAPI()

ip_requests = {}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Get the client's IP address
    client_ip = request.client.host

    # Update the request count for the client's IP
    if client_ip in ip_requests:
        ip_requests[client_ip] += 1
    else:
        ip_requests[client_ip] = 1

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
        {"".join([f"<li>IP: {ip} - Requests: {count}</li>" for ip, count in ip_requests.items()])}
    </ul>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)