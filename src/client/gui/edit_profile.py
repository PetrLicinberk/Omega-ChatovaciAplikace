from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from src.client.gui import panel
import src.client.application as application
import src.client.config as config

class EditProfilePanel(panel.Panel):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        width = config.get_int('window', 'width', 800)
        height = config.get_int('window', 'height', 400)
        self.setFixedSize(width, height)

        self._topbar = TopBar(self._app)
        self._edit_profile_scroll = EditProfileScroll(self._app)

        self._back_btn = QtWidgets.QPushButton('Zpět')
        self._back_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._back_btn.clicked.connect(self.back_clicked)
        self._back_btn.setFixedHeight(30)

        self._save_btn = QtWidgets.QPushButton('Uložit')
        self._save_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._save_btn.clicked.connect(self.save_clicked)
        self._save_btn.setFixedHeight(30)

        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 7)
        self._layout.addWidget(self._topbar, 0, 0, 1, 20)
        self._layout.addWidget(self._edit_profile_scroll, 1, 1, 18, 18)
        self._layout.addWidget(self._back_btn, 19, 8, 1, 2)
        self._layout.addWidget(self._save_btn, 19, 10, 1, 2)
        self.setLayout(self._layout)

    def back_clicked(self):
        '''
        Displays MY_PROFILE panel.
        '''
        self._app.show_panel(panel.Panels.MY_PROFILE)

    def save_clicked(self):
        '''
        Saves user details to the server and displays MY_PROFILE panel.
        '''
        self._edit_profile_scroll.save()
        self._app.show_panel(panel.Panels.MY_PROFILE)

    def reset(self):
        '''
        Changes all values to defalt and resets child widgets.
        '''
        self._edit_profile_scroll.reset()


class EditProfileScroll(QtWidgets.QScrollArea):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        self.setStyleSheet('QLabel { \
                           font-size: 15px; \
                           } \
                           QLineEdit { \
                           font-size: 15px; \
                           } \
                           QScrollArea { \
                           border: none; \
                           }')

        self._username_label = QtWidgets.QLabel('Uživatelské jméno:')

        self._first_name_label = QtWidgets.QLabel('Jméno:')
        self._first_name_edit = QtWidgets.QLineEdit()
        self._first_name_edit.setFixedWidth(300)
        self._first_name_edit.setFixedHeight(30)

        self._last_name_label = QtWidgets.QLabel('Příjmení:')
        self._last_name_edit = QtWidgets.QLineEdit()
        self._last_name_edit.setFixedWidth(300)
        self._last_name_edit.setFixedHeight(30)

        self._email_label = QtWidgets.QLabel('Email:')
        self._email_edit = QtWidgets.QLineEdit()
        self._email_edit.setFixedWidth(300)
        self._email_edit.setFixedHeight(30)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.addWidget(self._username_label)
        self._layout.addWidget(self._first_name_label)
        self._layout.addWidget(self._first_name_edit)
        self._layout.addWidget(self._last_name_label)
        self._layout.addWidget(self._last_name_edit)
        self._layout.addWidget(self._email_label)
        self._layout.addWidget(self._email_edit)
        self._widget = QtWidgets.QWidget()
        self._widget.setLayout(self._layout)
        self.setWidget(self._widget)

    def reset(self):
        '''
        Loads user details from the server and displays them to the user.
        '''
        self._username_label.setText('Uživatelské jméno: {username}'.format(username=self._app._username))
        self._app._server.send('get_details', { 'username': self._app._username })
        cmd = None
        args = None
        try:
            cmd, args = self._app._server.recv()
        except:
            pass
        if cmd == 'user_details':
            self._first_name_edit.setText(args['first_name'])
            self._last_name_edit.setText(args['last_name'])
            self._email_edit.setText(args['email'])

    def save(self):
        '''
        Sends user details to the server.
        '''
        args = {}
        args['first_name'] = self._first_name_edit.text()
        args['last_name'] = self._last_name_edit.text()
        args['email'] = self._email_edit.text()
        self._app._server.send('save_details', args)


class TopBar(QtWidgets.QWidget):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('background-color: rgb(91, 217, 252);')
        
        self._layout = QtWidgets.QGridLayout()
        
        self._username = QtWidgets.QLabel('Upravit profil')
        self._username.setStyleSheet('font-size: 25px;')

        self._logout_btn = QtWidgets.QPushButton('Odhlásit se')
        self._logout_btn.setFixedWidth(90)
        self._logout_btn.setStyleSheet('QPushButton { \
                                       padding: 7px 0px; \
                                       background-color: none; \
                                       font-size: 14px; \
                                       }')
        self._logout_btn.clicked.connect(self.logout_clicked)
        self._logout_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._invites_btn = QtWidgets.QPushButton('Žádosti')
        self._invites_btn.setFixedWidth(90)
        self._invites_btn.setStyleSheet('QPushButton { \
                                       padding: 7px 0px; \
                                       background-color: none; \
                                       font-size: 14px; \
                                       }')
        self._invites_btn.clicked.connect(self.invites_clicked)
        self._invites_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._my_profile_btn = QtWidgets.QPushButton('Můj profil')
        self._my_profile_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._my_profile_btn.setFixedWidth(90)
        self._my_profile_btn.setStyleSheet('QPushButton { \
                                       padding: 7px 0px; \
                                       background-color: none; \
                                       font-size: 14px; \
                                       }')
        self._my_profile_btn.clicked.connect(self.my_profile_clicked)

        self._layout.addWidget(self._username, 0, 0, 1, 1)
        self._layout.addWidget(self._my_profile_btn, 0, 1, 1, 1)
        self._layout.addWidget(self._invites_btn, 0, 2, 1, 1)
        self._layout.addWidget(self._logout_btn, 0, 3, 1, 1)
        self.setLayout(self._layout)

    def reset(self):
        pass

    def logout_clicked(self):
        '''
        Logs out user and changes the panel to LOGIN.
        '''
        self._app._username = None
        self._app._chat_username = None
        self._app._server.send('logout_user', {})
        self._app.show_panel(panel.Panels.LOGIN)

    def invites_clicked(self):
        '''
        Changes the panel to INVITES
        '''
        self._app.show_panel(panel.Panels.INVITES)

    def my_profile_clicked(self):
        '''
        Changes the panel to MY_PROFILE
        '''
        self._app.show_panel(panel.Panels.MY_PROFILE)