class Character:
    def __init__(self, name, server, region):
        self.name = name
        self.server = server
        self.region = region
        self.item_level = -1
        self.mythic_rating = -1
        self.character_class = "unknown"
        
        @property
        def item_level(self):
            return self.item_level
        
        @item_level.setter
        def item_level(self, value):
            self.item_level = value
            
        @property
        def mythic_rating(self):
            return self.mythic_rating
        
        @mythic_rating.setter
        def mythic_rating(self, value):
            self.mythic_rating = value
            
        @property
        def character_class(self):
            return self.character_class
        
        @character_class.setter
        def character_class(self, value):
            self.character_class = value
        
        
            
        
        