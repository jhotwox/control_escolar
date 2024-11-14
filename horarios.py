from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, is_alphabetic, find_id, validate_email, INFO_TITLE, WARNING_TITLE, ERROR_TITLE
from db_horarios import db_horarios
from horario import Horario as horario_class
from table_style import apply_style
from db_functions import email_available
from constants import TYPE    

class Horario(Frame):
    # region Interfaz
    def __init__(self, container, controller, horario_class_type: horario_class, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.controller = controller
        self.band = False
        self.horario_class_type = horario_class_type
        
        self.TYPE_DICT = TYPE
        
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
        self.tx_search = Entry(fr_search, width=200)
        self.tx_search.grid(row=0, column=1, padx=10, pady=10)
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_user)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0, sticky="w")
        self.tx_id = Entry(fr_entry)
        self.tx_id.grid(row=0, column=1, pady=5)

        self.lb_Turno = Label(fr_entry, text="Turno")
        self.lb_Turno.grid(row=1, column=0, pady=0, sticky="w")
        self.tx_Turno = Entry(fr_entry)
        self.tx_Turno.grid(row=1, column=1, pady=5, padx=20)
        
        self.lb_Hora = Label(fr_entry, text="Hora")
        self.lb_Hora.grid(row=1, column=2, pady=0, sticky="w")
        self.tx_Hora = Entry(fr_entry)
        self.tx_Hora.grid(row=1, column=3, pady=5, padx=20)

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
        
        self.table['columns'] = ("ID", "Turno", "Hora")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=30)
        self.table.column("Turno", anchor="center", width=150)
        self.table.column("Hora", anchor="center", width=150)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Turno", text="Turno", anchor="center")
        self.table.heading("Hora", text="Hora", anchor="center")
        
        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_horario)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_horario)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_horario)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_horario)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        self.bt_update = Button(fr_button, text="Actualizar", border_width=1, width=60, command=self.update_table)
        self.bt_update.grid(row=0, column=5, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=6, padx=5, pady=10)
        
        self.default()
        self.update_table()

    #region Funciones SQL
    def new_horario(self):
        print("Nuevo horario")
        return

    def save_horario(self):
        print("Guardar horario")
        return

    def edit_horario(self):
        print("Editar horario")
        return

    def remove_horario(self):
        print("Eliminar horario")
        return

    def update_table(self):
        print("Actualizar tabla")
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
            messagebox.showwarning(WARNING_TITLE, "No se encontro el horario")
            return
        
        self.table.selection_set(id)
        self.table.focus(id)
        self.table.see(id)