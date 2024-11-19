from customtkinter import CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTkFrame as Frame
from tkinter import messagebox
from functions import is_empty, WARNING_TITLE
from db_user import db_user
from user import user as teacher_class
from menu import Menu
from users import Users
from students import Students
from horarios import Horario
from teachers import Teachers
from subjects import Subjects
from careers import Careers
from buildings import Buildings
from classrooms import Classrooms
from subjects_careers import Subjects_Careers
from constants import TYPE

class Login(Frame):
    def __init__(self, container, controller, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.container = container
        self.controller = controller
        
        lb_title = Label(self, text="Login", font=("Arial", 36, "bold"))
        lb_title.grid(row=0, column=1, pady=20)

        self.tx_email = Entry(self, width=200, placeholder_text="Correo")
        self.tx_email.grid(row=1, column=1, padx=20, pady=10)
        self.tx_email.insert(0, "correo@gmail.com")
        
        self.tx_pass = Entry(self, width=200, placeholder_text="Contraseña", show="*")
        self.tx_pass.grid(row=2, column=1, padx=20, pady=10)
        self.tx_pass.insert(0, "123456")
        
        self.btLogin = Button(self, text="Ingresar", command=self.login)
        self.btLogin.grid(row=3, column=1, pady=15)
    
    def validate(self) -> bool:
        email = self.tx_email.get()
        password = self.tx_pass.get()
        
        if is_empty(email):
            messagebox.showwarning(WARNING_TITLE, "El campo correo esta vacio")
            return False
        if is_empty(password):
            messagebox.showwarning(WARNING_TITLE, "El campo contraseña esta vacio")
            return False
        if len(password) < 6:
            messagebox.showwarning(WARNING_TITLE, "La contraseña es demasiado corta")
            return False
        return True

    def login(self) -> None:
        email = self.tx_email.get()
        password = self.tx_pass.get()
        
        # validar el formato de los datos enviados
        if not self.validate():
            return
        
        try:
            aux = teacher_class(email=email, password=password)
            self.user = db_user.authenticate(self, aux)
        except:
            return

        # Ventanas a crear en caso de que sea admin
        if self.user.get_type() == TYPE[0]:
            windows = {
                "Menu": Menu,
                "Users": Users,
                "Students": Students,
                "Teachers": Teachers,
                "Schedules": Horario,
                "Subjects": Subjects,
                "Carreers": Careers,
                "Buildings": Buildings,
                "Classrooms": Classrooms,
                "Subjects_Careers": Subjects_Careers,
            }
        
        # Ventanas a crear en caso de que sea maestro
        if self.user.get_type() == TYPE[1]:
            windows = {
                "Menu": Menu,
                "Teachers": Teachers
            }
        
        # Ventanas a crear en caso de que sea alumno
        if self.user.get_type() == TYPE[2]:
            windows = {
                "Menu": Menu,
                "Students": Students
            }
        
        # Recorrer las clases
        for key, F in windows.items():
            # La llave es el nombre de la clase, con esta accedemos a la clase (ventana)
            # self.controller.add_frame("Menu", Menu(), self.user)
            self.controller.add_frame(key, F, self.user)

        self.controller.show_frame("Menu")