from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from src.client.gui.panel import Panels, Panel
from src.client.gui import view_profile
import src.client.config as config
import src.client.application as application


class FindUserWidget(Panel):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        width = config.get_int('window', 'width', 800)
        height = config.get_int('window', 'height', 400)
        self.setFixedSize(width, height)

        self._topbar = TopBar(self._app)
        self._search = Search(self._app)

        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._topbar, 0, 0, 1, 20)
        self._layout.addWidget(self._search, 1, 0, 19, 20)
        self.setLayout(self._layout)

    def reset(self):
        '''
        Resets values to default.
        '''
        self._topbar.reset()

class TopBar(QtWidgets.QWidget):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('background-color: rgb(91, 217, 252);')
        
        self._layout = QtWidgets.QGridLayout()
        
        self._username = QtWidgets.QLabel('Hledat uživatele')
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
        logs out user and changes the panel to LOGIN.
        '''
        self._app._username = None
        self._app._server.send('logout_user', {})
        self._app.show_panel(Panels.LOGIN)

    def invites_clicked(self):
        '''
        Displays the INVITES panel.
        '''
        self._app.show_panel(Panels.INVITES)

    def my_profile_clicked(self):
        '''
        Displays the MY_PROFILE panel.
        '''
        self._app.show_panel(Panels.MY_PROFILE)


class Search(QtWidgets.QWidget):
    def __init__(self, app):
        super().__init__()
        self._app: application.ChatClient = app

        self._input = QtWidgets.QLineEdit()
        self._input.setPlaceholderText('Uživatelské jméno')
        self._input.setFixedHeight(40)
        self._input.textChanged.connect(self.input_changed)
        self._input.setStyleSheet('QLineEdit { \
                                  font-size: 14px; \
                                  }')

        self._search_btn = QtWidgets.QPushButton('Hledat')
        self._search_btn.setFixedHeight(40)
        self._search_btn.clicked.connect(self.search_clicked)
        self._search_btn.setStyleSheet('QPushButton { \
                                       font-size: 15px; \
                                       }')
        self._search_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        self._err_message = QtWidgets.QLabel('')
        self._err_message.setStyleSheet('QLabel { \
                                        font-size: 14px; \
                                        color: red; \
                                        }')
        self._err_message.setFixedHeight(20)
        
        self._result_layout = QtWidgets.QVBoxLayout()
        self._result_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self._result_widget = QtWidgets.QWidget()
        self._result_widget.setLayout(self._result_layout)
        
        self._result_scroll = QtWidgets.QScrollArea()
        self._result_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._result_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._result_scroll.setWidgetResizable(True)
        self._result_scroll.setWidget(self._result_widget)
        self._result_scroll.setStyleSheet('QScrollArea { \
                                          border: none; \
                                          }')
        
        self._back_btn = QtWidgets.QPushButton('Zpět')
        self._back_btn.setStyleSheet('QPushButton { \
                                     font-size: 14px; \
                                     }')
        self._back_btn.setFixedHeight(30)
        self._back_btn.clicked.connect(self.back_clicked)

        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 7)
        self._layout.addWidget(self._input, 0, 2, 1, 5)
        self._layout.addWidget(self._search_btn, 0, 7, 1, 2)
        self._layout.addWidget(self._err_message, 1, 2, 1, 7)
        self._layout.addWidget(self._result_scroll, 2, 0, 10, 10)
        self._layout.addWidget(self._back_btn, 12, 4, 1, 2)
        self.setLayout(self._layout)

    def input_changed(self):
        '''
        Method called when search input changes.
        '''
        self.validate_username()

    def search_clicked(self):
        '''
        Method called when search button clicked.
        Loads search results from the server and displays them
        to the user.
        '''
        if self.validate_username():
            username = self._input.text()
            for i in reversed(range(self._result_layout.count())):
                item = self._result_layout.itemAt(i)
                widget = item.widget()
                self._result_layout.removeWidget(widget)
            self._app._server.send('find_users', { 'username': username })
            cmd = None
            args = None
            while cmd is None:
                try:
                    cmd, args = self._app._server.recv()
                except:
                    break
                if cmd != 'find_users':
                    cmd = None
                    args = None
            if cmd == 'find_users':
                results = args['users']
                for result in results:
                    object = SearchResult(self._app, self, result)
                    self._result_layout.addWidget(object)

    def back_clicked(self):
        '''
        Method called when back button clicked.
        Changes panel to MAIN.
        '''
        self._app.show_panel(Panels.MAIN)

    def validate_username(self):
        '''
        Check if the entered username is 3 - 64 characters long.
        '''
        username = self._input.text()
        if len(username) < 3:
            self._input.setStyleSheet('QLineEdit { \
                                  font-size: 14px; \
                                  color: red; \
                                  }')
            self._err_message.setText('Uživatelské jméno musí být alespoň 3 znaky dlouhé.')
        elif len(username) > 64:
            self._input.setStyleSheet('QLineEdit { \
                                  font-size: 14px; \
                                  color: red; \
                                  }')
            self._err_message.setText('Uživatelské jméno musí být maximálně 64 znaků dlouhé.')
        else:
            self._input.setStyleSheet('QLineEdit { \
                                  font-size: 14px; \
                                  }')
            self._err_message.setText('')
            return True
        return False
    

class SearchResult(QtWidgets.QWidget):
    def __init__(self, app, search, username):
        '''
        Creates search result widget containig username, view profile
        button and add to friends button.
        '''
        super().__init__()
        self._app: application.ChatClient = app
        self._search: Search = search
        self._username: str = username

        self._username_label = QtWidgets.QLabel(self._username)
        self._username_label.setStyleSheet('QLabel { \
                                           font-size: 15px; \
                                           }')
        
        self._view_profile_btn = QtWidgets.QPushButton('Profil')
        self._view_profile_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._view_profile_btn.setFixedWidth(100)
        self._view_profile_btn.setFixedHeight(30)
        self._view_profile_btn.clicked.connect(self.view_profile_clicked)
        
        self._add_friend = QtWidgets.QPushButton('Přidat do přátel')
        self._add_friend.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._add_friend.setFixedWidth(100)
        self._add_friend.setFixedHeight(30)
        self._add_friend.clicked.connect(self.add_friend_clicked)

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._username_label)
        self._layout.addWidget(self._view_profile_btn)
        self._layout.addWidget(self._add_friend)
        self.setLayout(self._layout)

    def add_friend_clicked(self):
        '''
        Method called when add to friends button is clicked.
        Sends add_friend command to the server.
        '''
        self._app._server.send('add_friend', { 'username': self._username })
        self._search.search_clicked()

    def view_profile_clicked(self):
        '''
        Method called when view profile button is clicked.
        Displays VIEW_PROFILE panel.
        '''
        self._app.show_panel(Panels.VIEW_PROFILE)
        if type(self._app._panel) == view_profile.ViewProfile:
            self._app._panel.set_username(self._username)
            self._app._panel.reset()