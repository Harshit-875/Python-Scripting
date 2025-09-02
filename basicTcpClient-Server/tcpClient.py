import socket

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect(('localhost', 12345))  # Also uses a tuple here

# Send data
message = "Hello from client!"
client_socket.send(message.encode())

# Receive response
response = client_socket.recv(1024).decode()
print(f"Server response: {response}")

# Close the connection
client_socket.close()