from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar, CTk
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, is_alphabetic, find_id, validate_email, INFO_TITLE, WARNING_TITLE, ERROR_TITLE
from db_horarios import db_horarios
from horario import Horario as horario_class
from table_style import apply_style
from db_functions import email_available
from constants import TYPE
from user import user as teacher_class

#region Interfaz
class Horario(Frame):
    # region Interfaz
    def __init__(self, container, controller, type: teacher_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.controller = controller
        self.band = False
        self.type = type
        
        fr_search = Frame(self)
        fr_search.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        fr_entry = Frame(self)
        fr_entry.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)
        fr_table = Frame(self)
        fr_table.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        fr_button = Frame(self)
        fr_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        # Sección de búsqueda
        self.lb_search = Label(fr_search, text="ID a buscar: ", font=("Calisto MT", 12))
        self.lb_search.grid(row=0, column=0, padx=5)
        self.tx_search = Entry(fr_search, placeholder_text="ID a buscar", width=200)
        self.tx_search.grid(row=0, column=1, padx=10, pady=10)
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_horario)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        # Campos de entrada
        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0, sticky="w")
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)

        self.lb_dia = Label(fr_entry, text="Dia")
        self.lb_dia.grid(row=1, column=0, pady=0, sticky="w")
        self.tx_dia = Entry(fr_entry, placeholder_text="Dia")
        self.tx_dia.grid(row=1, column=1, pady=5, padx=20)
        
        self.lb_hora_inicio = Label(fr_entry, text="Hora de inicio")
        self.lb_hora_inicio.grid(row=1, column=2, pady=0, sticky="w")
        self.tx_hora_inicio = Entry(fr_entry, placeholder_text="Hora de inicio")  # Corregido de tx_email a tx_hora
        self.tx_hora_inicio.grid(row=1, column=3, pady=5, padx=20)

        self.lb_hora_fin = Label(fr_entry, text="Hora de fin")
        self.lb_hora_fin.grid(row=3, column=0, pady=0, sticky="w")
        self.tx_hora_fin = Entry(fr_entry, placeholder_text="Hora de fin")
        self.tx_hora_fin.grid(row=3, column=1, pady=5, padx=20)
        
        frame = Frame(fr_table)
        frame.grid(row=0, column=0, sticky="nsew")
        
        scroll_y = Scrollbar(frame)
        scroll_y.grid(row=0, column=1, sticky="ns")  # Desplazamiento vertical
        
        scroll_x = Scrollbar(frame, orientation="horizontal")
        scroll_x.grid(row=1, column=0, sticky="ew")  # Desplazamiento horizontal
        
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
        
        self.table['columns'] = ("ID","Dia","Hora de inicio","Hora de fin")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=30)
        self.table.column("Dia", anchor="center", width=150)
        self.table.column("Hora de inicio", anchor="center", width=150)
        self.table.column("Hora de fin", anchor="center", width=150)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Dia", text="Dia", anchor="center")
        self.table.heading("Hora de inicio", text="Hora de inicio", anchor="center")
        self.table.heading("Hora de fin", text="Hora de fin", anchor="center")
        
        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_horario)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_horario)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_horario)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_horario)  # Corregido aquí
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        self.bt_update = Button(fr_button, text="Actualizar", border_width=1, width=60, command=self.update_table)
        self.bt_update.grid(row=0, column=5, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=6, padx=5, pady=10)
        
        self.default()
        self.update_table()

    #region Funciones DB
    def edit_horario(self):
        try:
            self.get_horario()
        except Exception as err:
            print("[-] ", err)
            messagebox.showerror(ERROR_TITLE, err)
            return
        self.band = False

    def new_horario(self) -> None:
        self.tx_id.configure(state=ENABLE)
        self.tx_dia.configure(state=ENABLE)
        self.tx_hora_inicio.configure(state=ENABLE)
        self.tx_hora_fin.configure(state=ENABLE)
        
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.clear_horario()
        self.tx_id.insert(0, db_horarios.get_max_id(self)+1)
        self.tx_id.configure(state=DISABLED)
        self.band = True
        return

    def remove_horario(self):
        print("Eliminar horario")
        return

    def update_table(self):
        return

    def _return(self):
        self.controller.show_frame("Menu")

    def default(self):
        self.tx_id.delete(0, END)
        self.tx_Turno.delete(0, END)
        self.tx_Hora.delete(0, END)

    def search_user(self) -> None:
        if not self.tx_search.get().isdecimal():
            messagebox.showwarning(ERROR_TITLE, "Ingrese un ID válido")
            return
        
        def search_id():
            for item in self.table.get_children():
                item_values = self.table.item(item, "values")

                if item_values[0] == self.tx_search.get():
                    return item
            return None
        
        id = search_id()
        if id is None:
            messagebox.showwarning(WARNING_TITLE, "No se encontró el horario")
            return
        
        self.table.selection_set(id)
        self.table.focus(id)
        return id
    
    def remove_horario(self):  # Método para eliminar horario
        try:
            selected = self.table.focus()
            if selected is None or selected == "":
                messagebox.showwarning(WARNING_TITLE, "No se selecciono un Horario")
                return
            
            values = self.table.item(selected, "values")
            aux = horario_class(id=int(values[0]))
            db_horarios.remove(self, aux)
            messagebox.showinfo(INFO_TITLE, "Horario eliminado")
            self.update_table()
            self.default()
        except Exception as err:
            print("[-] remove_horario", err)
            messagebox.showerror(ERROR_TITLE, "No se logro eliminar el Horario")
    #region Funciones Extras
    def _return(self) -> None:
        self.controller.show_frame("Menu")

    def clear_horario(self):
        self.tx_id.delete(0, END)
        self.tx_dia.delete(0, END)
        self.tx_hora_inicio.delete(0, END)
        self.tx_hora_fin.delete(0, END)

    def default(self):
        self.tx_id.configure(state=ENABLE)
        self.clear_horario()
        self.bt_edit.configure(state=ENABLE)
        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_remove.configure(state=ENABLE)
        
        self.tx_id.configure(state=DISABLED)
        self.tx_dia.configure(state=DISABLED)
        self.tx_hora_inicio.configure(state=DISABLED)
        self.tx_hora_fin.configure(state=DISABLED)

    def enable_edit(self):
        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)
        self.bt_edit.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        
        self.tx_id.configure(state=ENABLE)
        self.tx_dia.configure(state=ENABLE)
        self.tx_hora_inicio.configure(state=ENABLE)
        self.tx_hora_fin.configure(state=ENABLE)
        self.clear_horario()

    def _return(self):
        self.controller.show_frame("Menu")

    #region Tabla
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)
            
    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())
        
    def update_table(self) -> None:
        self.clear_table()
        Horario = db_horarios.get_all_horarios(self)
        self.insert_table(Horario)
    
    
    def validate(self) -> None:
        # Empty
        entry_empty(self.tx_dia, "Día")
        entry_empty(self.tx_hora_inicio, "Hora de inicio")
        entry_empty(self.tx_hora_fin, "Hora de fin")
    
        # Validación de día
        if not self.tx_dia.get().isdigit() or not (0 <= int(self.tx_dia.get()) <= 5):
            raise Exception("El día debe ser un número entre 0 y 5 (0 para Lunes, 5 para Sabado)")
    
        # Validación del formato de hora
        def validate_time_format(time_str: str) -> bool:
            try:
                hour, minute = map(int, time_str.split(":"))
                return 0 <= hour < 24 and 0 <= minute < 60
            except ValueError:
                return False
    
        if not validate_time_format(self.tx_hora_inicio.get()):
            raise Exception("La hora de inicio debe tener el formato HH:MM de 24 horas (ejemplo: 09:00)")
    
        if not validate_time_format(self.tx_hora_fin.get()):
            raise Exception("La hora de fin debe tener el formato HH:MM de 24 horas (ejemplo: 13:00)")
    
            # Validación de la duración del horario
        from datetime import datetime, timedelta
    
        start_time = datetime.strptime(self.tx_hora_inicio.get(), "%H:%M")
        end_time = datetime.strptime(self.tx_hora_fin.get(), "%H:%M")
        duration = end_time - start_time
    
        if duration < timedelta(hours=2):
            raise Exception("El horario debe tener una duración mínima de 2 horas")
    
        if duration > timedelta(hours=4):
            raise Exception("El horario debe tener una duración máxima de 4 horas")
