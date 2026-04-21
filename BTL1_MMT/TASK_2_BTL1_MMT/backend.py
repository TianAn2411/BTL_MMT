import socket
import threading
from httpadapter import HttpAdapter

def handle_client(ip, port, conn, addr, routes):
    print(f"[Backend] connection from {addr}")
    adapter = HttpAdapter(ip, port, conn, addr, routes)
    adapter.handle_client(conn, addr, routes)

def run_backend(ip, port, routes):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(50)

    print(f"[Backend] running at {ip}:{port}")

    while True:
        conn, addr = server.accept()
        # TODO CODE threading

def create_backend(ip, port, routes={}):
    run_backend(ip, port, routes)