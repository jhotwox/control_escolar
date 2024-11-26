class classroom:
    def __init__(self, id: int = 0, name: str = "", building_id: int = 0):
        self.id = id
        self.name = name
        self.id_building = building_id

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_id_building(self):
        return self.id_building