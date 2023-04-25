from src.server.commands import command
import src.server.user as u

class GetMessagesCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        if 'user' not in args or self._client._user is None:
            self._client.send('messages', { 'msg': [] })
        user1 = self._client._user
        user2 = u.get_user_by_username(args['user'])
        if user2 is None:
            self._client.send('messages', { 'msg': [] })
        messages: list[u.Message] = u.get_messages(user1, user2)
        response = []
        for msg in messages:
            dict = {}
            dict['from'] = msg.get_from()
            dict['to'] = msg.get_to()
            dict['content'] = msg.get_content()
            dict['date'] = msg.get_date()
            response.append(dict)
        self._client.send('messages', { 'msg': response })