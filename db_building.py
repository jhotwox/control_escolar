from tkinter import messagebox
import mysql.connector as mysql
import database as db
from building import building as building_class
from db_functions import max_id
from functions import ERROR_TITLE

table = "building"

class db_building:
    def save(self, building: building_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(id, name) values (%s,%s)"
            self.data = (building.get_id(), building.get_name())
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_building: {err}")
            raise Exception(f"Error al guardar edificio: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def edit(self, building: building_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET name=%s WHERE id={building.get_id()}"
            self.data = (
                building.get_name(),
                )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit in db_building: {err}")
            raise Exception(f"Error al editar edificio: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_max_id(self) -> int:
        return max_id(table)
    
    def get_all_building(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            # self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron edificios")
            return rows
        except Exception as err:
            print("[-] get_all_carrers: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def get_all_building_id(self) -> list:
            try:
                self.conn = db.conection().open()
                self.cursor = self.conn.cursor()
                self.sql = f"SELECT id FROM {table}"
                self.cursor.execute(self.sql)
                rows = self.cursor.fetchall()
                self.conn.commit()
                if rows is None:
                    raise Exception("No se encontraron edificios")
                return [row[0] for row in rows] if len(rows) > 0 else [""]
            except Exception as err:
                print("[-] get_all_building: ", err)
                messagebox.showerror(ERROR_TITLE, "Error en la consulta")
            finally:
                if self.cursor:
                    self.cursor.close()
                if self.conn:
                    self.conn.close()