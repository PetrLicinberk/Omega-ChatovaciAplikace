from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
import math
from src.client import application
from src.client.gui import main_panel, panel, view_profile


class Chat(QtWidgets.QWidget):
    def __init__(self, app) -> None:
        super().__init__()
        self._app: application.ChatClient = app

        self._topbar = ChatTopBar(self._app)
        self._messages = MessagesWidget(self._app)
        self._message_input = MessageInput(self._app, self._messages)
        
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._topbar)
        self._layout.addWidget(self._messages)
        self._layout.addWidget(self._message_input)
        self.setLayout(self._layout)

    def reset(self):
        if self._app._chat_username is None:
            self.setVisible(False)
        else:
            self.setVisible(True)
        self._messages.reset()
        self._topbar.reset()


class MessageInput(QtWidgets.QWidget):
    def __init__(self, app, messages) -> None:
        super().__init__()
        self._app: application.ChatClient = app
        self._messages = messages
        self._to_long_style = 'font-size: 13px;'
        self.setFixedHeight(150)

        self._message_edit = QtWidgets.QTextEdit()
        self._message_edit.setPlaceholderText('Nová zpráva')
        self._message_edit.setStyleSheet('QTextEdit { font-size: 12px; }')
        self._message_edit.setFixedHeight(100)
        self._message_edit.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
        self._message_edit.show()
        self._message_edit.textChanged.connect(self.message_changed)

        self._send_button = QtWidgets.QPushButton('Poslat')
        self._send_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._send_button.setStyleSheet('QPushButton { font-size: 14px; }')
        self._send_button.setFixedHeight(50)
        self._send_button.clicked.connect(self.send_message_clicked)

        self._to_long_label = QtWidgets.QLabel('0/2048')
        self._to_long_label.setStyleSheet(self._to_long_style + ' color: gray;')
        self._to_long_label.setFixedHeight(15)

        self._layout = QtWidgets.QGridLayout()
        self._layout.addWidget(self._message_edit, 0, 0, 1, 9)
        self._layout.addWidget(self._send_button, 0, 9)
        self._layout.addWidget(self._to_long_label, 1, 0, 1, 10)
        self.setLayout(self._layout)

    def send_message_clicked(self):
        if self.validate_length():
            self._app._server.send('send_message', {
                'to': self._app._chat_username,
                'content': self._message_edit.toPlainText() })
            self._message_edit.setText('')
            self._messages.reset()

    def message_changed(self):
        self.validate_length()

    def validate_length(self):
        length = len(self._message_edit.toPlainText())
        if length <= 2048:
            self._to_long_label.setText('{len}/2048'.format(len=length))
            self._to_long_label.setStyleSheet(self._to_long_style + 'color: gray;')
            return True
        else:
            self._to_long_label.setText('Zpráva je příliž dlouhá: {len}/2048'.format(len=length))
            self._to_long_label.setStyleSheet(self._to_long_style + 'color: red;')
            return False
        

class ChatTopBar(QtWidgets.QWidget):
    def __init__(self, app):
        super().__init__()
        self._app: application.ChatClient = app
        self.setFixedHeight(40)

        self._username_label = QtWidgets.QLabel('')

        self._view_profile_btn = QtWidgets.QPushButton('Zobrazit profil')
        self._view_profile_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._view_profile_btn.setStyleSheet('QPushButton { font-size: 14px; }')
        self._view_profile_btn.setFixedWidth(150)
        self._view_profile_btn.setFixedHeight(30)
        self._view_profile_btn.clicked.connect(self.view_profile_clicked)

        self._remove_friend_btn = QtWidgets.QPushButton('Odebrat z přátel')
        self._remove_friend_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._remove_friend_btn.setStyleSheet('QPushButton { font-size: 14px; }')
        self._remove_friend_btn.setFixedWidth(150)
        self._remove_friend_btn.setFixedHeight(30)
        self._remove_friend_btn.clicked.connect(self.remove_friend_clicked)

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.addWidget(self._username_label)
        self._layout.addWidget(self._view_profile_btn)
        self._layout.addWidget(self._remove_friend_btn)
        self.setLayout(self._layout)

    def reset(self):
        if self._app._chat_username is not None:
            self._username_label.setText(self._app._chat_username)
        else:
            self._username_label.setText('')

    def remove_friend_clicked(self):
        self._app._server.send('remove_friend', { 'username': self._app._chat_username })
        if type(self._app._panel) == main_panel.MainWidget:
            self._app._panel.reset()
            self._app._chat_username = None

    def view_profile_clicked(self):
        self._app.show_panel(panel.Panels.VIEW_PROFILE)
        if type(self._app._panel) == view_profile.ViewProfile:
            self._app._panel.set_username(self._app._chat_username)
            self._app._panel.reset()




class MessagesWidget(QtWidgets.QScrollArea):
    def __init__(self, app):
        super().__init__()
        self._app: application.ChatClient = app
        self.setStyleSheet('QScrollArea { \
                           border: none; \
                           }')
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self._messages = []

        self._widget = QtWidgets.QWidget()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._widget.setLayout(self._layout)
        self.setWidget(self._widget)

    def reset(self):
        '''
        Sets default values and scrolls to bottom.
        '''
        if self._app._username is None:
            return
        if self._app._chat_username is not None and type(self._app._panel) == main_panel.MainWidget:
            self.load_messages()
            self.show_messages()
            self.setVisible(True)
        else:
            self.setVisible(False)
        if self.verticalScrollBar().value() == self.verticalScrollBar().maximum():
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def load_messages(self):
        '''
        Loads all messages for current chat from the server.
        '''
        self._app._server.send('get_messages', { 'user': self._app._chat_username })
        cmd = None
        args = None
        try:
            cmd, args = self._app._server.recv()
        except:
            pass
        if cmd != 'messages':
            cmd = None
            args = None
        if cmd == 'messages':
            self._messages = args['msg']

    def show_messages(self):
        '''
        Displays messages returned from the server.
        '''
        scroll_to_botom = self.verticalScrollBar().maximum() - 100 <= self.verticalScrollBar().value()
        for i in reversed(range(self._layout.count())):
            item = self._layout.itemAt(i)
            widget = item.widget()
            self._layout.removeWidget(widget)
        for i in range(len(self._messages)):
            message = self._messages[i]
            object = Message(message['from'], message['date'], message['content'])
            self._layout.addWidget(object)
        self.setVisible(True)
        if scroll_to_botom:
            max = self.verticalScrollBar().maximum()
            self.verticalScrollBar().setValue(max)

class Message(QtWidgets.QWidget):
    def __init__(self, from_user: str, date: str, content: str):
        '''
        Creates message widget containig sender's username, date
        and content of the message.

        :param from_user: Username of sender
        :param date: Datetime when the message was sent
        :param content: Message content
        '''
        super().__init__()
        
        self._from_user_label = QtWidgets.QLabel(from_user)
        self._from_user_label.setStyleSheet('QLabel { \
                                            font-weight: bold; \
                                            font-size: 15px; \
                                            }')
        
        formated_date = date.replace('-', '. ')
        self._date_label = QtWidgets.QLabel(formated_date)
        self._date_label.setStyleSheet('QLabel { \
                                       font-size: 14px; \
                                       color: gray \
                                       }')
        
        self._message_content = QtWidgets.QTextEdit()
        self._message_content.setReadOnly(True)
        self._message_content.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._message_content.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._message_content.setPlainText(content)
        self._message_content.setStyleSheet('QTextEdit { \
                                            background-color: rgb(240, 240, 240); \
                                            border: none; \
                                            font-size: 15px; \
                                            }')
        self._message_content.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
        self._message_content.show()
        doc_height = self._message_content.document().size().height()
        doc_height = math.ceil(doc_height)
        margins = self._message_content.contentsMargins().top() + self._message_content.contentsMargins().bottom()
        self._message_content.setFixedHeight(doc_height + margins)

        self._layout = QtWidgets.QGridLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.addWidget(self._from_user_label, 0, 0, 1, 1)
        self._layout.addWidget(self._date_label, 0, 1, 1, 1, Qt.AlignmentFlag.AlignRight)
        self._layout.addWidget(self._message_content, 1, 0, 1, 2)
        self.setLayout(self._layout)