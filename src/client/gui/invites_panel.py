from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from src.client.gui import panel, view_profile
import src.client.config as config
import src.client.application as application


class InvitesPanel(panel.Panel):
    def __init__(self, app):
        super().__init__()
        self._app: application.ChatClient = app
        width = config.get_int('window', 'width', 800)
        height = config.get_int('window', 'height', 400)
        self.setFixedSize(width, height)

        self._topbar = TopBar(self._app)
        self._invites_widget = InvitesWidget(self._app)

        self._friend_invites_label = QtWidgets.QLabel('Žádosti o přátelství:')
        self._friend_invites_label.setStyleSheet('QLabel { \
                                                 font-size: 15px; \
                                                 }')

        self._back_btn = QtWidgets.QPushButton('Zpět')
        self._back_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._back_btn.clicked.connect(self.back_clicked)
        self._back_btn.setFixedHeight(30)

        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 7)
        self._layout.addWidget(self._topbar, 0, 0, 1, 20)
        self._layout.addWidget(self._friend_invites_label, 1, 1, 1, 18)
        self._layout.addWidget(self._invites_widget, 2, 1, 17, 18)
        self._layout.addWidget(self._back_btn, 19, 9, 1, 2)
        self.setLayout(self._layout)

    def back_clicked(self):
        '''
        Method called when back button is clicked.
        Changes the panel to MAIN.
        '''
        self._app.show_panel(panel.Panels.MAIN)

    def reset(self):
        self._topbar.reset()
        self._invites_widget.reset()

class TopBar(QtWidgets.QWidget):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('background-color: rgb(91, 217, 252);')
        
        self._layout = QtWidgets.QGridLayout()
        
        self._username = QtWidgets.QLabel('Žádosti o přátelství')
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
        Logs out user and changes the panel to LOGIN.
        '''
        self._app._username = None
        self._app._server.send('logout_user', {})
        self._app.show_panel(panel.Panels.LOGIN)

    def invites_clicked(self):
        '''
        Method called when invites button clicked.
        Changes the panel to INVITES
        '''
        self._app.show_panel(panel.Panels.INVITES)

    def my_profile_clicked(self):
        '''
        Method called when view my profile button is clicked.
        Displays MY_PROFILE panel.
        '''
        self._app.show_panel(panel.Panels.MY_PROFILE)


class InvitesWidget(QtWidgets.QScrollArea):
    def __init__(self, app):
        super().__init__()
        self._app: application.ChatClient = app
        self._requests = []
        self.setWidgetResizable(True)
        self.setStyleSheet('QScrollArea { \
                           border: none; \
                           }')
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._scroll_layout = QtWidgets.QVBoxLayout()
        self._scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._scroll_widget = QtWidgets.QWidget()
        self._scroll_widget.setLayout(self._scroll_layout)

        self.setWidget(self._scroll_widget)

    def reset(self):
        '''
        Resets values to defalt and reset child widgets.
        '''
        if self._app._username is not None:
            self.load_requests()
            self.show_requests()

    def load_requests(self):
        '''
        Loads friend invites from the server.
        '''
        if self._app._username is not None:
            self._app._server.send('get_invites', { })
            cmd = None
            args = None
            try:
                cmd, args = self._app._server.recv()
            except:
                pass
            if cmd != 'friend_req':
                cmd = None
                args = None
            if cmd == 'friend_req':
                self._requests = args['req']

    def show_requests(self):
        '''
        Displays friend requests returned by the server.
        '''
        for i in reversed(range(self._scroll_layout.count())):
            item = self._scroll_layout.itemAt(i)
            widget = item.widget()
            self._scroll_layout.removeWidget(widget)
        if len(self._requests) == 0:
            label = QtWidgets.QLabel('Nemáte žádné žádosti o přátelství')
            self._scroll_layout.addWidget(label)
        for i in range(len(self._requests)):
            request = self._requests[i]
            object = Invite(self._app, request)
            self._scroll_layout.addWidget(object)


class Invite(QtWidgets.QWidget):
    def __init__(self, app, username):
        '''
        Creates invite widget containing username, view profile button,
        accept button and decline button.

        :param username: Username invite was sent from
        '''
        super().__init__()
        self._app: application.ChatClient = app
        self._username = username

        self._username_label = QtWidgets.QLabel(self._username)
        self._username_label.setStyleSheet('QLabel { \
                                           font-size: 15px; \
                                           }')
        
        self._accept_btn = QtWidgets.QPushButton('Přijmout')
        self._accept_btn.setFixedWidth(100)
        self._accept_btn.setFixedHeight(30)
        self._accept_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._accept_btn.clicked.connect(self.accept_clicked)

        self._decline_btn = QtWidgets.QPushButton('Odmítnout')
        self._decline_btn.setFixedWidth(100)
        self._decline_btn.setFixedHeight(30)
        self._decline_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._decline_btn.clicked.connect(self.decline_clicked)

        self._view_profile_btn = QtWidgets.QPushButton('Profil')
        self._view_profile_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._view_profile_btn.setFixedWidth(100)
        self._view_profile_btn.setFixedHeight(30)
        self._view_profile_btn.clicked.connect(self.view_profile_clicked)

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._username_label)
        self._layout.addWidget(self._view_profile_btn)
        self._layout.addWidget(self._accept_btn)
        self._layout.addWidget(self._decline_btn)
        self.setLayout(self._layout)

    def accept_clicked(self):
        '''
        Method called when accept invite button is clicked.
        Accepts the invite and sends the command to the server.
        '''
        self._app._server.send('accept_friend_req', { 'username': self._username })
        if type(self._app._panel) == InvitesPanel:
            self._app._panel.reset()

    def decline_clicked(self):
        '''
        Method called when decline button is clicked.
        Declines the invite and sends the command to the server.
        '''
        self._app._server.send('decline_friend_req', { 'username': self._username })
        if type(self._app._panel) == InvitesPanel:
            self._app._panel.reset()

    def view_profile_clicked(self):
        '''
        Method called when the view profile button is clicked.
        Displays the VIEW_PROFILE panel.
        '''
        self._app.show_panel(panel.Panels.VIEW_PROFILE)
        if type(self._app._panel) == view_profile.ViewProfile:
            self._app._panel.set_username(self._username)
            self._app._panel.reset()