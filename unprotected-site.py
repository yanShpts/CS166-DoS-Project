from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
import socket

app = FastAPI()

ip_requests = {}

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Get the client's IP address
    client_ip = request.client.host

    # Update the request count for the client's IP
    if client_ip in ip_requests:
        ip_requests[client_ip] += 1
    else:
        ip_requests[client_ip] = 1

    # Simulate a page load delay
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
        {"".join([f"<li>IP: {ip} - Requests: {count}</li>" for ip, count in ip_requests.items()])}
    </ul>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)