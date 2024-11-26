from customtkinter import END, CTkButton as Button, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar,  CTkTextbox as Textbox
from tkinter import messagebox
from functions import find_id, INFO_TITLE, WARNING_TITLE, ERROR_TITLE
from db_career import db_carreer
from career import career as career_class
from db_subject_career import db_subject_career
from db_subject import db_subject

class Subjects_Careers(Frame):
    # region Interfaz
    def __init__(self, container, controller, type: career_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.controller = controller
        self.band = False
        
        fr_entry = Frame(self)
        fr_entry.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        fr_button = Frame(self)
        fr_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)


        self.careers: dict = {}
        self.lb_career = Label(fr_entry, text="Carrera")
        self.lb_career.grid(row=0, column=0, pady=0, sticky="w")
        self.selected_career = StringVar(value="")
        self.selected_career.trace("w", self.on_selection_carreer)
        self.opm_career = OptMenu(fr_entry, values=(self.careers.values()), variable=self.selected_career)
        self.opm_career.grid(row=0, column=1, pady=5)
        
        self.tx_subject = Textbox(fr_entry, width=200, height=150)
        self.tx_subject.grid(row=0, column=2, columnspan=2, rowspan=3, pady=5)
        
        self.subjects: dict = {}
        self.lb_subject = Label(fr_entry, text="Materia")
        self.lb_subject.grid(row=1, column=0, pady=0, sticky="w")
        self.selected_subject = StringVar(value="")
        self.selected_subject.trace("w", self.on_selection_subject)
        self.opm_subject = OptMenu(fr_entry, values=(self.subjects.values()), variable=self.selected_subject)
        self.opm_subject.grid(row=1, column=1, pady=5)
        
        
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_subject_career)
        self.bt_save.grid(row=0, column=0, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=1, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=2, padx=5, pady=10)

        self.default()

    # region Funciones SQL
    def on_selection_carreer(self, *args) -> None:
        career_name = self.opm_career.get()        
        if career_name == "" or career_name is None:
            return
        
        career_id = find_id(self.careers, career_name)
        
        # Eliminar el contenido anterior
        self.tx_subject.configure(state=ENABLE)
        self.tx_subject.delete(1.0, END)
        
        # Obtener materias asignadas a la carrera seleccionada
        assigned_subjects = db_subject_career.get_subjects_by_career_dict(self, career_id)
        
        # Recorrer las materias y añadirlas al textbox
        for subject in assigned_subjects.values():
            self.tx_subject.insert(1.0, subject + "\n")
        
        self.tx_subject.configure(state=DISABLED)
        self.opm_subject.configure(state=ENABLE)

    def on_selection_subject(self, *args) -> None:
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
    
    def save_subject_career(self) -> None:
        try:
            self.validate()  # Llamada a la validación general
        except Exception as error:
            messagebox.showwarning(WARNING_TITLE, error)
            return
        
        try:
            db_subject_career.remove_by_career(self, find_id(self.careers, self.opm_career.get()))
            for subject in self.get_subjects_from_tb():
                db_subject_career.save(self, find_id(self.subjects, subject), find_id(self.careers, self.opm_career.get()))
            messagebox.showinfo(INFO_TITLE, "Materias asignadas exitosamente!")
            self.default()
        except Exception as err:
            print(f"[-] saveSubject: {err}")
            messagebox.showerror(ERROR_TITLE, f"Error al asociar materias a la carrera en la BD")
    
    # region Funciones extras
    def _return(self) -> None:
        self.controller.show_frame("Menu")

    def clear_subject_career(self):
        self.opm_career.set("")
        self.opm_subject.set("")
        self.tx_subject.configure(state=ENABLE)
        self.tx_subject.delete(1.0, END)
        self.tx_subject.configure(state=DISABLED)

    def default(self):
        # Obtener todas las carreras
        self.careers = db_carreer.get_all_careers_dict(self)
        self.opm_career.configure(values=(self.careers.values()))
        self.opm_career.set("")
        
        self.subjects = db_subject.get_subjects_dict(self)
        self.opm_subject.configure(values=(self.subjects.values()))
        self.opm_subject.set("")
        
        self.tx_subject.delete(1.0, END)
        
        self.clear_subject_career()
        
        self.opm_career.configure(state=ENABLE)
        self.opm_subject.configure(state=DISABLED)
        self.tx_subject.configure(state=DISABLED)

        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_return.configure(state=ENABLE)


    # region Validación
    def validate(self) -> None:
        subjects = self.get_subjects_from_tb()
        for subject in subjects:
            if subject not in self.subjects.values():
                raise Exception(f"La materia {subject} no existe")