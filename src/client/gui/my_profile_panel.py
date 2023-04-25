from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from src.client.gui import panel
from src.client import application
from src.client import config

class MyProfilePanel(panel.Panel):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        width = config.get_int('window', 'width', 800)
        height = config.get_int('window', 'height', 400)
        self.setFixedSize(width, height)

        self._topbar = TopBar(self._app)
        self._user_details = UserDetailsScroll(self._app)

        self._back_btn = QtWidgets.QPushButton('Zpět')
        self._back_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._back_btn.clicked.connect(self.back_clicked)
        self._back_btn.setFixedHeight(30)

        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 7)
        self._layout.addWidget(self._topbar, 0, 0, 1, 20)
        self._layout.addWidget(self._user_details, 1, 1, 18, 18)
        self._layout.addWidget(self._back_btn, 19, 9, 1, 2)
        self.setLayout(self._layout)

    def back_clicked(self):
        '''
        Method called when the back button is clicked.
        Displays the MAIN panel.
        '''
        self._app.show_panel(panel.Panels.MAIN)

    def reset(self):
        '''
        Resets values to defalt and resets child wodgets.
        '''
        self._user_details.reset()


class TopBar(QtWidgets.QWidget):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('background-color: rgb(91, 217, 252);')
        
        self._layout = QtWidgets.QGridLayout()
        
        self._username = QtWidgets.QLabel('Můj profil')
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
        Method called when logout button is clicked.
        Logs out the user and send the command to the server.
        '''
        self._app._username = None
        self._app._chat_username = None
        self._app._server.send('logout_user', {})
        self._app.show_panel(panel.Panels.LOGIN)

    def invites_clicked(self):
        '''
        Method called when the invites button is clicked.
        Displays the INVITES panel.
        '''
        self._app.show_panel(panel.Panels.INVITES)

    def my_profile_clicked(self):
        '''
        Method called when my profile button is clicked.
        Displayd MY_PROFILE panel.
        '''
        self._app.show_panel(panel.Panels.MY_PROFILE)


class UserDetailsScroll(QtWidgets.QScrollArea):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        self.setStyleSheet('QLabel { \
                           font-size: 15px; \
                           margin: 3px 0px; \
                           } \
                           QScrollArea { \
                           border: none; \
                           }')
        self.setWidgetResizable(True)
        
        self._username = ''
        self._first_name = ''
        self._last_name = ''
        self._email = ''

        self._username_label = QtWidgets.QLabel('Uživatelské jméno: ')
        self._first_name_label = QtWidgets.QLabel('Jméno: ')
        self._last_name_label = QtWidgets.QLabel('Příjmení: ')
        self._email_label = QtWidgets.QLabel('Email: ')

        self._edit_profile_btn = QtWidgets.QPushButton('Upravit profil')
        self._edit_profile_btn.setFixedWidth(150)
        self._edit_profile_btn.setFixedHeight(30)
        self._edit_profile_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._edit_profile_btn.setStyleSheet('QPushButton { \
                                             font-size: 15px; \
                                             }')
        self._edit_profile_btn.clicked.connect(self.edit_profile_clicked)

        self._delete_profile_btn = QtWidgets.QPushButton('Smazat profil')
        self._delete_profile_btn.setFixedWidth(150)
        self._delete_profile_btn.setFixedHeight(30)
        self._delete_profile_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._delete_profile_btn.setStyleSheet('QPushButton { \
                                             font-size: 15px; \
                                             }')
        self._delete_profile_btn.clicked.connect(self.delete_profile_clicked)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.addWidget(self._username_label)
        self._layout.addWidget(self._first_name_label)
        self._layout.addWidget(self._last_name_label)
        self._layout.addWidget(self._email_label)
        self._layout.addWidget(self._edit_profile_btn)
        self._layout.addWidget(self._delete_profile_btn)
        self._widget = QtWidgets.QWidget()
        self._widget.setLayout(self._layout)
        self.setWidget(self._widget)

    def reset(self):
        '''
        Resets values to default.
        Loads and displays user details from the server.
        '''
        if self._app._username is not None:
            self.load_details()
            self.show_details()

    def load_details(self):
        '''
        Loads the user details from the server.
        '''
        self._app._server.send('get_details', { 'username': self._app._username })
        cmd = None
        args = None
        try:
            cmd, args = self._app._server.recv()
        except:
            pass
        if cmd == 'user_details':
            self._username = args['username']
            self._first_name = args['first_name']
            self._last_name = args['last_name']
            self._email = args['email']

    def show_details(self):
        '''
        Displeys user details returned by the server.
        '''
        self._username_label.setText('Uživatelské jméno: {username}'.format(username=self._username))
        self._first_name_label.setText('Jméno: {name}'.format(name=self._first_name))
        self._last_name_label.setText('Příjmení: {last_name}'.format(last_name=self._last_name))
        self._email_label.setText('Email: {email}'.format(email=self._email))

    def edit_profile_clicked(self):
        '''
        Method called when the edit profile button is clicked.
        Displays the EDIT_PROFILE panel.
        '''
        self._app.show_panel(panel.Panels.EDIT_PROFILE)

    def delete_profile_clicked(self):
        '''
        Method called when the delete profile button is cliced.
        Sends the command to the server.
        Displays the LOGIN panel.
        '''
        self._app._username = None
        self._app._chat_username = None
        self._app._server.send('delete_user', { })
        self._app.show_panel(panel.Panels.LOGIN)