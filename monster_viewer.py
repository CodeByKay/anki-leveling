# monster_viewer.py
from aqt.qt import *
from . import config

class MonsterViewer(QDialog):
    def __init__(self, monster_data, parent=None):
        super().__init__(parent)
        self.monster_data = monster_data
        self.setWindowTitle("Monster Data Viewer")
        self.setGeometry(200, 200, 1200, 900)
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Monster Bestiary - Evolution Lines")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: {config.FONT_SIZE_BIG}; font-weight: bold; padding: 15px; color: {config.FONT_COLOR};")
        layout.addWidget(title)
        
        # Main tab widget for stat focus categories
        self.main_tab_widget = QTabWidget()
        
        # Get monster tier border colors from config
        tier_colors = [
            config.MONSTER_TIER_BORDER_COLOR_1, 
            config.MONSTER_TIER_BORDER_COLOR_2,
            config.MONSTER_TIER_BORDER_COLOR_3
        ]
        
        self.main_tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 2px solid black;
                border-radius: 8px;
                background-color: #FFF8DC;
            }}
            QTabWidget::tab-bar {{
                alignment: center;
            }}
            QTabBar::tab {{
                background-color: #DEB887;
                border: 2px solid black;
                border-bottom-color: black;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                min-width: 120px;
                padding: 10px 20px;
                margin-right: 3px;
                font-weight: bold;
                color: #654321;
            }}
            QTabBar::tab:selected {{
                background-color: white;
                color: white;
                border-bottom-color: white;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: #CD853F;
            }}
        """)
        
        # Stat focus categories using config stat names and colors
        categories = [
            (config.STATS_NAME_HP, f"{config.STATS_NAME_HP}-Focused (Tanks)", config.STATS_TEXT_COLOR_HP),
            (config.STATS_NAME_STR, f"{config.STATS_NAME_STR}-Focused (Attackers)", config.STATS_TEXT_COLOR_STR),
            (config.STATS_NAME_SPD, f"{config.STATS_NAME_SPD}-Focused (Agile)", config.STATS_TEXT_COLOR_SPD),
            (config.STATS_NAME_DEF, f"{config.STATS_NAME_DEF}-Focused (Guardians)", config.STATS_TEXT_COLOR_DEF),
            (config.STATS_NAME_MP, f"{config.STATS_NAME_MP}-Focused (Magical)", config.STATS_TEXT_COLOR_MP)
        ]
        
        for category_key, category_name, category_color in categories:
            category_tab = self.create_category_tab(category_key, category_name, category_color)
            self.main_tab_widget.addTab(category_tab, category_name.split(" ")[0])
        
        layout.addWidget(self.main_tab_widget)
        
        self.setLayout(layout)
    
    def create_category_tab(self, category_key, category_name, category_color):
        """Create a tab widget for a specific stat category with monster sub-tabs"""
        category_widget = QWidget()
        category_layout = QVBoxLayout()
        
        # Category header
        category_header = QLabel(category_name)
        category_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        category_header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_MEDIUM}; 
            font-weight: bold; 
            color: {category_color}; 
            padding: 12px; 
            background-color: {category_color}; 
            border-radius: 8px; 
            margin-bottom: 10px;
        """)
        category_layout.addWidget(category_header)
        
        # Check if this category exists in the data
        if category_key not in self.monster_data:
            no_data_label = QLabel(f"No monsters available for {category_name}")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet(f"font-size: {config.FONT_SIZE_MEDIUM}; color: #666; padding: 50px;")
            category_layout.addWidget(no_data_label)
            category_widget.setLayout(category_layout)
            return category_widget
        
        # Create sub-tab widget for individual monsters in this category
        monster_tab_widget = QTabWidget()
        monster_tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {category_color};
                border-radius: 5px;
                background-color: #FFFEF7;
                margin-top: 5px;
            }}
            QTabBar::tab {{
                background-color: #F5F5DC;
                border: 1px solid {category_color};
                border-bottom-color: {category_color};
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                min-width: 90px;
                padding: 8px 12px;
                margin-right: 1px;
                font-weight: bold;
                font-size: 11px;
                color: #8B4513;
            }}
            QTabBar::tab:selected {{
                background-color: {category_color};
                color: white;
                border-bottom-color: {category_color};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: #F0E68C;
            }}
        """)
        
        monsters = self.monster_data[category_key]
        
        for i, monster in enumerate(monsters):
            monster_tab = self.create_monster_tab(monster, category_color)
            tab_name = monster['name']['base']
            monster_tab_widget.addTab(monster_tab, f"{i+1}. {tab_name}")
        
        category_layout.addWidget(monster_tab_widget)
        category_widget.setLayout(category_layout)
        return category_widget
    
    def create_monster_tab(self, monster, category_color):
        """Create a tab for a specific monster showing its evolution line and abilities"""
        monster_widget = QWidget()
        monster_layout = QVBoxLayout()
        
        # Evolution line header
        evolution_header = QFrame()
        evolution_header.setStyleSheet(f"""
            QFrame {{ 
                background-color: {category_color}; 
                border-radius: 10px; 
                margin: 5px; 
            }}
        """)
        evolution_layout = QHBoxLayout()
        
        # Display all three tiers using config monster tier colors
        tiers = ['tier1', 'tier2', 'tier3']
        tier_colors = [
            config.MONSTER_TIER_BACKGROUND_COLOR_0,
            config.MONSTER_TIER_BACKGROUND_COLOR_1, 
            config.MONSTER_TIER_BACKGROUND_COLOR_2
        ]
        
        for tier, tier_color in zip(tiers, tier_colors):
            tier_frame = QFrame()
            tier_frame.setStyleSheet(f"""
                QFrame {{ 
                    background-color: {tier_color}; 
                    border-radius: 8px; 
                    padding: 8px; 
                    margin: 5px;
                }}
            """)
            tier_layout = QVBoxLayout()
            
            name_label = QLabel(monster['name'][tier])
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_label.setStyleSheet(f"font-size: {config.FONT_SIZE_SMALL}; font-weight: bold; color: white;")
            name_label.setWordWrap(True)
            
            tier_layout.addWidget(name_label)
            tier_frame.setLayout(tier_layout)
            evolution_layout.addWidget(tier_frame)
        
        evolution_header.setLayout(evolution_layout)
        monster_layout.addWidget(evolution_header)
        
        # Stats display using config stat colors
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            QFrame {{ 
                border: 2px solid white; 
                border-radius: 8px; 
                background-color: #FFF8DC; 
                margin: 5px; 
            }}
        """)
        stats_layout = QVBoxLayout()
        
        stats_title = QLabel("Base Stats")
        stats_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_title.setStyleSheet(f"font-size: {config.FONT_SIZE_SMALL}; font-weight: bold; color: {config.FONT_COLOR}; padding: 5px;")
        stats_layout.addWidget(stats_title)
        
        stats_grid_layout = QHBoxLayout()
        stats_data = monster['stats']
        
        # Use config stat colors
        stat_colors = {
            config.STATS_NAME_HP: config.STATS_TEXT_COLOR_HP,
            config.STATS_NAME_STR: config.STATS_TEXT_COLOR_STR, 
            config.STATS_NAME_SPD: config.STATS_TEXT_COLOR_SPD,
            config.STATS_NAME_DEF: config.STATS_TEXT_COLOR_DEF,
            config.STATS_NAME_MP: config.STATS_TEXT_COLOR_MP
        }
        
        for stat_name, stat_value in stats_data.items():
            stat_container = QFrame()
            stat_container.setStyleSheet(f"""
                QFrame {{ 
                    border: 2px solid {stat_colors.get(stat_name, '#666')}; 
                    border-radius: 6px; 
                    background-color: white; 
                    padding: 8px;
                    margin: 2px;
                }}
            """)
            stat_container_layout = QVBoxLayout()
            
            stat_name_label = QLabel(stat_name)
            stat_name_label.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {stat_colors.get(stat_name, '#666')};")
            stat_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            stat_value_label = QLabel(str(stat_value))
            stat_value_label.setStyleSheet(f"font-size: {config.FONT_SIZE_SMALL}; font-weight: bold; color: #333;")
            stat_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            stat_container_layout.addWidget(stat_name_label)
            stat_container_layout.addWidget(stat_value_label)
            stat_container.setLayout(stat_container_layout)
            
            stats_grid_layout.addWidget(stat_container)
        
        stats_layout.addLayout(stats_grid_layout)
        stats_frame.setLayout(stats_layout)
        monster_layout.addWidget(stats_frame)
        
        # Abilities section
        abilities_scroll = QScrollArea()
        abilities_widget = QWidget()
        abilities_layout = QVBoxLayout()
        
        abilities_title = QLabel("Abilities")
        abilities_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        abilities_title.setStyleSheet(f"font-size: {config.FONT_SIZE_MEDIUM}; font-weight: bold; color: {config.FONT_COLOR}; padding: 10px;")
        abilities_layout.addWidget(abilities_title)
        
        for ability in monster['abilities']:
            ability_frame = self.create_ability_display(ability, category_color)
            abilities_layout.addWidget(ability_frame)
        
        abilities_layout.addStretch()
        abilities_widget.setLayout(abilities_layout)
        abilities_scroll.setWidget(abilities_widget)
        abilities_scroll.setWidgetResizable(True)
        monster_layout.addWidget(abilities_scroll)
        
        monster_widget.setLayout(monster_layout)
        return monster_widget
    
    def create_ability_display(self, ability, category_color):
        """Create a display widget for a single ability"""
        ability_frame = QFrame()
        ability_frame.setFrameStyle(QFrame.Shape.Box)
        ability_frame.setStyleSheet(f"""
            QFrame {{ 
                border: 2px solid {category_color}; 
                border-radius: 10px; 
                margin: 8px; 
                background-color: #FFFEF7;
            }}
        """)
        ability_layout = QVBoxLayout()
        ability_layout.setSpacing(10)
        
        # Ability header
        header_layout = QHBoxLayout()
        
        # Ability name
        ability_name = QLabel(ability['name'])
        ability_name.setStyleSheet(f"font-weight: bold; font-size: {config.FONT_SIZE_MEDIUM}; color: {category_color};")
        header_layout.addWidget(ability_name)
        header_layout.addStretch()
        
        ability_layout.addLayout(header_layout)
        
        # Description
        desc_label = QLabel(ability['description'])
        desc_label.setStyleSheet(f"""
            font-style: italic; 
            color: #8B4513; 
            padding: 8px 12px; 
            background-color: #FFF8DC; 
            border-radius: 6px; 
            border-left: 4px solid {category_color};
        """)
        desc_label.setWordWrap(True)
        ability_layout.addWidget(desc_label)
        
        # Stats in a grid using config ability colors
        stats_frame = QFrame()
        stats_frame.setStyleSheet("QFrame { border: 1px solid #DDD; border-radius: 6px; background-color: #FAFAFA; }")
        stats_layout = QGridLayout()
        stats_layout.setSpacing(6)
        stats_layout.setContentsMargins(8, 8, 8, 8)
        
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
            row = i // 4
            col = i % 4
            
            stat_container = QFrame()
            stat_container.setStyleSheet(f"""
                QFrame {{ 
                    border: 1px solid {color}; 
                    border-radius: 4px; 
                    background-color: white; 
                    padding: 4px;
                }}
            """)
            stat_container_layout = QVBoxLayout()
            stat_container_layout.setContentsMargins(4, 2, 4, 2)
            
            stat_name_label = QLabel(stat_name)
            stat_name_label.setStyleSheet(f"font-size: 9px; font-weight: bold; color: {color};")
            stat_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            stat_value_label = QLabel(str(stat_value))
            stat_value_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #333;")
            stat_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            stat_container_layout.addWidget(stat_name_label)
            stat_container_layout.addWidget(stat_value_label)
            stat_container.setLayout(stat_container_layout)
            
            stats_layout.addWidget(stat_container, row, col)
        
        stats_frame.setLayout(stats_layout)
        ability_layout.addWidget(stats_frame)
        
        ability_frame.setLayout(ability_layout)
        return ability_frame