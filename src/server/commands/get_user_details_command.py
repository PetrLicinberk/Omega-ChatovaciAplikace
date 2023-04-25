from src.server.commands import command
import src.server.user as u


class GetUserDetailsCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        if 'username' not in args:
            return
        user = u.get_user_by_username(args['username'])
        if user is not None:
            details = user.get_user_details()
            self._client.send('user_details', details)