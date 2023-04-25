from src.client import config
from src.client import connection
import sys
import threading
import time
from src.client.gui import window, login, register, main_panel, find_user, invites_panel, my_profile_panel, \
                view_profile, edit_profile
from PyQt6 import QtWidgets, QtCore
from src.client.gui.panel import Panels, Panel
from src.client.commands import login_command, register_command

class ChatClient:
    def __init__(self):
        config.get_config().read('config/client.ini')
        self._server_ip = config.get_str('server', 'ip', '127.0.0.1')
        self._server_port = config.get_int('server', 'port', 65525)
        self._server = connection.Connection(self._server_ip, self._server_port)
        self._app = None
        self._window = None
        self._panel = None
        self._panels = None
        self._username = None
        self._is_running = False
        self._chat_username = None

    def get_window(self) -> window.Window:
        '''
        Returns window of the application.

        :return: window instance
        '''
        return self._window

    def run(self):
        '''
        Starts the application.
        '''
        self._app = QtWidgets.QApplication(sys.argv)
        self._panels = [
            login.LoginPanel(self),
            register.RegisterPanel(self),
            main_panel.MainWidget(self),
            find_user.FindUserWidget(self),
            invites_panel.InvitesPanel(self),
            my_profile_panel.MyProfilePanel(self),
            view_profile.ViewProfile(self),
            edit_profile.EditProfilePanel(self)
        ]

        try:
            self._server.connect()
            self._server.set_timeout(1000)
            pass
        except:
            err = QtWidgets.QMessageBox.critical(
                self._window,
                'Error',
                'Spojení se serverem se nezdařilo.',
                QtWidgets.QMessageBox.StandardButton.Ok
            )
        else:
            self._window = window.Window('Chat')
            self._is_running = True
            for panel in self._panels:
                self._window.add_panel(panel)

            self.show_panel(Panels.LOGIN)
            self._window.show()
            self._app.exec()

            self._is_running = False
            self._server.close()

    def show_panel(self, panel_id):
        '''
        Changes the displayed panel.
        '''
        panel: Panel = self._panels[panel_id]
        self._panel = panel
        panel.reset()
        self._window.setFixedSize(panel.size())
        self._window.change_panel(panel_id)