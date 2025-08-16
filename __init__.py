# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
import json
import os

# Global variable to store character data
CHARACTER_DATA = {}

def get_addon_dir():
    """Get the directory where this addon is located"""
    return os.path.dirname(__file__)

def load_character_data():
    """Load character data from character.json file"""
    global CHARACTER_DATA
    try:
        addon_dir = get_addon_dir()
        json_file_path = os.path.join(addon_dir, "character.json")
        
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                CHARACTER_DATA = json.load(f)
            return True
        else:
            showInfo(f"character.json not found at:\n{json_file_path}\n\nPlease ensure the file exists in the addon directory.")
            return False
    except Exception as e:
        showInfo(f"Error loading character.json: {str(e)}")
        return False

# Load character data when the module is imported
load_character_data()

class CharacterViewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Character Data Viewer")
        self.setGeometry(200, 200, 800, 600)
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("RPG Character Classes & Abilities")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Create tabs for different weapons
        tab_widget = QTabWidget()
        
        for weapon_type, weapon_data in CHARACTER_DATA.items():
            weapon_tab = QWidget()
            weapon_layout = QVBoxLayout()
            
            # Weapon title
            weapon_title = QLabel(f"{weapon_type} Classes")
            weapon_title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
            weapon_layout.addWidget(weapon_title)
            
            # Scroll area for classes
            scroll = QScrollArea()
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout()
            
            for stat_type, class_data in weapon_data.items():
                # Class group box
                class_group = QGroupBox(f"{stat_type} - {class_data['class']}")
                class_layout = QVBoxLayout()
                
                # Abilities
                for ability_type, ability in class_data['abilities'].items():
                    ability_frame = QFrame()
                    ability_frame.setFrameStyle(QFrame.Shape.Box)
                    ability_layout = QVBoxLayout()
                    
                    # Ability name and type
                    ability_header = QLabel(f"{ability['name']} ({ability_type})")
                    ability_header.setStyleSheet("font-weight: bold; color: #2E86AB;")
                    ability_layout.addWidget(ability_header)
                    
                    # Description
                    desc_label = QLabel(ability['description'])
                    desc_label.setStyleSheet("font-style: italic; margin-bottom: 5px;")
                    ability_layout.addWidget(desc_label)
                    
                    # Stats in a grid
                    stats_widget = QWidget()
                    stats_layout = QGridLayout()
                    
                    stats = [
                        ('Base Damage', ability['baseDamage']),
                        ('Heal', ability['heal']),
                        ('Speed Buff', ability['speedBuff']),
                        ('Speed Debuff', ability['speedDebuff']),
                        ('Defense Buff', ability['defenseBuff']),
                        ('Defense Debuff', ability['defenseDebuff']),
                        ('Strength Buff', ability['strengthBuff']),
                        ('Strength Debuff', ability['strengthDebuff']),
                        ('Mana Cost', ability['manaCost'])
                    ]
                    
                    for i, (stat_name, stat_value) in enumerate(stats):
                        row = i // 3
                        col = i % 3
                        stat_label = QLabel(f"{stat_name}: {stat_value}")
                        stat_label.setStyleSheet("font-size: 11px; padding: 2px;")
                        stats_layout.addWidget(stat_label, row, col)
                    
                    stats_widget.setLayout(stats_layout)
                    ability_layout.addWidget(stats_widget)
                    
                    ability_frame.setLayout(ability_layout)
                    class_layout.addWidget(ability_frame)
                
                class_group.setLayout(class_layout)
                scroll_layout.addWidget(class_group)
            
            scroll_widget.setLayout(scroll_layout)
            scroll.setWidget(scroll_widget)
            scroll.setWidgetResizable(True)
            weapon_layout.addWidget(scroll)
            
            weapon_tab.setLayout(weapon_layout)
            tab_widget.addTab(weapon_tab, weapon_type)
        
        layout.addWidget(tab_widget)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

def showCharacterData():
    """Function to display the character data in a new window"""
    if not CHARACTER_DATA:
        showInfo("No character data loaded. Please ensure character.json exists in the addon directory and reload the data.")
        return
        
    dialog = CharacterViewer(mw)
    dialog.exec()

def exportCharacterJSON():
    """Function to export character data to JSON file in addon directory"""
    if not CHARACTER_DATA:
        showInfo("No character data to export.")
        return
        
    try:
        addon_dir = get_addon_dir()
        json_file_path = os.path.join(addon_dir, "character.json")
        
        # Write the character data to JSON file
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(CHARACTER_DATA, f, indent=2, ensure_ascii=False)
        
        showInfo(f"Character data exported to:\n{json_file_path}")
    except Exception as e:
        showInfo(f"Error exporting character data: {str(e)}")

def reloadCharacterJSON():
    """Function to reload character data from JSON file"""
    if load_character_data():
        showInfo("Character data reloaded successfully!")
    else:
        showInfo("Failed to reload character data.")

# Create menu items
# View Character Data
view_action = QAction("View Character Data", mw)
qconnect(view_action.triggered, showCharacterData)
mw.form.menuTools.addAction(view_action)

# Export Character JSON
export_action = QAction("Export Character JSON", mw)
qconnect(export_action.triggered, exportCharacterJSON)
mw.form.menuTools.addAction(export_action)

# Reload Character JSON
reload_action = QAction("Reload Character JSON", mw)
qconnect(reload_action.triggered, reloadCharacterJSON)
mw.form.menuTools.addAction(reload_action)