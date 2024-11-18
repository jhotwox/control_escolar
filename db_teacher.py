from tkinter import messagebox
import mysql.connector as mysql
import database as db
from user import user as teacher_class
from teacher import teacher as teacher_class
from functions import ERROR_TITLE

table = "teacher"

class db_teacher:    
    def save(self, teacher: teacher_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(id, cedula) values (%s,%s)"
            self.data = (
                teacher.get_id(),
                teacher.get_cedula()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_teacher: {err}")
            raise Exception(f"Error al guardar maestro: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def edit(self, teacher: teacher_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET cedula=%s WHERE id={teacher.get_id()}"
            self.data = (teacher.get_cedula())
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit in db_teacher: {err}")
            raise Exception(f"Error al editar maestro: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        
    def remove(self, teacher: teacher_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={teacher.get_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_teacher: {err}")
            raise Exception(f"Error al eliminar maestro: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_all_teachers(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = """
                SELECT id, name, p_surname, m_surname, email
                FROM user
                WHERE type='maestro';
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron maestros")
            return rows
        except Exception as err:
            print("[-] get_all_teachers: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            
    def get_teacher_by_id(self, id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT id, name, p_surname, m_surname, email
                FROM user
                WHERE type='maestro'
                AND id={id}
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontro el maestro")
            return rows
        except Exception as err:
            print("[-] get_teacher_by_id: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_cedula_by_id(self, id: int) -> str:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT cedula
                FROM {table}
                WHERE id={id}
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchone()
            self.conn.commit()
            return None if rows is None else rows[0]
        except Exception as err:
            print("[-] get_cedula_by_id: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def close(self):
        self.conn.close()