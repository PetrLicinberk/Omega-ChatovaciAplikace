from src.server.commands import command

class GetFriendList(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        if self._client._user is None:
            return
        friends = self._client._user.get_friend_list()
        self._client.send('friend_list', { 'friends': friends })