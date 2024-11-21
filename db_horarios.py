from tkinter import messagebox
import mysql.connector as mysql
import database as db
from horario import Horario as horario_class
from db_functions import max_id
from functions import ERROR_TITLE, WARNING_TITLE

table = "schedule"

class db_horarios:    
    def save(self, schedule: horario_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(id, day, start_time, end_time) values (%s,%s,%s,%s)"
            self.data = (
                schedule.get_id(),
                schedule.get_day(),
                schedule.get_start_time(),
                schedule.get_end_time(),
                schedule.get_type()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_horarios: {err}")
            raise Exception(f"Error al guardar horarios: {err}")
        finally:
            self.conn.close()
    
    def edit(self, shedule: horario_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET day=%s, start_time=%s, end_time=%s, WHERE id={shedule.get_id()}"
            self.data = (
                shedule.get_day(),
                shedule.get_start_time(),
                shedule.get_end_time()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit in db_horarios: {err}")
            raise Exception(f"Error al editar horarios: {err}")
        finally:
            self.conn.close()
        
    def remove(self, shedule: horario_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={shedule.get_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_horarios: {err}")
            raise Exception(f"Error al eliminar usuario: {err}")
        finally:
            self.conn.close()
        
    def get_max_id(self) -> int:
        return max_id(table)
    
    def get_all_horarios(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron horarios")
            return rows
        except Exception as err:
            print("[-] get_all_horarios: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            self.conn.close()
            
    def get_horario_by_id(self, id: int) -> horario_class:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table} WHERE id={id}"
            self.cursor.execute(self.sql)
            row = self.cursor.fetchone()
            self.conn.commit()
            if row is None:
                raise Exception("No se encontro el usuario")
            return horario_class(int(row[0]), row[1], row[2], row[3])
        except Exception as err:
            print("[-] get_horario_by_id: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            self.conn.close()
        
    def close(self):
        self.conn.close()