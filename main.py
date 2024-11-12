from customtkinter import CTk, CTkFrame as Frame
from login import Login

class my_app(CTk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.title("Control escolar")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # Pantalla completa
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        # self.attributes("-fullscreen", True)
        
        self.main_container = Frame(self)
        self.main_container.grid(padx=20, pady=20, sticky="nsew")
        
        # Variables globales entre ventanas
        self.shared_data = {
            "VALIDATE": False
        }
        
        # Todas las clases de frames (ventanas)
        self.frames = dict()
        
        self.frames["Login"] = Login(self.main_container, self)
        self.frames["Login"].grid(row=0, column=0, sticky="nsew")
        #self.frames["Login"].geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        
        # Mostrar ventana
        self.show_frame("Login")
    
    # Mostrar ventana
    def show_frame(self, page_name) -> None:
        try:
            frame = self.frames[page_name]
            frame.tkraise()
        except Exception as err:
            print(f"[-] show_frame in myApp: {err}")
    
    # Agregar ventana
    def add_frame(self, page_name, frame_class, *args) -> None:
        if page_name not in self.frames:
            frame = frame_class(self.main_container, self, *args)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = frame
    
    # Eliminar todas ventanas excepto login (puede usarse para volveras a crear de ser necesario)
    # Actualmente solo se usa al salir del menu para volverse a realizar el login 12/11/2024
    def delete_frames(self) -> None:
        for key, frame in list(self.frames.items()):
            if key != "Login":
                frame.destroy()
                del self.frames[key]

root = my_app()
root.mainloop()