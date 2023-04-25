from src.client.commands.command import Command
from src.client.gui import register
from src.client.gui.panel import Panels

class RegisterCommand(Command):
    def __init__(self, app):
        super().__init__(app)

    def execute(self, args):
        if type(self._app._panel) == register.RegisterPanel:
            if args['err'] == 2:
                self._app._username = None
                self._app._panel._username.setStyleSheet('color: red;')
                self._app._panel._err_message.setText('Toto uživatelské jméno není volné.')
            elif args['err'] == 1:
                self._app._username = None
                self._app._panel._err_message.setText('Při registraci nastala chyba.')
            elif args['err'] == 0:
                self._app.show_panel(Panels.MAIN)