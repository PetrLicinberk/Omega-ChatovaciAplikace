from src.server.commands import command
from src.server import user
from src.server import db_connection as db

class CreateUserCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        if 'username' not in args or 'password' not in args:
            return
        new_user = user.User()

        try:
            new_user.set_username(args['username'])
            new_user.set_password(args['password'])
        except:
            self._client.send('register', { 'err': 1 })
            return

        if user.does_exist(new_user):
            self._client.send('register', { 'err': 2 })
            return
        new_user.save()
        self._client._user = new_user
        self._client.send('register', { 'err': 0 })