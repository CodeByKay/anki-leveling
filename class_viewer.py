# character_viewer.py
from aqt.qt import *
from . import config

class ClassViewer(QDialog):
    def __init__(self, character_data, parent=None):
        super().__init__(parent)
        self.character_data = character_data
        self.setWindowTitle("Character Data Viewer")
        self.setGeometry(50, 50, config.VIEWER_LENGTH, config.VIEWER_WIDTH)
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Anki Leveling Classes & Abilities")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: {config.FONT_SIZE_MEDIUM}; font-weight: bold; padding: 10px; color: {config.FONT_COLOR};")
        layout.addWidget(title)
        
        # Main tab widget for weapons
        self.main_tab_widget = QTabWidget()
        self.main_tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #c0c0c0;
                border-radius: 5px;
                background-color: white;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                border: 2px solid #c0c0c0;
                border-bottom-color: #c0c0c0;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                min-width: 100px;
                padding: 8px 16px;
                margin-right: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
                border-bottom-color: #4CAF50;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e8e8e8;
            }
        """)
        
        # Use config weapons
        weapons = [
            config.WEAPONS_NAME_0,
            config.WEAPONS_NAME_1,
            config.WEAPONS_NAME_2,
            config.WEAPONS_NAME_3,
            config.WEAPONS_NAME_4
        ]
        
        for weapon in weapons:
            weapon_tab = self.create_weapon_tab(weapon)
            self.main_tab_widget.addTab(weapon_tab, weapon)
        
        layout.addWidget(self.main_tab_widget)
        
        self.setLayout(layout)
    
    def create_weapon_tab(self, weapon):
        """Create a tab widget for a specific weapon with stat sub-tabs"""
        weapon_widget = QWidget()
        weapon_layout = QVBoxLayout()
        
        # Check if this weapon exists in the data
        if weapon not in self.character_data:
            no_data_label = QLabel(f"No data available for {weapon}")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet(f"font-size: {config.FONT_SIZE_MEDIUM}; color: #666; padding: 50px;")
            weapon_layout.addWidget(no_data_label)
            weapon_widget.setLayout(weapon_layout)
            return weapon_widget
        
        # Create sub-tab widget for stats
        stat_tab_widget = QTabWidget()
        stat_tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #a0a0a0;
                border-radius: 3px;
                background-color: #fafafa;
                margin-top: 5px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                border: 1px solid #a0a0a0;
                border-bottom-color: #a0a0a0;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                min-width: 80px;
                padding: 6px 12px;
                margin-right: 1px;
                font-weight: bold;
                font-size: 11px;
            }
            QTabBar::tab:selected {
                background-color: #2196F3;
                color: white;
                border-bottom-color: #2196F3;
            }
            QTabBar::tab:hover:!selected {
                background-color: #d0d0d0;
            }
        """)
        
        # Use config stats
        stats = [
            config.STATS_NAME_HP,
            config.STATS_NAME_STR,
            config.STATS_NAME_SPD,
            config.STATS_NAME_DEF,
            config.STATS_NAME_MP
        ]
        weapon_data = self.character_data[weapon]
        
        for stat in stats:
            if stat in weapon_data:
                stat_tab = self.create_stat_tab(weapon, stat, weapon_data[stat])
                stat_tab_widget.addTab(stat_tab, stat)
            else:
                # Create empty tab if stat doesn't exist
                empty_tab = QWidget()
                empty_layout = QVBoxLayout()
                empty_label = QLabel(f"No {stat} class available for {weapon}")
                empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                empty_label.setStyleSheet(f"font-size: {config.FONT_SIZE_SMALL}; color: #999; padding: 30px;")
                empty_layout.addWidget(empty_label)
                empty_tab.setLayout(empty_layout)
                stat_tab_widget.addTab(empty_tab, stat)
        
        weapon_layout.addWidget(stat_tab_widget)
        weapon_widget.setLayout(weapon_layout)
        return weapon_widget
    
    def create_stat_tab(self, weapon, stat, class_data):
        """Create a tab for a specific stat showing the class details"""
        stat_widget = QWidget()
        stat_layout = QVBoxLayout()
        
        # Class header
        class_header = QLabel(f"{weapon} - {stat} - {class_data['class']}")
        class_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        class_header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_MEDIUM}; 
            font-weight: bold; 
            color: #2E86AB; 
            padding: 15px; 
            background-color: #f8f9fa; 
            border-radius: 8px; 
            margin-bottom: 10px;
            border: 2px solid #e9ecef;
        """)
        stat_layout.addWidget(class_header)
        
        # Scroll area for abilities
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Abilities
        for ability_type, ability in class_data['abilities'].items():
            ability_frame = self.create_ability_display(ability_type, ability)
            scroll_layout.addWidget(ability_frame)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        stat_layout.addWidget(scroll_area)
        
        stat_widget.setLayout(stat_layout)
        return stat_widget
    
    def create_ability_display(self, ability_type, ability):
        """Create a display widget for a single ability"""
        ability_frame = QFrame()
        ability_frame.setFrameStyle(QFrame.Shape.Box)
        ability_frame.setStyleSheet("""
            QFrame { 
                border: 2px solid #dee2e6; 
                border-radius: 8px; 
                margin: 8px; 
                background-color: white;
            }
        """)
        ability_layout = QVBoxLayout()
        ability_layout.setSpacing(8)
        
        # Ability header with type badge
        header_layout = QHBoxLayout()
        
        # Ability name
        ability_name = QLabel(ability['name'])
        ability_name.setStyleSheet(f"font-weight: bold; font-size: {config.FONT_SIZE_SMALL}; color: #2E86AB;")
        header_layout.addWidget(ability_name)
        
        # Ability type badge
        type_badge = QLabel(ability_type)
        type_badge.setStyleSheet("""
            background-color: #6c757d; 
            color: white; 
            padding: 4px 8px; 
            border-radius: 12px; 
            font-size: 10px; 
            font-weight: bold;
        """)
        type_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(type_badge)
        header_layout.addStretch()
        
        ability_layout.addLayout(header_layout)
        
        # Description
        desc_label = QLabel(ability['description'])
        desc_label.setStyleSheet("""
            font-style: italic; 
            color: #6c757d; 
            padding: 5px 10px; 
            background-color: #f8f9fa; 
            border-radius: 5px; 
            border-left: 4px solid #007bff;
        """)
        desc_label.setWordWrap(True)
        ability_layout.addWidget(desc_label)
        
        # Stats in a more organized grid using config values
        stats_frame = QFrame()
        stats_frame.setStyleSheet("QFrame { border: 1px solid #e9ecef; border-radius: 5px; background-color: #f8f9fa; }")
        stats_layout = QGridLayout()
        stats_layout.setSpacing(8)
        stats_layout.setContentsMargins(10, 10, 10, 10)
        
        stats = [
            (config.ABILITY_NAME_DMG, ability['baseDamage'], config.ABILITY_BACKGROUND_COLOR_DMG),
            (config.ABILITY_NAME_HEAL, ability['heal'], config.ABILITY_BACKGROUND_COLOR_HEAL),
            (config.ABILITY_NAME_SPD_UP, ability['speedBuff'], config.ABILITY_BACKGROUND_COLOR_SPD_UP),
            (config.ABILITY_NAME_SPD_DOWN, ability['speedDebuff'], config.ABILITY_BACKGROUND_COLOR_SPD_DOWN),
            (config.ABILITY_NAME_DEF_UP, ability['defenseBuff'], config.ABILITY_BACKGROUND_COLOR_DEF_UP),
            (config.ABILITY_NAME_DEF_DOWN, ability['defenseDebuff'], config.ABILITY_BACKGROUND_COLOR_DEF_DOWN),
            (config.ABILITY_NAME_STR_UP, ability['strengthBuff'], config.ABILITY_BACKGROUND_COLOR_STR_UP),
            (config.ABILITY_NAME_STR_DOWN, ability['strengthDebuff'], config.ABILITY_BACKGROUND_COLOR_STR_DOWN),
            (config.ABILITY_NAME_MANA_COST, ability['manaCost'], config.ABILITY_BACKGROUND_COLOR_MANA_COST)
        ]
        
        displayed_stats = [(name, value, color) for name, value, color in stats if value != 0]
        
        for i, (stat_name, stat_value, color) in enumerate(displayed_stats):
            row = i // 3
            col = i % 3
            
            stat_container = QFrame()
            stat_container.setStyleSheet(f"""
                QFrame {{ 
                    border: 1px solid {color}; 
                    border-radius: 4px; 
                    background-color: white; 
                    padding: 5px;
                }}
            """)
            stat_container_layout = QVBoxLayout()
            stat_container_layout.setContentsMargins(5, 3, 5, 3)
            
            stat_name_label = QLabel(stat_name)
            stat_name_label.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {color};")
            stat_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            stat_value_label = QLabel(str(stat_value))
            stat_value_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #333;")
            stat_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            stat_container_layout.addWidget(stat_name_label)
            stat_container_layout.addWidget(stat_value_label)
            stat_container.setLayout(stat_container_layout)
            
            stats_layout.addWidget(stat_container, row, col)
        
        stats_frame.setLayout(stats_layout)
        ability_layout.addWidget(stats_frame)
        
        ability_frame.setLayout(ability_layout)
        return ability_frame