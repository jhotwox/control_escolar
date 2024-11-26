from customtkinter import CTkButton as Button, CTkFrame as Frame, CTkLabel as Label
from user import user as teacher_class
from constants import TYPE

class Menu(Frame):
    def __init__(self, container, controller, profile: teacher_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.controller = controller
        self.profile = profile
        self.lb_title = Label(self, text=f"Hola {profile.get_name()}", font=("", 36, "bold"))
        self.lb_title.grid(row=0, column=0, pady=20, columnspan=2)
        
        self.bt_users = Button(self, text="Usuarios", command=self.open_users)
        self.bt_users.grid(row=1, column=0, padx=10, pady=10)
        
        self.bt_students = Button(self, text="Alumnos", command= self.open_students)
        self.bt_students.grid(row=1, column=1, padx=10, pady=10)
        
        self.bt_teachers = Button(self, text="Maestros", command=self.open_teachers)
        self.bt_teachers.grid(row=2, column=0, padx=10, pady=10)
        
        self.bt_subjects = Button(self, text="Materias", command=self.open_subjects)
        self.bt_subjects.grid(row=2, column=1, padx=10, pady=10)
        
        self.bt_schedules = Button(self, text="Horarios", command=self.open_schedules)
        self.bt_schedules.grid(row=3, column=0, padx=10, pady=10)
        
        self.bt_careers = Button(self, text="Carreras", command=self.open_careers)
        self.bt_careers.grid(row=3, column=1, padx=10, pady=10)
        
        self.bt_buildings = Button(self, text="Edificios", command=self.open_buildings)
        self.bt_buildings.grid(row=4, column=0, padx=10, pady=10)
        
        self.bt_classrooms = Button(self, text="Salones", command=self.open_classrooms)
        self.bt_classrooms.grid(row=4, column=1, padx=10, pady=10)
        
        self.bt_groups = Button(self, text="Grupos", command=self.open_groups)
        self.bt_groups.grid(row=5, column=0, padx=10, pady=10)
        
        self.bt_registrations = Button(self, text="Planeación", command=self.open_registrations)
        self.bt_registrations.grid(row=5, column=1, padx=10, pady=10)
        
        self.bt_subjects_careers = Button(self, text="Asignar materias", command=self.open_subjects_careers)
        self.bt_subjects_careers.grid(row=6, column=0, padx=10, pady=10)
        
        self.bt_priority = Button(self, text="Prioridad", command=self.open_priority)
        self.bt_priority.grid(row=6, column=1, padx=10, pady=10)
        
        self.bt_exit = Button(self, text="Salir", command=self.exit)
        self.bt_exit.grid(row=7, column=0, pady=10, padx=35, columnspan=2, sticky="ew")
        
        # Desavilitar botones por tipo de usuario
        if profile.get_type() == TYPE[1]:
            # self.bt_users.configure(state=DISABLED)
            # self.bt_teachers.configure(state=DISABLED)
            # self.bt_subjects.configure(state=DISABLED)
            # self.bt_careers.configure(state=DISABLED)
            return
        
        if profile.get_type() == TYPE[2]:
            # self.bt_users.configure(state=DISABLED)
            # self.bt_students.configure(state=DISABLED)
            # self.bt_teachers.configure(state=DISABLED)
            # self.bt_subjects.configure(state=DISABLED)
            # self.bt_careers.configure(state=DISABLED)
            return
    
    def open_users(self) -> None:
        self.controller.show_frame("Users")
    
    def open_students(self) -> None:
        self.controller.show_frame("Students")

    def open_teachers(self) -> None:
        self.controller.show_frame("Teachers")
    
    def open_subjects(self) -> None:
        self.controller.show_frame("Subjects")

    def open_schedules(self) -> None:
        self.controller.show_frame("Schedules")
        
    def open_careers(self) -> None:
        self.controller.show_frame("Carreers")
        
    def open_buildings(self) -> None:
        self.controller.show_frame("Buildings")
        
    def open_classrooms(self) -> None:
        self.controller.show_frame("Classrooms")
        
    def open_groups(self) -> None:
        self.controller.show_frame("Groups")
        
    def open_registrations(self) -> None:
        return
        # self.controller.show_frame("Registrations")
    
    def open_subjects_careers(self) -> None:
        self.controller.show_frame("Subjects_Careers")
    
    def open_priority(self) -> None:
        self.controller.show_frame("Priority")
    
    def exit(self) -> None:
        # if hasattr(self.controller, "show_frame"):
        #     self.controller.show_frame("Login")
        #     self.controller.delete_frames()
        # else:
        #     print("[-] Error con el controlador")
        
        self.controller.show_frame("Login")
        self.controller.delete_frames()