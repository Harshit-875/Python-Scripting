import socket

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to address and port - FIXED: using a tuple (host, port)
server_socket.bind(('localhost', 12345))

# Listen for connections (max 5 queued connections)
server_socket.listen(5)
print("Server listening on port 12345...")

while True:
    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    
    # Receive data from client
    data = client_socket.recv(1024).decode()
    print(f"Received: {data}")
    
    # Send response
    client_socket.send("Hello from server!".encode())
    
    # Close the connection
    client_socket.close()