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
from .source.character_viewer import CharacterViewer
from .source.character import Character

# Global variables to store data
CLASS_DATA = {}
MONSTER_DATA = {}
CHARACTER_DATA = []

def get_addon_dir():
    """Get the directory where this addon is located"""
    return os.path.dirname(__file__)

def load_json_data(json_path, default_value):
    """Generic function to load JSON data from a file
    
    Args:
        json_path (str): Path to the JSON file relative to addon directory
        default_value: Default value to use if file doesn't exist
    
    Returns:
        dict/list: The loaded JSON data or default value
    """
    try:
        addon_dir = get_addon_dir()
        json_file_path = os.path.join(addon_dir, json_path)
        
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            showInfo(f"{os.path.basename(json_path)} not found at:\n{json_file_path}\n\nPlease ensure the file exists in the addon directory.")
            return default_value
        
        return data
        
    except Exception as e:
        showInfo(f"Error loading {os.path.basename(json_path)}: {str(e)}")
        return default_value

# Load data when the module is imported
CLASS_DATA = load_json_data(config.CLASSES_PATH, {})
MONSTER_DATA = load_json_data(config.MONSTERS_PATH, {})
CHARACTER_DATA = load_json_data(config.CHARACTERS_PATH, [])
MAIN_CHARACTER = None

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

def showCharacterData():
    """Function to display the character manager in a new window"""
    if not CHARACTER_DATA:
        showInfo("No character data available. Please ensure characters.json exists in the addon directory.")
        return
        
    dialog = CharacterViewer(CHARACTER_DATA, mw)
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

# Character-related actions
view_character_action = QAction("View Characters", mw)
qconnect(view_character_action.triggered, showCharacterData)
mw.form.menuTools.addAction(view_character_action)

# Add separator for visual organization
mw.form.menuTools.addSeparator()