from aqt.qt import *
from ..data import config
from .character import Character

class CharacterViewer(QDialog):
    def __init__(self, character_data, parent=None):
        super().__init__(parent)
        self.character_data = character_data
        self.characters = [Character(char_data) for char_data in character_data]
        self.current_character_index = 0
        
        self.setWindowTitle("Character Viewer")
        self.setGeometry(50, 50, config.VIEWER_LENGTH, config.VIEWER_WIDTH)
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Character Viewer")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: {config.FONT_SIZE_BIG}; font-weight: bold; padding: 10px; color: {config.FONT_COLOR};")
        layout.addWidget(title)
        
        # Character selector
        if len(self.characters) > 1:
            selector_layout = QHBoxLayout()
            selector_label = QLabel("Select Character:")
            selector_label.setStyleSheet(f"font-size: {config.FONT_SIZE_SMALL}; font-weight: bold;")
            
            self.character_combo = QComboBox()
            for i, char in enumerate(self.characters):
                self.character_combo.addItem(char.name)
            self.character_combo.currentIndexChanged.connect(self.on_character_changed)
            
            selector_layout.addWidget(selector_label)
            selector_layout.addWidget(self.character_combo)
            selector_layout.addStretch()
            layout.addLayout(selector_layout)
        
        # Scroll area for all content
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Create all sections
        self.create_overview_section(scroll_layout)
        self.create_stats_section(scroll_layout)
        self.create_dungeon_section(scroll_layout)
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Initialize with first character
        if self.characters:
            self.update_display()
    
    def create_overview_section(self, parent_layout):
        """Create the overview section showing basic character info"""
        # Section header
        section_header = QLabel("Character Overview")
        section_header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_MEDIUM}; 
            font-weight: bold; 
            color: #2E86AB; 
            padding: 15px; 
            background-color: #f8f9fa; 
            border-radius: 8px; 
            margin: 20px 0 15px 0;
            border: 2px solid #e9ecef;
        """)
        section_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(section_header)
        
        # Character header
        self.overview_header = QLabel()
        self.overview_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.overview_header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_BIG}; 
            font-weight: bold; 
            color: #2E86AB; 
            padding: 20px; 
            background-color: #f8f9fa; 
            border-radius: 10px; 
            margin-bottom: 20px;
            border: 3px solid #e9ecef;
        """)
        parent_layout.addWidget(self.overview_header)
        
        # Basic info grid
        self.overview_info = QGridLayout()
        self.overview_info.setSpacing(15)
        
        # Create info labels
        self.overview_labels = {}
        info_fields = [
            ('Level', 'level'),
            ('Rank', 'rank'),
            ('Weapon', 'weapon'),
            ('Current XP', 'current_xp'),
            ('Date Joined', 'date_joined'),
            ('Last Adventure', 'date_last_adventure')
        ]
        
        for i, (label_text, field_name) in enumerate(info_fields):
            row = i // 2
            col = i % 2 * 2
            
            label = QLabel(f"{label_text}:")
            label.setStyleSheet(f"font-weight: bold; font-size: {config.FONT_SIZE_SMALL}; color: #333;")
            
            value_label = QLabel()
            value_label.setStyleSheet(f"""
                font-size: {config.FONT_SIZE_SMALL}; 
                color: #666; 
                padding: 8px 12px; 
                background-color: white; 
                border: 1px solid #ddd; 
                border-radius: 5px;
            """)
            
            self.overview_info.addWidget(label, row, col)
            self.overview_info.addWidget(value_label, row, col + 1)
            self.overview_labels[field_name] = value_label
        
        parent_layout.addLayout(self.overview_info)
        parent_layout.addSpacing(20)
    
    def create_stats_section(self, parent_layout):
        """Create the stats section showing character statistics"""
        # Section header
        section_header = QLabel("Character Statistics")
        section_header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_MEDIUM}; 
            font-weight: bold; 
            color: #2E86AB; 
            padding: 15px; 
            background-color: #f8f9fa; 
            border-radius: 8px; 
            margin: 20px 0 15px 0;
            border: 2px solid #e9ecef;
        """)
        section_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(section_header)
        
        # Stats grid
        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(20)
        
        # Create stat displays
        self.stat_displays = {}
        stats_config = [
            ('HP', config.STATS_BACKGROUND_COLOR_HP, config.STATS_BORDER_COLOR_HP),
            ('Strength', config.STATS_BACKGROUND_COLOR_STR, config.STATS_BORDER_COLOR_STR),
            ('Speed', config.STATS_BACKGROUND_COLOR_SPD, config.STATS_BORDER_COLOR_SPD),
            ('Defense', config.STATS_BACKGROUND_COLOR_DEF, config.STATS_BORDER_COLOR_DEF),
            ('MP', config.STATS_BACKGROUND_COLOR_MP, config.STATS_BORDER_COLOR_MP)
        ]
        
        for i, (stat_name, bg_color, border_color) in enumerate(stats_config):
            row = i // 3
            col = i % 3
            
            stat_frame = QFrame()
            stat_frame.setStyleSheet(f"""
                QFrame {{ 
                    border: 3px solid {border_color}; 
                    border-radius: 10px; 
                    background-color: {bg_color}; 
                    padding: 15px;
                    margin: 5px;
                }}
            """)
            
            stat_layout = QVBoxLayout()
            
            stat_name_label = QLabel(stat_name)
            stat_name_label.setStyleSheet(f"font-size: {config.FONT_SIZE_SMALL}; font-weight: bold; color: {border_color}; text-align: center;")
            stat_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            stat_value_label = QLabel()
            stat_value_label.setStyleSheet(f"font-size: {config.FONT_SIZE_BIG}; font-weight: bold; color: #333; text-align: center;")
            stat_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            stat_layout.addWidget(stat_name_label)
            stat_layout.addWidget(stat_value_label)
            stat_frame.setLayout(stat_layout)
            
            self.stats_grid.addWidget(stat_frame, row, col)
            self.stat_displays[stat_name] = stat_value_label
        
        parent_layout.addLayout(self.stats_grid)
        parent_layout.addSpacing(20)
    
    def create_dungeon_section(self, parent_layout):
        """Create the dungeon section showing dungeon records"""
        # Section header
        section_header = QLabel("Dungeon Records")
        section_header.setStyleSheet(f"""
            font-size: {config.FONT_SIZE_MEDIUM}; 
            font-weight: bold; 
            color: #2E86AB; 
            padding: 15px; 
            background-color: #f8f9fa; 
            border-radius: 8px; 
            margin: 20px 0 15px 0;
            border: 2px solid #e9ecef;
        """)
        section_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(section_header)
        
        # Summary stats
        self.summary_frame = QFrame()
        self.summary_frame.setStyleSheet("""
            QFrame { 
                border: 2px solid #dee2e6; 
                border-radius: 8px; 
                background-color: #f8f9fa; 
                padding: 15px;
                margin-bottom: 20px;
            }
        """)
        summary_layout = QHBoxLayout()
        
        self.total_passes_label = QLabel()
        self.total_fails_label = QLabel()
        self.success_rate_label = QLabel()
        
        for label in [self.total_passes_label, self.total_fails_label, self.success_rate_label]:
            label.setStyleSheet(f"font-size: {config.FONT_SIZE_SMALL}; font-weight: bold; color: #333;")
            summary_layout.addWidget(label)
        
        self.summary_frame.setLayout(summary_layout)
        parent_layout.addWidget(self.summary_frame)
        
        # Dungeon records grid
        self.dungeon_grid = QGridLayout()
        self.dungeon_grid.setSpacing(10)
        
        # Create dungeon rank displays
        self.dungeon_displays = {}
        ranks = ['F', 'E', 'D', 'C', 'B', 'A', 'S']
        
        for i, rank in enumerate(ranks):
            row = i // 4
            col = i % 4
            
            rank_frame = QFrame()
            rank_frame.setStyleSheet("""
                QFrame { 
                    border: 2px solid #dee2e6; 
                    border-radius: 8px; 
                    background-color: white; 
                    padding: 10px;
                    margin: 5px;
                }
            """)
            
            rank_layout = QVBoxLayout()
            
            rank_label = QLabel(f"Rank {rank}")
            rank_label.setStyleSheet(f"font-size: {config.FONT_SIZE_SMALL}; font-weight: bold; color: #2E86AB; text-align: center;")
            rank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            passes_label = QLabel()
            passes_label.setStyleSheet("color: #28a745; font-weight: bold;")
            passes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            fails_label = QLabel()
            fails_label.setStyleSheet("color: #dc3545; font-weight: bold;")
            fails_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            rank_layout.addWidget(rank_label)
            rank_layout.addWidget(passes_label)
            rank_layout.addWidget(fails_label)
            rank_frame.setLayout(rank_layout)
            
            self.dungeon_grid.addWidget(rank_frame, row, col)
            self.dungeon_displays[rank] = {'passes': passes_label, 'fails': fails_label}
        
        parent_layout.addLayout(self.dungeon_grid)
        parent_layout.addSpacing(20)
    
    def on_character_changed(self, index):
        """Handle character selection change"""
        self.current_character_index = index
        self.update_display()
    
    def update_display(self):
        """Update all displays with current character data"""
        if not self.characters:
            return
            
        character = self.characters[self.current_character_index]
        
        # Update overview section
        self.overview_header.setText(f"{character.name}")
        
        # Update overview info
        self.overview_labels['level'].setText(str(character.level))
        self.overview_labels['rank'].setText(character.rank)
        self.overview_labels['weapon'].setText(character.weapon)
        self.overview_labels['current_xp'].setText(str(character.current_xp))
        self.overview_labels['date_joined'].setText(character.date_joined)
        self.overview_labels['date_last_adventure'].setText(character.date_last_adventure)
        
        # Update stats section
        self.stat_displays['HP'].setText(str(character.hp))
        self.stat_displays['Strength'].setText(str(character.strength))
        self.stat_displays['Speed'].setText(str(character.speed))
        self.stat_displays['Defense'].setText(str(character.defense))
        self.stat_displays['MP'].setText(str(character.mp))
        
        # Update dungeon section
        self.total_passes_label.setText(f"Total Passes: {character.get_total_dungeon_passes()}")
        self.total_fails_label.setText(f"Total Fails: {character.get_total_dungeon_fails()}")
        self.success_rate_label.setText(f"Success Rate: {character.get_success_rate():.1f}%")
        
        for rank in ['F', 'E', 'D', 'C', 'B', 'A', 'S']:
            record = character.get_dungeon_record(rank)
            self.dungeon_displays[rank]['passes'].setText(f"Passes: {record['pass']}")
            self.dungeon_displays[rank]['fails'].setText(f"Fails: {record['fail']}")