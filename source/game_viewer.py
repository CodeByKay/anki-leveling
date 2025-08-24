# game_viewer.py
from aqt.qt import *
from ..data import config

class GameViewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Anki Leveling")
        self.setGeometry(50, 50, config.VIEWER_LENGTH, config.VIEWER_WIDTH)
        #self.setupUI()