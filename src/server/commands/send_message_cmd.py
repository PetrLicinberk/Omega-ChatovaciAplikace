from src.server.commands import command
import src.server.user as u

class SendMessageCommand(command.Command):
    def __init__(self, client):
        super().__init__(client)

    def execute(self, args):
        to_user = args['to']
        msg_text = args['content']
        if len(msg_text) <= 2048:
            user = u.get_user_by_username(to_user)
            if self._client._user.is_friend(user.get_id()):
                u.send_message(self._client._user, user, msg_text)