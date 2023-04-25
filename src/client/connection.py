import socket
import json
import src.client.commands.command as command

class Connection:
    def __init__(self, server_ip: str, server_port: int):
        self._ip = server_ip
        self._port = server_port
        self._socket = None
        self._connected = False

    def connect(self):
        '''
        Connects to the server.
        '''
        self._socket = socket.socket()
        self._socket.connect((self._ip, self._port))
        self._connected = True

    def close(self):
        '''
        Closes the connection with the server.
        '''
        if self.is_connected():
            self._socket.close()
            self._socket = None
            self._connected = False

    def send(self, cmd_name: str, cmd_args: dict):
        '''
        Sends a command to the server

        :param cmd_name: command name
        :param cmd_args: command argumets
        '''
        data = command.to_json(cmd_name, cmd_args)
        self._socket.send(len(data).to_bytes(4, byteorder='big'))
        self._socket.send(bytes(data, 'utf-8'))

    def recv(self):
        '''
        Recieves command from the server.

        :return: command name and command args
        '''
        cmd_name = None
        cmd_args = {}
        size = self._socket.recv(4)
        if size:
            cmd = self._socket.recv(int.from_bytes(size, byteorder='big'))
            cmd = cmd.decode('utf-8')
            cmd_name, cmd_args = command.from_json(cmd)
        return cmd_name, cmd_args
    
    def is_connected(self) -> bool:
        '''
        Checked if the application is connected to the server.
        '''
        return self._connected
    
    def set_timeout(self, timeout):
        '''
        Sets the socket's timeout.
        '''
        self._socket.settimeout(timeout / 1000)
