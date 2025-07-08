import socket
from core.router import handle_command

def run_px4_agent():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 5760))  # PX4 listens on this port

    print("[PX4Agent] Listening on 127.0.0.1:5760")

    while True:
        data, addr = sock.recvfrom(4096)
        try:
            decoded = data.decode()
            handle_command(decoded)
        except:
            continue
