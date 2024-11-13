class subject_career:
    def __init__(self, id_subject: int = 0, id_career: int = 0):
        self.subject_id = id_subject
        self.career_id = id_career
        
    def get_subject_id(self):
        return self.subject_id
    
    def get_career_id(self):
        return self.career_id