class Character:
    """Represents a character in the Anki Leveling game"""
    
    def __init__(self, character_data):
        """Initialize a character from character data dictionary"""
        self.name = character_data.get('name', 'Unknown')
        self.date_joined = character_data.get('dateJoined', 'Unknown')
        self.date_last_adventure = character_data.get('dateLastAdventure', 'Unknown')
        self.weapon = character_data.get('weapon', 'None')
        self.stats = character_data.get('stats', {})
        self.level = character_data.get('level', 1)
        self.rank = character_data.get('rank', 'F')
        self.current_xp = character_data.get('currentXP', 0)
        self.dungeons = character_data.get('dungeons', {})
        
        # Initialize stats with defaults if missing
        self.hp = self.stats.get('HP', 120)
        self.strength = self.stats.get('Strength', 1)
        self.speed = self.stats.get('Speed', 1)
        self.defense = self.stats.get('Defense', 1)
        self.mp = self.stats.get('MP', 1)
    
    def get_stat(self, stat_name):
        """Get a specific stat value"""
        return self.stats.get(stat_name, 0)
    
    def get_dungeon_record(self, rank):
        """Get dungeon pass/fail record for a specific rank"""
        return self.dungeons.get(rank, {'pass': 0, 'fail': 0})
    
    def get_total_dungeon_passes(self):
        """Get total number of dungeon passes across all ranks"""
        return sum(dungeon.get('pass', 0) for dungeon in self.dungeons.values())
    
    def get_total_dungeon_fails(self):
        """Get total number of dungeon fails across all ranks"""
        return sum(dungeon.get('fail', 0) for dungeon in self.dungeons.values())
    
    def get_success_rate(self):
        """Calculate overall dungeon success rate"""
        total_passes = self.get_total_dungeon_passes()
        total_attempts = total_passes + self.get_total_dungeon_fails()
        return (total_passes / total_attempts * 100) if total_attempts > 0 else 0
    
    def to_dict(self):
        """Convert character back to dictionary format"""
        return {
            'name': self.name,
            'dateJoined': self.date_joined,
            'dateLastAdventure': self.date_last_adventure,
            'weapon': self.weapon,
            'stats': {
                'HP': self.hp,
                'Strength': self.strength,
                'Speed': self.speed,
                'Defense': self.defense,
                'MP': self.mp
            },
            'level': self.level,
            'rank': self.rank,
            'currentXP': self.current_xp,
            'dungeons': self.dungeons
        }
    
    def __str__(self):
        return f"Character: {self.name} (Level {self.level}, Rank {self.rank})"
    
    def __repr__(self):
        return f"Character(name='{self.name}', level={self.level}, rank='{self.rank}')"
