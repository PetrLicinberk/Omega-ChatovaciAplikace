from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from src.client.gui import window
from src.client.gui.panel import Panels, Panel
from src.client.commands import login_command
import time

class LoginPanel(Panel):
    def __init__(self, app) -> None:
        super().__init__()
        self.setStyleSheet('padding: 5px; font-size: 15px;')
        self._app = app
        self.setFixedSize(400, 250)

        self._layout = QtWidgets.QGridLayout()

        self._title = QtWidgets.QLabel('Přihášení')
        self._title.setStyleSheet('font-size: 40px;')

        self._username = QtWidgets.QLineEdit()
        self._username.setMaxLength(64)
        self._username.setPlaceholderText('Uživatelské jméno')
        self._username.setFixedWidth(250)
        self._username.textChanged
        
        self._password = QtWidgets.QLineEdit()
        self._password.setMaxLength(64)
        self._password.setPlaceholderText('Heslo')
        self._password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self._password.setFixedWidth(250)

        self._login_btn = QtWidgets.QPushButton('Přihlásit')
        self._login_btn.setFixedWidth(125)
        self._login_btn.setStyleSheet('padding: 7px 0px;')
        self._login_btn.clicked.connect(self.login_clicked)
        self._login_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._register_btn = QtWidgets.QPushButton('Registrace')
        self._register_btn.setFixedWidth(125)
        self._register_btn.setStyleSheet('padding: 7px 0px;')
        self._register_btn.clicked.connect(self.register_clicked)
        self._register_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._err_message = QtWidgets.QLabel('')
        self._err_message.setStyleSheet('color: red;')

        self._layout.addWidget(self._title, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._username, 1, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._password, 2, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._err_message, 3, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._login_btn, 4, 0, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        self._layout.addWidget(self._register_btn, 4, 1, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self._layout)

    def reset(self):
        '''
        Resets values to default.
        '''
        self._username.setText('')
        self._password.setText('')
        self._err_message.setText('')

    def register_clicked(self):
        '''
        Method called when the register button is clicked.
        Changes the panel to REGISTER.
        '''
        self._app.show_panel(Panels.REGISTER)

    def login_clicked(self):
        '''
        Method called when the login button is clicked.
        Logs in the user and sends the command to the server.
        '''
        username = self._username.text()
        password = self._password.text()
        self._app._server.send('login_user', { 'username': username, 'password': password })
        self._app._username = username
        cmd = None
        args = None
        while cmd is None:
            try:
                cmd, args = self._app._server.recv()
            except:
                break
            if cmd != 'login':
                cmd = None
                args = None
        login_cmd = login_command.LoginCommand(self._app)
        if cmd == 'login':
            login_cmd.execute(args)
        else:
            login_cmd.execute({ 'err': 1 })

    def set_err_message(self, message):
        '''
        Sets the displayed error message.

        :param message: error message
        '''
        self._err_message.setText(message)