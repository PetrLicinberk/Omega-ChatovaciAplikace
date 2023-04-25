from src.client.commands.command import Command
from src.client.gui import login, panel

class LoginCommand(Command):
    def __init__(self, app):
        super().__init__(app)

    def execute(self, args):
        if args['err'] == 0:
            self._app.show_panel(panel.Panels.MAIN)
        else:
            if type(self._app._panel) == login.LoginPanel:
                self._app._panel.set_err_message('Špatné přihlašovací údaje.')