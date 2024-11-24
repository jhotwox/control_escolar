class Horario:
    def __init__(self, id: int = 0, day: int = 0, start_time: str = "", end_time: str = ""):
        self.id = id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
    
    def get_id(self):
        return self.id
    
    def get_day(self):
        return self.day
    
    def get_start_time(self):
        return self.start_time
    
    def get_end_time(self):
        return self.end_time