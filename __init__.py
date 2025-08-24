# **init**.py (main addon file)
# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
import json
import os
# import config values
from .data import config
# import the ClassViewer and MonsterViewer from the separate modules
from .source.class_viewer import ClassViewer
from .source.monster_viewer import MonsterViewer
from .source.game_viewer import GameViewer

# Global variables to store data
CLASS_DATA = {}
MONSTER_DATA = {}

def get_addon_dir():
    """Get the directory where this addon is located"""
    return os.path.dirname(__file__)

def load_class_data():
    """Load class data from classes.json file"""
    global CLASS_DATA
    try:
        addon_dir = get_addon_dir()
        json_file_path = os.path.join(addon_dir, config.CLASSES_PATH)
       
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                CLASS_DATA = json.load(f)
            return True
        else:
            showInfo(f"classes.json not found at:\n{json_file_path}\n\nPlease ensure the file exists in the addon directory.")
            return False
    except Exception as e:
        showInfo(f"Error loading classes.json: {str(e)}")
        return False

def load_monster_data():
    """Load monster data from monsters.json file"""
    global MONSTER_DATA
    try:
        addon_dir = get_addon_dir()
        json_file_path = os.path.join(addon_dir, config.MONSTERS_PATH)
       
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                MONSTER_DATA = json.load(f)
            return True
        else:
            showInfo(f"monsters.json not found at:\n{json_file_path}\n\nPlease ensure the file exists in the addon directory.")
            return False
    except Exception as e:
        showInfo(f"Error loading monsters.json: {str(e)}")
        return False

# Load data when the module is imported
load_class_data()
load_monster_data()

def showClassData():
    """Function to display the class data in a new window"""
    if not CLASS_DATA:
        showInfo("No class data loaded. Please ensure classes.json exists in the addon directory and reload the data.")
        return
       
    # Pass the class data to the ClassViewer
    dialog = ClassViewer(CLASS_DATA, mw)
    dialog.exec()

def showMonsterData():
    """Function to display the monster data in a new window"""
    if not MONSTER_DATA:
        showInfo("No monster data loaded. Please ensure monsters.json exists in the addon directory and reload the data.")
        return
       
    # Pass the monster data to the MonsterViewer
    dialog = MonsterViewer(MONSTER_DATA, mw)
    dialog.exec()

def startAnkiLeveling():
    """function to display game in a new window"""
    dialog = GameViewer(mw)
    dialog.exec()

# Add separator for visual organization
mw.form.menuTools.addSeparator()

# Game-related actions
start_anki_leveling = QAction("Start Anki Leveling", mw)
qconnect(start_anki_leveling.triggered, startAnkiLeveling)
mw.form.menuTools.addAction(start_anki_leveling)

# Class-related actions
view_class_action = QAction("View Class Data", mw)
qconnect(view_class_action.triggered, showClassData)
mw.form.menuTools.addAction(view_class_action)

# Monster-related actions
view_monster_action = QAction("View Monster Bestiary", mw)
qconnect(view_monster_action.triggered, showMonsterData)
mw.form.menuTools.addAction(view_monster_action)

# Add separator for visual organization
mw.form.menuTools.addSeparator()