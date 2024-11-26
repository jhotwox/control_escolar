from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar 
from tkinter import messagebox
from tkinter.ttk import Treeview
from db_group import db_group  
from db_classroom import db_classroom
from group import group as group_class
from table_style import apply_style
from functions import WARNING_TITLE, ERROR_TITLE, INFO_TITLE, find_id
import database as db
import random


class Groups(Frame):
    def __init__(self, container, controller, type: group_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.controller = controller
        self.type = type
        self.band = None

        fr_search = Frame(self)
        fr_search.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        fr_entry = Frame(self)
        fr_entry.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)
        fr_table = Frame(self)
        fr_table.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        fr_button = Frame(self)
        fr_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        self.lb_search = Label(fr_search, text="ID a buscar: ", font=("Calisto MT", 12))
        self.lb_search.grid(row=0, column=0, padx=5)
        self.tx_search = Entry(fr_search, placeholder_text="ID a buscar", width=200)
        self.tx_search.grid(row=0, column=1, padx=10, pady=10)
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_group)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0, sticky="w")
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)

        self.lb_name = Label(fr_entry, text="Nombre del Grupo")
        self.lb_name.grid(row=1, column=0, pady=0, sticky="w")
        self.tx_name = Entry(fr_entry, placeholder_text="Nombre del grupo")
        self.tx_name.grid(row=1, column=1, pady=5, padx=20)

        self.lb_capacity = Label(fr_entry, text="Cupo Máximo")
        self.lb_capacity.grid(row=2, column=0, pady=0, sticky="w")
        self.tx_capacity = Entry(fr_entry, placeholder_text="Cupo máximo")
        self.tx_capacity.grid(row=2, column=1, pady=5)

        self.lb_semester = Label(fr_entry, text="Semestre")
        self.lb_semester.grid(row=3, column=0, pady=0, sticky="w")
        self.tx_semester = Entry(fr_entry, placeholder_text="Semestre")
        self.tx_semester.grid(row=3, column=1, pady=5)

        self.lb_classroom = Label(fr_entry, text="Aula")
        self.lb_classroom.grid(row=4, column=0, pady=0, sticky="w")

        self.updated_classrooms = {}
        self.selected_classroom = StringVar(value="----")  # Valor por defecto
        self.opm_classroom = OptMenu(fr_entry, values=self.updated_classrooms.values(), variable=self.selected_classroom)
        self.opm_classroom.grid(row=4, column=1, pady=5)

        frame = Frame(fr_table)
        frame.grid(row=0, column=0, sticky="nsew")
        
        scroll_y = Scrollbar(frame)
        scroll_y.grid(row=0, column=1, sticky="ns") 
        
        scroll_x = Scrollbar(frame, orientation="horizontal")
        scroll_x.grid(row=1, column=0, sticky="ew") 

        apply_style()
        self.table = Treeview(
            frame,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            style="Custom.Treeview"
        )
        self.table.grid(row=0, column=0, sticky="nsew")

        scroll_y.configure(command=self.table.yview)
        scroll_x.configure(command=self.table.xview)

        self.table['columns'] = ("ID", "Horario","Maestro", "Aula", "Materia","Nombre del Grupo","Cupo Max","Cupo", "Semestre")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=30)
        self.table.column("Horario", anchor="center", width=100)
        self.table.column("Maestro", anchor="center", width=100)
        self.table.column("Aula", anchor="center", width=150)
        self.table.column("Materia", anchor="center", width=100)
        self.table.column("Nombre del Grupo", anchor="center", width=150)
        self.table.column("Cupo Max", anchor="center", width=100)
        self.table.column("Cupo", anchor="center", width=100)
        self.table.column("Semestre", anchor="center", width=100)
        
        
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Horario", text="Horario", anchor="center")
        self.table.heading("Maestro", text="Maestro", anchor="center")
        self.table.heading("Aula", text="Aula", anchor="center")
        self.table.heading("Materia", text="Materia", anchor="center")
        self.table.heading("Nombre del Grupo", text="Nombre del Grupo", anchor="center")
        self.table.heading("Cupo Max", text="Cupo Max", anchor="center")
        self.table.heading("Cupo", text="Cupo", anchor="center")
        self.table.heading("Semestre", text="Semestre", anchor="center")
        
        

        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_group)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_groups_for_all_schedules)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_group)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_group)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        self.bt_update = Button(fr_button, text="Actualizar", border_width=1, width=60, command=self.update_table)
        self.bt_update.grid(row=0, column=3, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=5, padx=5, pady=10)

        self.default()
        self.update_table()

    def edit_group(self) -> None:
        return

    def _return(self) -> None:
        self.controller.show_frame("Menu")
    
    def search_id_in_table(self, id: int) -> str:
        for item in self.table.get_children():
            item_values = self.table.item(item, "values")    
            if item_values[0] == str(id):
                return item
        return None
    
    def search_group(self) -> None:
        if not self.tx_search.get().isdecimal():
            messagebox.showwarning(ERROR_TITLE, "Ingrese un ID válido")
            return
        
        id = self.search_id_in_table(self.tx_search.get())
        if id is None:
            messagebox.showwarning(WARNING_TITLE, "No se encontro el grupo")
            return
        
        self.table.selection_set(id)
        self.table.focus(id)

    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)

    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())

    def update_table(self) -> None:
        self.clear_table()
        groups = db_group.get_all_groups(self)
        self.insert_table(groups)
    
  
    
    def remove_group(self) -> None:
       return

    def new_group(self) -> None:
        self.tx_search.configure(state=DISABLED)
        self.bt_search.configure(state=DISABLED)

        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.opm_classroom.configure(state=ENABLE)

        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)    
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        self.bt_return.configure(state=DISABLED)

        self.clear_group()
        next_id = db_group.get_max_id(self) + 1
        self.tx_id.insert(0, str(next_id))
        self.tx_id.configure(state=DISABLED)
        self.band = True
        return
    
    def update_classrooms(self) -> None:
        try:
            self.updated_classrooms = db_classroom.get_classroom_dict()
            
            menu = self.opm_classroom["menu"]
            menu.delete(0, "end")
            for name in self.updated_classrooms.values():
                menu.add_command(label=name, command=lambda value=name: self.selected_classroom.set(value))
        except Exception as err:
            print(f"[-] update_classrooms: {err}")
            messagebox.showerror(ERROR_TITLE, "Error al actualizar las aulas")

    def save_groups_for_all_schedules(self) -> None:
        try:

            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = "SELECT id FROM schedule"
            self.cursor.execute(self.sql)
            schedules = self.cursor.fetchall()

            self.sql = "SELECT id FROM subject"
            self.cursor.execute(self.sql)
            subjects = self.cursor.fetchall()

            if len(subjects) < len(schedules):
                raise Exception("No hay suficientes materias disponibles para llenar todos los horarios.")

            random.shuffle(subjects)

            for schedule, subject in zip(schedules, subjects):  
                schedule_id = schedule[0]
                subject_id = subject[0]

                group = group_class(
                    id=None,  
                    schedule_id=schedule_id,
                    teacher_id=None,  
                    classroom_id=None,  
                    subject_id=subject_id,
                    name=f"Grupo - {subject_id} - Horario {schedule_id}",
                    max_quota=int(self.tx_capacity.get()),
                    quota=int(self.tx_capacity.get()),
                    semester=int(self.tx_semester.get())
                )

                db_group.assign_teacher_and_classroom(group)

                db_group.save(group)

            self.default()
            self.update_table()
        except Exception as err:
            print(f"[-] save_groups_for_all_schedules: {err}")
            messagebox.showerror(ERROR_TITLE, f"Error al guardar grupos: {err}")


    def clear_group(self):
        self.tx_id.delete(0, END)
        self.tx_name.delete(0, END)
        self.tx_capacity.delete(0, END)
        self.tx_semester.delete(0, END)
        self.opm_classroom.set("")
    
    def default(self):
        self.updated_classrooms = db_classroom.get_classroom_dict(self)
        self.opm_classroom.configure(values=self.updated_classrooms.values())
        self.opm_classroom.set("----")
        
        self.tx_id.configure(state=ENABLE)
        
        self.tx_search.configure(state=ENABLE)
        self.bt_search.configure(state=ENABLE)

        self.tx_id.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        

        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_edit.configure(state=ENABLE)
        
        self.bt_return.configure(state=ENABLE)
        self.bt_remove.configure(state=ENABLE)

    def enable_edit(self):
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)

        self.bt_search.configure(state=DISABLED)
        self.tx_search.configure(state=DISABLED)
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        