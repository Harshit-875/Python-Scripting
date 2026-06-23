import socket
import threading

def handle_client(client_socket, client_address):
    """
    Handle a client connection
    """
    print(f"Connection from {client_address}")
    
    # Receive HTTP request
    request = client_socket.recv(1024).decode()
    print(f"Request: {request}")
    
    # Parse request to get requested path
    try:
        path = request.split()[1]
    except:
        path = "/"
    
    # Simple routing
    if path == "/":
        response_body = "<h1>Welcome to my server!</h1>"
    elif path == "/hello":
        response_body = "<h1>Hello World!</h1>"
    else:
        response_body = "<h1>404 Not Found</h1>"
    
    # Prepare HTTP response
    response_headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html",
        f"Content-Length: {len(response_body)}",
        "Connection: close",
        "",
        ""
    ]
    response = "\r\n".join(response_headers) + response_body
    
    # Send response
    client_socket.send(response.encode())
    client_socket.close()

def start_server(host='localhost', port=8080):
    """
    Start the HTTP server
    """
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind and listen
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server running on http://{host}:{port}")
    
    # Main loop
    while True:
        client_socket, client_address = server_socket.accept()
        
        # Handle client in a new thread
        client_thread = threading.Thread(
            target=handle_client, 
            args=(client_socket, client_address)
        )
        client_thread.start()

# Start the server
start_server()