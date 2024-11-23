from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, is_alphabetic, find_id, INFO_TITLE, WARNING_TITLE, ERROR_TITLE
from user import user as teacher_class
from table_style import apply_style
from db_user_subject import db_user_subject
from db_teacher import db_teacher
from db_subject import db_subject

class Priority(Frame):
    # region Interfaz
    def __init__(self, container, controller, type: teacher_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.controller = controller
                
        fr_search = Frame(self)
        fr_search.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        fr_entry = Frame(self)
        fr_entry.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)
        fr_table = Frame(self)
        fr_table.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        fr_button = Frame(self)
        fr_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        
        self.lb_search = Label(fr_search, text="Maestro a buscar: ", font=("Calisto MT", 12))
        self.lb_search.grid(row=0, column=0, padx=5)
        self.tx_search = Entry(fr_search, placeholder_text="Maestro a buscar", width=200)
        self.tx_search.grid(row=0, column=1,  padx=10, pady=10)
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_teacher)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        self.subjects = {}
        self.lb_subject = Label(fr_entry, text="Material")
        self.lb_subject.grid(row=0, column=0, pady=0, sticky="w")
        self.selected_subject = StringVar(value="administrador")
        self.selected_subject.trace("w", self.on_selection_subject)
        self.opm_subject = OptMenu(fr_entry, values="", variable=self.selected_subject)
        self.opm_subject.grid(row=0, column=1, pady=5)
        
        self.lb_name = Label(fr_entry, text="Nombre")
        self.lb_name.grid(row=1, column=0, pady=0, sticky="w")
        self.tx_name = Entry(fr_entry, placeholder_text="Nombre")
        self.tx_name.grid(row=1, column=1, pady=5, padx=20)
        self.lb_priority = Label(fr_entry, text="Prioridad")
        self.lb_priority.grid(row=1, column=2, pady=0, sticky="w")
        self.tx_priority = Entry(fr_entry, placeholder_text="Prioridad")
        self.tx_priority.grid(row=1, column=3, pady=5, padx=20)
                
        frame = Frame(fr_table)
        frame.grid(row=0, column=0, sticky="nsew")
        
        scroll_y = Scrollbar(frame)
        scroll_y.grid(row=0, column=1, sticky="ns") #Desplazamiento vertical
        
        scroll_x = Scrollbar(frame, orientation="horizontal")
        scroll_x.grid(row=1, column=0, sticky="ew") #Desplazamiento horizontal
        
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
        
        self.table['columns'] = ("Materia", "Maestro", "Prioridad")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("Materia", anchor="center", width=150)
        self.table.column("Maestro", anchor="center", width=150)
        self.table.column("Prioridad", anchor="center", width=100)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("Materia", text="Materia", anchor="center")
        self.table.heading("Maestro", text="Maestro", anchor="center")
        self.table.heading("Prioridad", text="Prioridad", anchor="center")

        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_priority)
        self.bt_save.grid(row=0, column=0, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=1, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_priority)
        self.bt_edit.grid(row=0, column=2, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=3, padx=5, pady=10)
        
        self.default()
    
    # region Funciones SQL
    def on_selection_subject(self, *args) -> None:
        subject_name = self.opm_subject.get()
        if subject_name == "" or subject_name is None:
            return
        
        self.update_table()
        self.bt_edit.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        
    def search_teacher(self) -> None:
        if not is_alphabetic(self.tx_search.get()):
            messagebox.showwarning(ERROR_TITLE, "Ingrese un nombre válido")
            return
        
        def search_id():
            for item in self.table.get_children():
                item_values = self.table.item(item, "values")
                
                if item_values[1] == self.tx_search.get():
                    return item
            return None
        
        id = search_id()
        if id is None:
            messagebox.showwarning(WARNING_TITLE, "No se encontro el maestro")
            return
        
        self.table.selection_set(id)
        self.table.focus(id)
        self.table.see(id)
        
    def save_priority(self) -> None:
        try:
            self.validate()
        except Exception as error:
            messagebox.showwarning(WARNING_TITLE, error)
            return
            
        try:
            teacher_id = find_id(db_teacher.get_teachers_dict(self), self.tx_name.get())
            subject_id = find_id(self.subjects, self.opm_subject.get())
            db_user_subject.edit(self, teacher_id, subject_id, self.tx_priority.get())
            messagebox.showinfo(INFO_TITLE, "Prioridad editada exitosamente!")
            self.default()
        except Exception as err:
            print(f"[-] save_priority: {err}")
            messagebox.showerror(ERROR_TITLE, f"Error al editar la prioridad en la BD")
    
    def get_priority(self) -> None:
        selected = self.table.focus()
        if selected is None or selected == "":
            raise Exception("No se selecciono un maestro")
        
        values = self.table.item(selected, "values")
        self.tx_name.configure(state=ENABLE)
        self.tx_priority.configure(state=ENABLE)
        self.opm_subject.configure(state=ENABLE)
        self.opm_subject.set(values[0])
        self.tx_name.insert(0, values[1])
        self.tx_priority.insert(0, values[2])
        self.tx_name.configure(state=DISABLED)
        self.tx_priority.configure(state=DISABLED)
        self.opm_subject.configure(state=DISABLED)
        self.enable_edit()
    
    # region Funciones extras
    def _return(self) -> None:
        self.controller.show_frame("Menu")
    
    def clear_priority(self):
        self.tx_name.configure(state=ENABLE)
        self.tx_name.delete(0, END)
        self.tx_priority.delete(0, END)
        self.opm_subject.set("")
    
    def default(self):
        self.subjects = db_subject.get_subjects_dict(self)
        self.opm_subject.configure(values=(self.subjects.values()))
        self.opm_subject.set("")
        
        self.clear_priority()
        self.clear_table()
        self.bt_edit.configure(state=DISABLED)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        
        self.opm_subject.configure(state=ENABLE)
        self.tx_name.configure(state=DISABLED)
        self.tx_priority.configure(state=DISABLED)
    
    def edit_priority(self) -> None:
        try:
            self.get_priority()
        except Exception as err:
            print("[-] ", err)
            messagebox.showerror(ERROR_TITLE, err)
            return
        
        self.band = False
    
    def enable_edit(self):
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        
        self.opm_subject.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        self.tx_priority.configure(state=ENABLE)
        
    # region Tabla
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
            
    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())
        
    def update_table(self) -> None:
        self.clear_table()
        subject_id = find_id(self.subjects, self.opm_subject.get())
        teachers = db_user_subject.get_teachers_by_subject(self, subject_id)
        self.insert_table(teachers)
    
    # region Validación
    def validate(self) -> None:
        # Empty
        entry_empty(self.tx_name, "Nombre")
        entry_empty(self.tx_priority, "Prioridad")
        
        if self.opm_subject.get() == "" or self.opm_subject.get() is None:
            raise Exception("Seleccione una materia")
        
        # Type
        if not self.tx_priority.get().isdecimal():
            raise Exception("Prioridad debe ser un número entero")
        
        # business logic
        print("Materia -> ", self.opm_subject.get(), " / Tipo ->", type(self.opm_subject.get()))
        prioritys: dict = db_user_subject.get_prioritys_by_subject(self, find_id(self.subjects, self.opm_subject.get()))
        print("Lista de prioridades -> ", prioritys)
        if int(self.tx_priority.get()) in prioritys.values():
            raise Exception("Este nivel de prioridad ya existe")