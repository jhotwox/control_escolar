class user:
    def __init__(self, id: int = 0, name: str = "", p_surname: str = "", m_surname: str = "", password: str = "", email: str = "", type: str = ""):
        self.id = id
        self.name = name
        self.p_surname = p_surname
        self.m_surname = m_surname
        self.password = password
        self.email = email
        self.type = type
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_p_surname(self):
        return self.p_surname
    
    def get_m_surname(self):
        return self.m_surname
        
    def get_password(self):
        return self.password
    
    def get_email(self):
        return self.email
    
    def get_type(self):
        return self.type