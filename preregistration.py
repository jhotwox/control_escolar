class preregistration:
    def __init__(self, id_user: int = 0, id_subject: int = 0):
        self.user_id = id_user
        self.subject_id = id_subject
        
    def get_user_id(self):
        return self.user_id
    
    def get_subject_id(self):
        return self.subject_id