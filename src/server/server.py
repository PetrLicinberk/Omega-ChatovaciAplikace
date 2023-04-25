import socket
import threading

from src.server import client

class Server:
    def __init__(self, ip_addr: str, port: int, timeout: int = 100):
        self._ip_addr = ip_addr
        self._port = port
        self._timeout = timeout
        self._clients: list[client.Client] = []
        self._socket = None
        self._running = False

    def start(self):
        '''
        Starts the server and server loop.
        '''
        self._socket = socket.socket()
        self._socket.bind((self._ip_addr, self._port))
        self._socket.settimeout(self._timeout / 1000)
        self._socket.listen()
        self._running = True
        self.loop()

    def stop(self):
        '''
        Stops the server
        '''
        self._running = False

    def loop(self):
        '''
        Server loop handling new connections.
        '''
        while self._running:
            try:
                client_socket, client_ip_addr = self._socket.accept()
                new_client = client.Client(client_socket, client_ip_addr)
                self._clients.append(new_client)
                thread = threading.Thread(target=new_client.handle_client)
                thread.start()
            except:
                pass
        for c in self._clients:
            c.disconnect()
        self._socket.close()