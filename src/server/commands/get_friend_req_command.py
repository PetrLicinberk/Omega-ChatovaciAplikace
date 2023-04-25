from src.server.commands import command

class GetFriendReqCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        if self._client._user is not None:
            requests = self._client._user.get_friend_req()
            self._client.send('friend_req', { 'req': requests })