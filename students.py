from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar, CTkTextbox as Textbox
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, find_id, INFO_TITLE, WARNING_TITLE, ERROR_TITLE
from table_style import apply_style
from db_user import db_user
from user import user as user_class
from db_subject import db_subject
from db_preregistration import db_preregistration
from db_user_career import db_user_career
from db_career import db_carreer

class Students(Frame):
    # region Interfaz
    def __init__(self, container, controller, type: user_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.controller = controller
        self.type: user_class = type
        
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
        self.tx_search.grid(row=0, column=1,  padx=10, pady=10)
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_student)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0, sticky="w")
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)
        
        self.lb_name = Label(fr_entry, text="Nombre")
        self.lb_name.grid(row=1, column=0, pady=0, sticky="w")
        self.tx_name = Entry(fr_entry, placeholder_text="Nombre")
        self.tx_name.grid(row=1, column=1, pady=5, padx=20)
        self.lb_email = Label(fr_entry, text="Correo")
        self.lb_email.grid(row=1, column=2, pady=0, sticky="w")
        self.tx_email = Entry(fr_entry, placeholder_text="Correo")
        self.tx_email.grid(row=1, column=3, pady=5, padx=20)

        self.lb_p_surname = Label(fr_entry, text="Apellido Paterno")
        self.lb_p_surname.grid(row=2, column=0, pady=0, sticky="w")
        self.tx_p_surname = Entry(fr_entry, placeholder_text="Apellido Paterno")
        self.tx_p_surname.grid(row=2, column=1, pady=5, padx=20)
        self.lb_m_surname = Label(fr_entry, text="Apellido Materno")
        self.lb_m_surname.grid(row=2, column=2, pady=0, sticky="w")
        self.tx_m_surname = Entry(fr_entry, placeholder_text="Apellido Materno")
        self.tx_m_surname.grid(row=2, column=3, pady=5, padx=20)

        self.careers = []
        self.lb_career = Label(fr_entry, text="Carrera")
        self.lb_career.grid(row=3, column=0, pady=0, sticky="w")
        self.selected_career = StringVar(value="")
        self.selected_career.trace("w", self.on_selection_carreer)
        self.opm_career = OptMenu(fr_entry, values=(self.careers), variable=self.selected_career)
        self.opm_career.grid(row=3, column=1, pady=5)
        
        self.subjects = []
        self.lb_subject = Label(fr_entry, text="Materia")
        self.lb_subject.grid(row=3, column=2, pady=0, sticky="w")
        self.selected_subject = StringVar(value="")
        self.selected_subject.trace("w", self.on_selection_subject)
        self.opm_subject = OptMenu(fr_entry, values=(self.subjects), variable=self.selected_subject)
        self.opm_subject.grid(row=3, column=3, pady=5)
        
        self.tx_subject = Textbox(fr_entry, width=200, height=100)
        self.tx_subject.grid(row=1, column=4, columnspan=2, rowspan=3, pady=5)
        
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
        
        self.table['columns'] = ("ID", "Nombre", "Ap_paterno", "Ap_materno", "Correo")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=30)
        self.table.column("Nombre", anchor="center", width=150)
        self.table.column("Ap_paterno", anchor="center", width=150)
        self.table.column("Ap_materno", anchor="center", width=150)
        self.table.column("Correo", anchor="center", width=150)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Nombre", text="Nombre", anchor="center")
        self.table.heading("Ap_paterno", text="Ap_paterno", anchor="center")
        self.table.heading("Ap_materno", text="Ap_materno", anchor="center")
        self.table.heading("Correo", text="Correo", anchor="center")
        
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save)
        self.bt_save.grid(row=0, column=0, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=1, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_student)
        self.bt_edit.grid(row=0, column=2, padx=5, pady=10)
        self.bt_update = Button(fr_button, text="Actualizar", border_width=1, width=60, command=self.update_table)
        self.bt_update.grid(row=0, column=3, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=4, padx=5, pady=10)
        
        self.update_table()
        self.default()
    
    # region Funciones SQL
    def on_selection_carreer(self, *args) -> None:
        if self.type.get_type() == "administrador":
            return
        
        career_name = self.opm_career.get()        
        if career_name == "" or career_name is None or career_name == "No asignado":
            return
        
        self.opm_subject.configure(state=ENABLE)
        career_id = db_carreer.get_id_by_name(self, career_name)
        self.subjects = db_subject.get_subjects_by_career(self, career_id)
        self.opm_subject.configure(values=self.subjects)
    
    def on_selection_subject(self, *args) -> None:
        if self.type.get_type() == "administrador":
            return
        
        subject_name = self.opm_subject.get()
        if subject_name == "" or subject_name is None:
            return
        
        subject_list = self.get_subjects_from_tb()
        self.tx_subject.configure(state=ENABLE)
        # Eliminar
        if subject_name in subject_list:
            new_text = self.tx_subject.get(1.0, "end-1c").replace(subject_name+"\n", "")
            self.tx_subject.delete(1.0, END)
            self.tx_subject.insert(1.0, new_text)
        # Añadir
        else:
            self.tx_subject.insert("end", subject_name + "\n")
        
        self.tx_subject.configure(state=DISABLED)
    
    def get_subjects_from_tb(self) -> list:
        self.tx_subject.configure(state=ENABLE)
        all_text = self.tx_subject.get(1.0, "end-1c")
        self.tx_subject.configure(state=DISABLED)
        return all_text.splitlines()
    
    def search_id_in_table(self, id: int) -> str:
        for item in self.table.get_children():
            item_values = self.table.item(item, "values")    
            if item_values[0] == str(id):
                return item
        return None
    
    def search_student(self) -> None:
        if not self.tx_search.get().isdecimal():
            messagebox.showwarning(ERROR_TITLE, "Ingrese un ID válido")
            return
        
        id = self.search_id_in_table(self.tx_search.get())
        if id is None:
            messagebox.showwarning(WARNING_TITLE, "No se encontro el estudiante")
            return
        
        self.table.selection_set(id)
        self.table.focus(id)
        self.table.see(id)
    
    #TODO: Guardar preregistro
    def save(self) -> None:
        try:
            self.validate()
        except Exception as error:
            messagebox.showwarning(WARNING_TITLE, error)
            return

        try:
            # Guardar carrera
            if self.type.get_type() == "administrador":
                db_user_career.remove_by_user(self, self.tx_id.get())
                db_user_career.save(self, self.tx_id.get(), db_carreer.get_id_by_name(self, self.opm_career.get()))
                messagebox.showinfo(INFO_TITLE, "Carrera guardada exitosamente!")
            # Guardar preregistro
            elif self.type.get_type() == "alumno":
                # Eliminar preregistros anteriores
                db_preregistration.remove_all_by_user(self, self.tx_id.get())
                
                # Guardar preregistros nuevos
                subjects_list = self.get_subjects_from_tb()
                subjects_dict = db_subject.get_subjects_dict(self, db_carreer.get_id_by_name(self, self.opm_career.get()))
                if subjects_dict is None or subjects_dict == {}:
                    raise Exception("No se encontraron materias en la carrera")
                for subject in subjects_list:
                    db_preregistration.save(self, self.tx_id.get(), find_id(subjects_dict, subject))
                
                messagebox.showinfo(INFO_TITLE, "Preregistro guardado exitosamente!")
            self.default()
        except Exception as err:
            print(f"[-] save: {err}")
            messagebox.showerror(ERROR_TITLE, f"Error al guardar")
    
    #TODO: Obtener estudiante al seleccionar en la tabla
    def get_student(self) -> None:
        selected = self.table.focus()
        if selected is None or selected == "":
            raise Exception("No se encontro el estudiante")
        
        values = self.table.item(selected, "values")
        self.enable_edit()
        self.tx_id.insert(0, values[0])
        self.tx_name.insert(0, values[1])
        self.tx_p_surname.insert(0, values[2])
        self.tx_m_surname.insert(0, values[3])
        self.tx_email.insert(0, values[4])
        self.tx_id.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        self.tx_p_surname.configure(state=DISABLED)
        self.tx_m_surname.configure(state=DISABLED)
        self.tx_email.configure(state=DISABLED)
        
        # Apartir de aqui hacen falta pruebas
        # Obtener la carrera del alumno
        career = db_user_career.get_carreer_by_user(self, values[0])
        self.opm_career.configure(state=ENABLE)
        if career is None or career == "" or career == []:
            self.opm_career.configure(values=self.careers)
            self.opm_career.set("No asignado")
            return
        
        self.opm_career.set(career)
        
        # Obtener el preregistro del alumno
        preregistro: list = db_preregistration.get_subjects_name_by_user(self, values[0])
        
        # Eliminar el contenido anterior
        self.tx_subject.configure(state=ENABLE)
        self.tx_subject.delete(1.0, END)
        
        # Recorrer las materias y añadirlas al textbox
        for subject in preregistro:
            self.tx_subject.insert(1.0, subject + "\n")
        
        self.tx_subject.configure(state=DISABLED)
        
    def edit_student(self) -> None:
        try:
            self.get_student()
        except Exception as err:
            print("[-] ", err)
            messagebox.showerror(ERROR_TITLE, err)
            return
    
    # region Funciones extras
    def _return(self) -> None:
        self.controller.show_frame("Menu")
    
    def clear_student(self):
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_p_surname.configure(state=ENABLE)
        self.tx_m_surname.configure(state=ENABLE)
        self.tx_email.configure(state=ENABLE)
        
        self.tx_id.delete(0, END)
        self.tx_name.delete(0, END)
        self.tx_p_surname.delete(0, END)
        self.tx_m_surname.delete(0, END)
        self.tx_email.delete(0, END)
        self.opm_career.set("")
        self.opm_subject.set("")
        
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_p_surname.configure(state=ENABLE)
        self.tx_m_surname.configure(state=ENABLE)
        self.tx_email.configure(state=ENABLE)
    
    def default(self):
        # Update career and subjects
        if self.type.get_type() == "administrador":
            self.careers = db_carreer.get_all_careers(self)
            self.opm_career.configure(values=self.careers)
            self.opm_career.set(self.careers[0])
        
        self.opm_subject.set("")
        
        self.tx_id.configure(state=ENABLE)
        self.clear_student()
        self.bt_edit.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=ENABLE)
        
        self.tx_subject.configure(state=ENABLE)
        self.tx_subject.delete(1.0, END)
        
        self.tx_id.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        self.tx_p_surname.configure(state=DISABLED)
        self.tx_m_surname.configure(state=DISABLED)
        self.tx_email.configure(state=DISABLED)
        self.opm_career.configure(state=DISABLED)
        self.opm_subject.configure(state=DISABLED)
        self.tx_subject.configure(state=DISABLED)
        
        if self.type.get_type() == "alumno":
            self.table.focus(0)
            self.get_student()
    
    def enable_edit(self):
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        
        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.tx_p_surname.configure(state=ENABLE)
        self.tx_m_surname.configure(state=ENABLE)
        self.tx_email.configure(state=ENABLE)
        if self.type.get_type() == "administrador":
            self.opm_career.configure(state=ENABLE)
        elif self.type.get_type() == "alumno":
            self.opm_subject.configure(state=ENABLE)
        self.clear_student()
    
    # region Tabla
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
            
    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())
        
    def update_table(self) -> None:
        self.clear_table()
        if self.type.get_type() == "administrador":
            students = db_user.get_all_students(self)
        elif self.type.get_type() == "alumno":
            students = db_user.get_student_by_id(self, self.type.get_id())
        self.insert_table(students)
    
    # region Validación
    def validate(self) -> None:
        # Empty
        entry_empty(self.tx_id, "ID")
        
        # Type
        if not self.tx_id.get().isdecimal():
            raise Exception("ID debe ser un número")
        
        if self.opm_career.get() == "No asignado":
            raise Exception("Carrrera no válida")