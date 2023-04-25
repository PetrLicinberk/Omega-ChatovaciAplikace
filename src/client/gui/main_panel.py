from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from src.client.gui.panel import Panels, Panel
from src.client import config
from src.client import application
from src.client.gui import chat


class MainWidget(Panel):
    def __init__(self, app) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 15px;')
        self._app: application.ChatClient = app
        width = config.get_int('window', 'width', 800)
        height = config.get_int('window', 'height', 400)
        self.setFixedSize(width, height)

        

        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(False)
        self._timer.timeout.connect(self.reset)
        self._timer.setInterval(3000)
        self._timer.setTimerType(Qt.TimerType.VeryCoarseTimer)

        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._topbar = TopBar(self._app)
        self._friend_list = FriendList(self._app)
        self._chat = chat.Chat(self._app)

        self._layout.addWidget(self._topbar, 0, 0, 1, 20)
        self._layout.addWidget(self._friend_list, 1, 0, 19, 6)
        self._layout.addWidget(self._chat, 1, 6, 19, 14)
        self.setLayout(self._layout)

    def reset(self):
        '''
        resets values to default.
        '''
        if not self._timer.isActive():
            self._timer.start()
        self._topbar.reset()
        self._friend_list.reset()
        if self._app._chat_username not in self._friend_list._friends:
            self._app._chat_username = None
        self._chat.reset()


class TopBar(QtWidgets.QWidget):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('background-color: rgb(91, 217, 252);')
        
        self._layout = QtWidgets.QGridLayout()
        
        self._username = QtWidgets.QLabel('')
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
        self._my_profile_btn.setFixedHeight(90)
        self._my_profile_btn.setStyleSheet('QPushButton { \
                                       padding: 7px 0px; \
                                       background-color: none; \
                                       font-size: 14px; \
                                       }')
        self._my_profile_btn.clicked.connect(self.my_profile_clicked)

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
        '''
        Sets the text of username label.
        '''
        self._username.setText(self._app._username)

    def logout_clicked(self):
        '''
        Method called when logout button is clicked.
        Logs out the user and send the command to the server.
        '''
        self._app._username = None
        self._app._chat_username = None
        self._app._server.send('logout_user', {})
        self._app.show_panel(Panels.LOGIN)

    def invites_clicked(self):
        '''
        method called when the invates button is clicked.
        Displays the INVITES panel.
        '''
        self._app.show_panel(Panels.INVITES)

    def my_profile_clicked(self):
        '''
        Method called when the my profile button is clicked.
        Displays the MY_PROFILE panel.
        '''
        self._app.show_panel(Panels.MY_PROFILE)
    

class FriendList(QtWidgets.QWidget):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        self._friends = []

        self._layout = QtWidgets.QVBoxLayout()

        self._scroll_layout = QtWidgets.QVBoxLayout()
        self._scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._scroll_content = QtWidgets.QWidget()
        self._scroll_content.setLayout(self._scroll_layout)

        self._label = QtWidgets.QLabel('Přátelé: ')
        self._no_friends_label = QtWidgets.QLabel('Nemáte žádné přátele')
        self._no_friends_label.setStyleSheet('QLabel { color: gray; font-size: 12px; }')

        self._scroll = QtWidgets.QScrollArea()
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setWidgetResizable(True)
        self._scroll.setWidget(self._scroll_content)
        self._scroll.setStyleSheet('QScrollArea { border: none; }')

        self._find_users_btn = QtWidgets.QPushButton('Hledat uživatele')
        self._find_users_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._find_users_btn.setFixedHeight(30)
        self._find_users_btn.clicked.connect(self.find_users_clicked)

        self._layout.addWidget(self._scroll)
        self._layout.addWidget(self._find_users_btn)
        self.setLayout(self._layout)

    def find_users_clicked(self):
        '''
        Method called when the find users button is clicked.
        Displays the FINDUSER panel.
        '''
        self._app.show_panel(Panels.FINDUSER)

    def reset(self):
        '''
        Resets values to defalt and loads and displays friend list from the server.
        '''
        if type(self._app._panel) != MainWidget:
            return
        for i in reversed(range(self._scroll_layout.count())):
            item = self._scroll_layout.itemAt(i)
            widget = item.widget()
            self._scroll_layout.removeWidget(widget)
        self._app._server.send('get_friend_list', {})
        cmd = None
        args = None
        while cmd is None:
                try:
                    cmd, args = self._app._server.recv()
                except:
                    break
                if cmd != 'friend_list':
                    cmd = None
                    args = None
        if cmd == 'friend_list':
            self._friends = args['friends']
            self._scroll_layout.addWidget(self._label)
            if len(args['friends']) == 0:
                self._scroll_layout.addWidget(self._no_friends_label)
            for friend in args['friends']:
                object = FriendWidget(self._app, friend)
                self._scroll_layout.addWidget(object)


class FriendWidget(QtWidgets.QWidget):
    def __init__(self, app, username) -> None:
        '''
        Creates friend widget contaning username.

        :param username: friend's username
        '''
        super().__init__()
        self._app: application.ChatClient = app
        self._username = username

        self._button = QtWidgets.QPushButton(self._username)
        self._button.setFixedHeight(35)
        self._button.clicked.connect(self.clicked)
        self._button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._button.setStyleSheet('QPushButton { font-size: 14px; }')
        
        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._button, 0, 0, 1, 1)
        self.setLayout(self._layout)

    def clicked(self):
        '''
        Method called when widget is clicked.
        Displays chat with the friend.
        '''
        self._app._chat_username = self._username
        if type(self._app._panel) == MainWidget:
            self._app._panel._chat.reset()