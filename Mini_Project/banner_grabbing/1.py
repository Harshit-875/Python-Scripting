import socket

def grab_banner(target, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    try:
        sock.connect((target, port))

        request = (
    f"HEAD / HTTP/1.1\r\n"
    f"Host: {target}\r\n"
    f"Connection: close\r\n\r\n"
)
        sock.sendall(request.encode())

        banner = b""

        while True:
            try:
                chunk = sock.recv(1024)

                if not chunk:
                    break

                banner += chunk

            except socket.timeout:
                break

        return banner.decode("utf-8", errors="ignore")

    except Exception as e:
        return f"Error: {e}"

    finally:
        sock.close()


print(grab_banner("example.com", 23))