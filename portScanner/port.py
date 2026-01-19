import socket
import threading
from queue import Queue

def port_scan(target, port):
    """
    Attempt to connect to a port on the target
    """
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        
        # Attempt connection
        result = sock.connect_ex((target, port))
        
        if result == 0:
            print(f"Port {port} is open")
            
            # Try to grab banner if port is open
            try:
                banner = sock.recv(1024).decode().strip()
                if banner:
                    print(f"  Banner: {banner}")
            except:
                pass
                
        sock.close()
    except Exception as e:
        pass

def threader():
    """
    Worker function for threading
    """
    while True:
        worker = q.get()
        port_scan(target, worker)
        q.task_done()

# Main code
target = "scan.nmap.org"  # Change this to your target
q = Queue()

# Create and start threads
for x in range(100):  # Number of threads
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# Queue ports to scan
for worker in range(1, 1025):  # Scan ports 1-1024
    q.put(worker)

# Wait for all threads to complete
q.join()
print("Scan completed!")