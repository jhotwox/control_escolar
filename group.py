class group:
    def __init__(self, id: int = 0, schedule_id: int = 0, teacher_id: int = 0, classroom_id: int = 0, subject_id: int = 0, name: str = "", max_quota: int = 0, quota: int = 0, semester: int = 0):
        if max_quota < 0 or quota < 0:
            raise ValueError("max_quota y quota deben ser valores no negativos.")
        if semester <= 0:
            raise ValueError("El semestre debe ser un valor positivo.")

        self.id = id
        self.schedule_id = schedule_id
        self.teacher_id = teacher_id
        self.classroom_id = classroom_id
        self.subject_id = subject_id
        self.name = name
        self.max_quota = max_quota
        self.quota = quota
        self.semester = semester
    
    def get_id(self):
        return self.id
    
    def get_schedule_id(self):
        return self.schedule_id
    
    def set_teacher_id(self, teacher_id: int):
        self.teacher_id = teacher_id

    def set_classroom_id(self, classroom_id: int):
        self.classroom_id = classroom_id
    
    def get_subject_id(self):
        return self.subject_id
    
    def get_name(self):
        return self.name
    
    def get_max_quota(self):
        return self.max_quota
    
    def get_quota(self):
        return self.quota
    
    def get_semester(self):
        return self.semester