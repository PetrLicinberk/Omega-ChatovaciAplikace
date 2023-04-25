from src.server.commands import command
from src.server import user

class FindUsersCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        if 'username' not in args:
            return
        username = args['username']
        users = user.get_all_users_by_name(username, self._client._user)
        self._client.send('find_users', { 'users': users })