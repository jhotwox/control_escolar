from customtkinter import END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, DISABLED, NORMAL as ENABLE, CTkFrame as Frame, CTkOptionMenu as OptMenu, StringVar, CTkScrollbar as Scrollbar
from tkinter import messagebox
from tkinter.ttk import Treeview
from functions import entry_empty, is_alphabetic, find_id, validate_email, INFO_TITLE, WARNING_TITLE, ERROR_TITLE
from db_classroom import db_classroom
from classroom import classroom as classroom_class
from db_building import db_building
from db_subject import db_subject
from table_style import apply_style

class Classrooms(Frame):
    # region Interfaz
    def __init__(self, container, controller, type: classroom_class, *args, **kwargs):
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
        self.tx_search.grid(row=0, column=1,  padx=10, pady=10)
        self.bt_search = Button(fr_search, text="Buscar", border_width=2, width=100, command=self.search_classroom)
        self.bt_search.grid(row=0, column=2, padx=5, pady=10)

        self.lb_id = Label(fr_entry, text="ID")
        self.lb_id.grid(row=0, column=0, pady=0, sticky="w")
        self.tx_id = Entry(fr_entry, placeholder_text="ID")
        self.tx_id.grid(row=0, column=1, pady=5)

        self.lb_name = Label(fr_entry, text="Nombre")
        self.lb_name.grid(row=1, column=0, pady=0, sticky="w")
        self.tx_name = Entry(fr_entry, placeholder_text="Nombre")
        self.tx_name.grid(row=1, column=1, pady=5, padx=20)

        self.lb_building = Label(fr_entry, text="Edificio")
        self.lb_building.grid(row=2, column=0, pady=0, sticky="w")

        self.updated_buildings = [str(id) for id in db_building.get_all_building_name(self)]
        self.selected_type = StringVar(value="----")  # Valor por defecto
        self.opm_type = OptMenu(fr_entry, values=self.updated_buildings, variable=self.selected_type)
        self.opm_type.grid(row=2, column=1, pady=5)

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

        self.table['columns'] = ("ID", "Nombre", "Nombre_edificio")
        self.table.column("#0", width=0, stretch=False)
        self.table.column("ID", anchor="center", width=30)
        self.table.column("Nombre", anchor="center", width=150)
        self.table.column("Nombre_edificio", anchor="center", width=200)
        
        self.table.heading("#0", text="", anchor="center")
        self.table.heading("ID", text="ID", anchor="center")
        self.table.heading("Nombre", text="Nombre", anchor="center")
        self.table.heading("Nombre_edificio", text="Nombre del edificio", anchor="center")

        self.bt_new = Button(fr_button, text="Nuevo", border_width=1, width=60, command=self.new_classroom)
        self.bt_new.grid(row=0, column=0, padx=5, pady=10)
        self.bt_save = Button(fr_button, text="Salvar", border_width=1, width=60, command=self.save_classroom)
        self.bt_save.grid(row=0, column=1, padx=5, pady=10)
        self.bt_cancel = Button(fr_button, text="Cancelar", border_width=1, width=60, command=self.default)
        self.bt_cancel.grid(row=0, column=2, padx=5, pady=10)
        self.bt_edit = Button(fr_button, text="Editar", border_width=1, width=60, command=self.edit_classroom)
        self.bt_edit.grid(row=0, column=3, padx=5, pady=10)
        self.bt_remove = Button(fr_button, text="Eliminar", border_width=1, width=60, command=self.remove_classroom)
        self.bt_remove.grid(row=0, column=4, padx=5, pady=10)
        self.bt_update = Button(fr_button, text="Actualizar", border_width=1, width=60, command=self.update_building_options)
        self.bt_update.grid(row=0, column=5, padx=5, pady=10)
        self.bt_return = Button(fr_button, text="Regresar", border_width=1, width=60, command=self._return)
        self.bt_return.grid(row=0, column=6, padx=5, pady=10)

        self.default()
        self.update_table()

    # region Funciones SQL
    def update_building_options(self):
    # Obtener los IDs de edificios actualizados desde la base de datos
        self.updated_buildings = [str(id) for id in db_building.get_all_building_name(self)]

        # Actualizar el contenido del OptionMenu
        self.opm_type.configure(values=self.updated_buildings)

    def search_classroom(self) -> None:
        if not self.tx_search.get().isdecimal():
            messagebox.showwarning(ERROR_TITLE, "Ingrese un ID valido")
            return
        
        def search_id():
            for item in self.table.get_children():
                item_values = self.table.item(item, "values")
                
                if item_values[0] == self.tx_search.get():
                    return item
            return None
        
        id = search_id()
        if id is None:
            messagebox.showwarning(WARNING_TITLE, "No se encontro el salon")
            return
        
        self.table.selection_set(id)
        self.table.focus(id)
        self.table.see(id)
    
    def remove_classroom(self) -> None:
        try:
            selected = self.table.focus()
            if selected is None or selected == "":
                messagebox.showwarning(WARNING_TITLE, "No se selecciono un salon")
                return
            
            values = self.table.item(selected, "values")
            aux = classroom_class(id=int(values[0]))
            db_classroom.remove(self, aux)
            messagebox.showinfo(INFO_TITLE, "Salon eliminado")
            self.update_table()
            self.default()
        except Exception as err:
            print("[-] remove_salon", err)
            messagebox.showerror(ERROR_TITLE, "No se logro eliminar el salon")

    def new_classroom(self) -> None:
        self.tx_search.configure(state=DISABLED)
        self.bt_search.configure(state=DISABLED)

        self.tx_id.configure(state=ENABLE)
        self.tx_name.configure(state=ENABLE)
        self.opm_type.configure(state=ENABLE)

        self.bt_new.configure(state=DISABLED)
        self.bt_save.configure(state=ENABLE)
        self.bt_cancel.configure(state=ENABLE)    
        self.bt_edit.configure(state=DISABLED)
        self.bt_update.configure(state=DISABLED)
        self.bt_remove.configure(state=DISABLED)
        self.bt_return.configure(state=DISABLED)

        self.clear_classroom()
        next_id = db_subject.get_max_id_from_table(self)
        self.tx_id.insert(0, next_id)
        self.tx_id.configure(state=DISABLED)
        self.band = True
        return

    def save_classroom(self) -> None:
        try:
            self.validate()  # Llamada a la validación general
        except Exception as error:
            messagebox.showwarning(WARNING_TITLE, error)
            return
        
        try:
            salones = classroom_class(
                int(self.tx_id.get()),
                self.tx_name.get(),
                db_building.get_building_by_name(self, self.opm_type.get())
            )

            if self.band == True:
                db_classroom.save(self, salones)
                messagebox.showinfo(INFO_TITLE, "Salon guardado exitosamente!")
            else:
                db_classroom.edit(self, salones)
                messagebox.showinfo(INFO_TITLE, "Salon editado exitosamente!")
            self.default()
            self.update_table()
        except Exception as err:
            print(f"[-] saveClassroom: {err}")
            messagebox.showerror(ERROR_TITLE, f"Error al {'guardar' if self.band else 'editar'} Salon en BD")
        finally:
            self.band = None

    def get_classroom(self) -> None:
        selected = self.table.focus()
        if selected is None or selected == "":
            raise Exception("No se encontro el salon")
        
        values = self.table.item(selected, "values")
        self.enable_edit()
        self.tx_id.insert(0, values[0])
        self.tx_name.insert(0, values[1])
        self.opm_type.set(values[2])
        self.tx_id.configure(state=DISABLED)

    def edit_classroom(self) -> None:
        try:
            self.get_classroom()
        except Exception as err:
            print("[-] ", err)
            messagebox.showerror(ERROR_TITLE, err)
            return
        
        self.band = False

    # region Funciones extras
    def _return(self) -> None:
        self.controller.show_frame("Menu")

    def clear_classroom(self):
        self.tx_id.delete(0, END)
        self.tx_name.delete(0, END)
        self.opm_type.set("----")

    def default(self):
        self.tx_id.configure(state=ENABLE)
        self.clear_classroom()
        self.tx_search.configure(state=ENABLE)
        self.bt_search.configure(state=ENABLE)

        self.tx_id.configure(state=DISABLED)
        self.tx_name.configure(state=DISABLED)
        self.opm_type.configure(state=DISABLED)

        self.bt_new.configure(state=ENABLE)
        self.bt_save.configure(state=DISABLED)
        self.bt_cancel.configure(state=DISABLED)
        self.bt_edit.configure(state=ENABLE)
        self.bt_update.configure(state=ENABLE)
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
        self.opm_type.configure(state=ENABLE)
        self.clear_classroom()

    #region Tabla
    def insert_table(self, data: list) -> None:
        for i, row in enumerate(data):
            self.table.insert("", "end", iid=i, values=row)

    def clear_table(self) -> None:
        self.table.delete(*self.table.get_children())

    def update_table(self) -> None:
        self.clear_table()
        classrooms = db_classroom.get_all_classroom(self)

        # Convertir IDs de edificios a nombres
        updated_classrooms = []
        for classroom in classrooms:
            id_classroom, name_classroom, id_building = classroom
            building_name = db_building.get_building_name_by_id(self, id_building)
            updated_classrooms.append((id_classroom, name_classroom, building_name))

        self.insert_table(updated_classrooms)

    # region Validación
    def validate(self) -> None:
        # Validar campos vacíos
        entry_empty(self.tx_id, "ID")
        entry_empty(self.tx_name, "Nombre")

        # Verificar longitud del nombre
        if len(self.tx_name.get()) > 20:
            raise Exception("El nombre del salón es demasiado largo")

        # Verificar que se haya seleccionado un edificio
        if self.opm_type.get() == "----":
            raise Exception("Debe seleccionar un edificio")

        # Verificar duplicados en el mismo edificio
        classroom_name = self.tx_name.get().strip()
        building_id = self.opm_type.get()

        for item in self.table.get_children():
            item_values = self.table.item(item, "values")
            
            # Saltar el registro actual en caso de edición
            if item_values[0] == self.tx_id.get():
                continue
            
            # Comparar nombre y edificio
            if (
                item_values[1].strip().lower() == classroom_name.lower() and
                item_values[2] == building_id
            ):
                raise Exception("Ya existe un salón con este nombre en el edificio seleccionado.")
