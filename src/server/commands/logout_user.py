from src.server.commands import command

class LogoutUser(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        self._client._user = None