# **init**.py (main addon file)
# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
import json
import os

# Import the ClassViewer and MonsterViewer from the separate modules
from .class_viewer import ClassViewer
from .monster_viewer import MonsterViewer

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
        json_file_path = os.path.join(addon_dir, "classes.json")
       
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
        json_file_path = os.path.join(addon_dir, "monsters.json")
       
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

def exportClassJSON():
    """Function to export class data to JSON file in addon directory"""
    if not CLASS_DATA:
        showInfo("No class data to export.")
        return
       
    try:
        addon_dir = get_addon_dir()
        json_file_path = os.path.join(addon_dir, "classes.json")
       
        # Write the class data to JSON file
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(CLASS_DATA, f, indent=2, ensure_ascii=False)
       
        showInfo(f"Class data exported to:\n{json_file_path}")
    except Exception as e:
        showInfo(f"Error exporting class data: {str(e)}")

def exportMonsterJSON():
    """Function to export monster data to JSON file in addon directory"""
    if not MONSTER_DATA:
        showInfo("No monster data to export.")
        return
       
    try:
        addon_dir = get_addon_dir()
        json_file_path = os.path.join(addon_dir, "monsters.json")
       
        # Write the monster data to JSON file
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(MONSTER_DATA, f, indent=2, ensure_ascii=False)
       
        showInfo(f"Monster data exported to:\n{json_file_path}")
    except Exception as e:
        showInfo(f"Error exporting monster data: {str(e)}")

def reloadClassJSON():
    """Function to reload class data from JSON file"""
    if load_class_data():
        showInfo("Class data reloaded successfully!")
    else:
        showInfo("Failed to reload class data.")

def reloadMonsterJSON():
    """Function to reload monster data from JSON file"""
    if load_monster_data():
        showInfo("Monster data reloaded successfully!")
    else:
        showInfo("Failed to reload monster data.")

def reloadAllData():
    """Function to reload both class and monster data"""
    class_success = load_class_data()
    monster_success = load_monster_data()
    
    if class_success and monster_success:
        showInfo("All data reloaded successfully!")
    elif class_success:
        showInfo("Class data reloaded successfully!\nFailed to reload monster data.")
    elif monster_success:
        showInfo("Monster data reloaded successfully!\nFailed to reload class data.")
    else:
        showInfo("Failed to reload both class and monster data.")

# Create menu items

# Class-related actions
view_class_action = QAction("View Class Data", mw)
qconnect(view_class_action.triggered, showClassData)
mw.form.menuTools.addAction(view_class_action)

export_class_action = QAction("Export Class JSON", mw)
qconnect(export_class_action.triggered, exportClassJSON)
mw.form.menuTools.addAction(export_class_action)

reload_class_action = QAction("Reload Class JSON", mw)
qconnect(reload_class_action.triggered, reloadClassJSON)
mw.form.menuTools.addAction(reload_class_action)

# Add separator for visual organization
mw.form.menuTools.addSeparator()

# Monster-related actions
view_monster_action = QAction("View Monster Bestiary", mw)
qconnect(view_monster_action.triggered, showMonsterData)
mw.form.menuTools.addAction(view_monster_action)

export_monster_action = QAction("Export Monster JSON", mw)
qconnect(export_monster_action.triggered, exportMonsterJSON)
mw.form.menuTools.addAction(export_monster_action)

reload_monster_action = QAction("Reload Monster JSON", mw)
qconnect(reload_monster_action.triggered, reloadMonsterJSON)
mw.form.menuTools.addAction(reload_monster_action)

# Add separator and reload all action
mw.form.menuTools.addSeparator()

reload_all_action = QAction("Reload All Game Data", mw)
qconnect(reload_all_action.triggered, reloadAllData)
mw.form.menuTools.addAction(reload_all_action)