from src.server.commands import command

class DeclineFriendReqCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        if 'username' not in args:
            return
        self._client._user.decline_friend_req(args['username'])