from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar, CTkCanvas as Canvas
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import find_id, INFO_TITLE, WARNING_TITLE, ERROR_TITLE
from db_career import db_carreer
from db_subject import db_subject
from career import career as career_class
from user import user as user_class
from table_style import apply_style
from constants import TYPE
from db_group import db_group

class Registrations(Frame):
    # region Interfaz
    def __init__(self, container, controller, type: user_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.controller = controller
        self.type = type
        
        self.TYPE_DICT = TYPE

        fr_table = Frame(self)
        fr_table.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        fr_button = Frame(self)
        fr_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Canvas
        self.canvas = Canvas(fr_table, width=600, height=600, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Dibujar cuadricula
        self.draw_canvas()

        # Inserción de datos
        # self.canvas.create_text(140, 50, text="Matemáticas", font=("Arial", 10), fill="black")
        self.draw_schedule()
        
        self.bt_update = Button(fr_button, text="Actualizar", border_width=1, width=60, command=self.clear_canvas)
        self.bt_update.grid(row=0, column=0, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=1, padx=5, pady=10)
        
    # region Funciones extras
    def _return(self) -> None:
        self.controller.show_frame("Menu")
    
    def clear_canvas(self) -> None:
        self.canvas.delete("all")
        self.draw_canvas()
        self.draw_schedule()

    def draw_canvas(self) -> None:
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        for i, dia in enumerate(dias):
            self.canvas.create_text(140 + i * 100, 20, text=dia, font=("Arial", 12, "bold"))
        
        # Horario
        for hora in range(7, 17):
            self.canvas.create_text(50, 50 + (hora - 7) * 40, text=f"{hora}:00", font=("Arial", 10, "bold"))
        
            # Dibujar rectangulos por hora
            for i in range(len(dias)):
                self.canvas.create_rectangle(100 + i * 100, 30 + (hora - 7) * 40, 180 + i * 100, 70 + (hora - 7) * 40, fill="lightgray")
    
    def draw_schedule(self) -> None:
        colors = ["lightblue", "lightgreen", "lightyellow", "lightpink"]
        
        groups = []
        if self.type.get_type() == "alumno":
            groups = db_group.get_student_table_data(self, self.type.get_id())
        if self.type.get_type() == "maestro":
            groups = db_group.get_teacher_table_data(self, self.type.get_id())
        print("grupos -> ", groups)
        
        for group in groups:
            (grupo_nombre, materia, profesor, salon, dia, hora_inicio, hora_fin) = group
            dia_idx = dia  # Obtiene el índice del día
            hora_inicio = int(hora_inicio.split(':')[0])
            hora_fin = int(hora_fin.split(':')[0])

            # Coordenadas para el Canvas
            x1 = 100 + dia_idx * 100
            y1 = 30 + (hora_inicio - 7) * 40
            x2 = x1 + 80
            y2 = 30 + (hora_fin - 7) * 40

            # Dibujar clase
            color = colors[dia % len(colors)]
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                            text=f"{materia}\n{profesor}\n{salon}", font=("Arial", 10))
