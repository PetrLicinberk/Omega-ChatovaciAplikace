from src.server.commands import command
from src.server import user


class DeleteUserCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        if self._client._user is None:
            return
        user.delete_user(self._client._user)
        self._client._user = None