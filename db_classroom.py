from tkinter import messagebox
import mysql.connector as mysql
import database as db
from classroom import classroom as classroom_class
from db_functions import max_id
from functions import ERROR_TITLE, WARNING_TITLE

table = "classroom"

class db_classroom:
    def save(self, classroom: classroom_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(id, name, building_id) values (%s,%s,%s)"
            self.data = (classroom.get_id(), classroom.get_name(), classroom.get_id_building())
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_classroom: {err}")
            raise Exception(f"Error al guardar salon: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def edit(self, classroom: classroom_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET name=%s, building_id=%s  WHERE id={classroom.get_id()}"
            self.data = (
                classroom.get_name(),
                classroom.get_id_building()
                )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit in db_classroom: {err}")
            raise Exception(f"Error al editar salon: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_all_classromm(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            # self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron salones")
            return rows
        except Exception as err:
            print("[-] get_all_classroom: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def remove(self, classroom: classroom_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={classroom.get_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_classroom: {err}")
            raise Exception(f"Error al eliminar salon: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()