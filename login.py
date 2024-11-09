from customtkinter import CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTk, CTkFrame as Frame
from tkinter import messagebox
from functions import is_empty, WARNING_TITLE, ERROR_TITLE
from db_user import db_user
from user import user as user_class
from menu import Menu
from users import Users

class Login(Frame):
    def __init__(self, container, controller, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # self.self = self
        self.container = container
        self.controller = controller
        
        lb_title = Label(self, text="Login", font=("Arial", 36, "bold"))
        lb_title.grid(row=0, column=1, pady=20)

        # self.lbUsername = Label(self, text="Username", font=("Calisto MT", 16))
        # self.lbUsername.grid(row=1, column=0)
        self.tx_email = Entry(self, width=200, placeholder_text="Correo")
        self.tx_email.grid(row=1, column=1, padx=20, pady=10)
        self.tx_email.insert(0, "")
        
        # self.lbPass = Label(self, text="Contraseña", font=("Calisto MT", 16))
        # self.lbPass.grid(row=2, column=0, pady=10)
        self.tx_pass = Entry(self, width=200, placeholder_text="Contraseña", show="*")
        self.tx_pass.grid(row=2, column=1, padx=20, pady=10)
        self.tx_pass.insert(0, "")
        
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
        
        if not self.validate():
            return
        
        try:
            aux = user_class(email=email, password=password)
            self.user = db_user.authenticate(self, aux)
        except:
            return
            
        if self.user.get_type() == 0:
            windows = {
                "Menu": Menu,
                "Users": Users
            }
        
        if self.user.get_type() == 1:
            windows = {
                "Menu": Menu
            }
        if self.user.get_type() == 2:
            windows = {
                "Menu": Menu
            }
        
        # Recorrer las clases
        for key, F in windows.items():
            # La llave se vuelve la clase
            self.controller.add_frame(key, F, self.user)

        self.controller.show_frame("Menu")