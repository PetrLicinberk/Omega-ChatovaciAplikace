import socket as socket
import re
import json
from src.server import user
from src.server.commands import command
from src.server.commands import create_user_command as create_user
from src.server.commands import login_command, logout_user, friend_list_cmd, send_message_cmd, \
                     get_messages_command, find_users_command, add_friend_command, \
                     get_friend_req_command, accept_friend_req_command, decline_friend_req_command, \
                     get_user_details_command, save_details_command, remove_friend_command, \
                     delete_user_command


class Client:
    def __init__(self, client_socket: socket.socket, ip_addr: tuple):
        '''
        Creates client instance with given socket and ip address

        :param client_socket: socket to witch the client is connected to
        :param ip_addr: clients ip address
        '''
        self._socket: socket.socket = client_socket
        self._ip_addr: tuple = ip_addr
        self._commands: dict[str, command.Command] = {
            'create_user': create_user.CreateUserCommand(self),
            'login_user': login_command.LoginCommand(self),
            'logout_user': logout_user.LogoutUser(self),
            'get_friend_list': friend_list_cmd.GetFriendList(self),
            'send_message': send_message_cmd.SendMessageCommand(self),
            'get_messages': get_messages_command.GetMessagesCommand(self),
            'find_users': find_users_command.FindUsersCommand(self),
            'add_friend': add_friend_command.AddFrienCommand(self),
            'get_invites': get_friend_req_command.GetFriendReqCommand(self),
            'accept_friend_req': accept_friend_req_command.AcceptFriendReqCommand(self),
            'decline_friend_req': decline_friend_req_command.DeclineFriendReqCommand(self),
            'get_details': get_user_details_command.GetUserDetailsCommand(self),
            'save_details': save_details_command.SaveDetailsCommand(self),
            'remove_friend': remove_friend_command.RemoveFriendCommand(self),
            'delete_user': delete_user_command.DeleteUserCommand(self)
        }
        self._user: user.User = None

    def handle_client(self):
        '''
        Method that handles client commands.
        '''
        try:
            while True:
                size = self._socket.recv(4)
                if not size:
                    break
                cmd = self._socket.recv(int.from_bytes(size, byteorder='big'))
                cmd = cmd.decode('utf-8')
                cmd_name, cmd_args = command.from_json(cmd)
                if cmd_name in self._commands:
                    self._commands[cmd_name].execute(cmd_args)
        except ConnectionResetError:
            pass
        except ConnectionAbortedError:
            pass

    def send(self, cmd_name: str, cmd_args: dict):
        '''
        Sends command to the client.

        :param cmd_name: command name
        :param cmd_args: command arguments
        '''
        try:
            data = command.to_json(cmd_name, cmd_args)
            self._socket.send(len(data).to_bytes(4, byteorder='big'))
            self._socket.send(bytes(data, 'utf-8'))
        except:
            pass

    def disconnect(self):
        '''
        Disconnects the client from the server.
        '''
        self._socket.close()