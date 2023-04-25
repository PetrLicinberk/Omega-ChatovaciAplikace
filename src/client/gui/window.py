from PyQt6 import QtWidgets
from PyQt6 import QtCore

class Window(QtWidgets.QMainWindow):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self._content = QtWidgets.QWidget()
        self._layout = QtWidgets.QStackedLayout()
        self._content.setLayout(self._layout)
        self.update()
        self.setCentralWidget(self._content)

    def add_panel(self, panel):
        '''
        Adds panel to the windows QStackedLayout.
        '''
        self._layout.addWidget(panel)
    
    def change_panel(self, panel_id):
        '''
        Changes the displayed panel.
        '''
        self._layout.setCurrentIndex(panel_id)