from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from src.client.gui import window
from src.client.gui.panel import Panels, Panel
from src.client.commands.register_command import RegisterCommand
import re

class RegisterPanel(Panel):
    def __init__(self, app) -> None:
        super().__init__()
        self.setStyleSheet('padding: 5px; font-size: 15px;')
        self._app = app
        self.setFixedSize(400, 350)

        self._layout = QtWidgets.QGridLayout()

        self._title = QtWidgets.QLabel('Registrace')
        self._title.setStyleSheet('font-size: 40px;')

        self._username = QtWidgets.QLineEdit()
        self._username.setMaxLength(64)
        self._username.setPlaceholderText('Uživatelské jméno')
        self._username.setFixedWidth(250)
        self._username.textChanged.connect(self.username_changed)
        
        self._password = QtWidgets.QLineEdit()
        self._password.setMaxLength(64)
        self._password.setPlaceholderText('Heslo')
        self._password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self._password.setFixedWidth(250)
        self._password.textChanged.connect(self.password_changed)

        self._retype_password = QtWidgets.QLineEdit()
        self._retype_password.setMaxLength(64)
        self._retype_password.setPlaceholderText('Heslo znovu')
        self._retype_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self._retype_password.setFixedWidth(250)
        self._retype_password.textChanged.connect(self.retype_password_changed)

        self._err_message = QtWidgets.QLabel('')
        self._err_message.setStyleSheet('color: red;')

        self._register_btn = QtWidgets.QPushButton('Registrovat')
        self._register_btn.setFixedWidth(125)
        self._register_btn.setStyleSheet('padding: 7px 0px;')
        self._register_btn.clicked.connect(self.register_clicked)
        self._register_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._cancel_btn = QtWidgets.QPushButton('Zpět')
        self._cancel_btn.setFixedWidth(125)
        self._cancel_btn.setStyleSheet('padding: 7px 0px;')
        self._cancel_btn.clicked.connect(self.cancel_clicked)
        self._cancel_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._layout.addWidget(self._title, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._username, 1, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._password, 2, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._retype_password, 3, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._err_message, 4, 0, 2, 2, Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._register_btn, 6, 0, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        self._layout.addWidget(self._cancel_btn, 6, 1, 1, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self._layout)
        self.adjustSize()

    def reset(self):
        '''
        Resets values to default.
        '''
        self._username.setText('')
        self._username.setStyleSheet('')
        self._password.setText('')
        self._password.setStyleSheet('')
        self._retype_password.setText('')
        self._retype_password.setStyleSheet('')
        self._err_message.setText('')

    def register_clicked(self):
        '''
        Method called when register button is clicked.
        Validates the username and password.
        Sends register command to the server.
        '''
        username = self._username.text()
        password = self._password.text()

        self._username.setStyleSheet('')
        self._password.setStyleSheet('')
        self._retype_password.setStyleSheet('')
        self._err_message.setText('')
        if self.validate_username() and self.validate_password and self.validate_retype_password():
            self._app._server.send('create_user', { 'username': username, 'password': password })
            self._app._username = username
            cmd = None
            args = None
            while cmd is None:
                try:
                    cmd, args = self._app._server.recv()
                except:
                    break
                if cmd != 'register':
                    cmd = None
                    args = None
            register_cmd = RegisterCommand(self._app)
            if cmd == 'register':
                register_cmd.execute(args)
            else:
                register_cmd.execute({ 'err': 1 })

    def cancel_clicked(self):
        '''
        Method called when the cancel button is clicked.
        Displays the LOGIN panel.
        '''
        self._app.show_panel(Panels.LOGIN)

    def username_changed(self):
        '''
        Method called when the username input changed.
        Validates the username.
        '''
        self.validate_username()

    def password_changed(self):
        '''
        Method called when the password input chaned.
        Validates the password entered and checks wether the two passwords match.
        '''
        self.validate_retype_password()
        self.validate_password()

    def retype_password_changed(self):
        '''
        Method called when the retype password input chaned.
        Checks wether the two passwords match.
        '''
        self.validate_retype_password()

    def validate_username(self):
        '''
        Checks if the username is 3 - 64 characters long
        and contains only allowed characters.
        '''
        username = self._username.text()
        if re.search(r'^[a-z0-9_-]*$', username, re.IGNORECASE) is None:
            self._username.setStyleSheet('color: red;')
            self._err_message.setText('Uživatelské jméno může obsahovat pouze\nmalá a velká písmena a čísla.')
        elif len(username) < 3 or len(username) > 64:
            self._username.setStyleSheet('color: red;')
            self._err_message.setText('Uživatelské jméno musí být dlouhé\n 3 - 64 znaků')
        else:
            self._username.setStyleSheet('')
            self._err_message.setText('')
            return True
        return False
    
    def validate_password(self):
        '''
        Checks if the password is 4 - 64 characters long
        and contains al least one lower case letter,
        one upper case letter and one number.
        '''
        password = self._password.text()
        if re.search(r'[a-z]', password) is None:
            self._password.setStyleSheet('color: red;')
            self._err_message.setText('Heslo musí obsahovat alespoň jedno\nmalé písmeno.')
        elif re.search(r'[A-Z]', password) is None:
            self._password.setStyleSheet('color: red;')
            self._err_message.setText('Heslo musí obsahovat alespoň jedno\nvelké písmeno.')
        elif re.search(r'[0-9]', password) is None:
            self._password.setStyleSheet('color: red;')
            self._err_message.setText('Heslo musí obsahovat alespoň jedno\nčíslo.')
        elif len(password) < 4 or len(password) > 64:
            self._password.setStyleSheet('color: red;')
            self._err_message.setText('Heslo musí být dlouhé 3 - 64 znaků')
        else:
            self._password.setStyleSheet('')
            self._err_message.setText('')
            return True
        return False
    
    def validate_retype_password(self):
        '''
        Checks wether the to passwords match.
        '''
        password = self._password.text()
        retype_password = self._retype_password.text()
        if password != retype_password:
            self._retype_password.setStyleSheet('color: red;')
            self._err_message.setText('Hesla se musejí shodovat.')
        else:
            self._retype_password.setStyleSheet('')
            self._err_message.setText('')
            return True
        return False