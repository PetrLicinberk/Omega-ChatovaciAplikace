from src.server.commands import command

class AddFrienCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        username = args['username']
        self._client._user.add_friend(username)