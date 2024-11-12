class teacher:
    def __init__(self, id: int = 0, cedula: str = ""):
        self.id = id
        self.cedula = cedula
    
    def get_id(self):
        return self.id
    
    def get_cedula(self):
        return self.cedula