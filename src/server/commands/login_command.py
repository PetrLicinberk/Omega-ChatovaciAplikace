import src.server.user as u
from src.server.commands import command

class LoginCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        if 'username' not in args or 'password' not in args:
            return
        user, status = u.verify_login(args['username'], args['password'])
        self._client.send('login', { 'err': status })
        if status == 0:
            self._client._user = user