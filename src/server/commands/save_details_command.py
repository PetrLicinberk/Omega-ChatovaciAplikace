from src.server.commands import command


class SaveDetailsCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        if self._client._user is None:
            return
        self._client._user.update_details(args['first_name'], args['last_name'], args['email'])