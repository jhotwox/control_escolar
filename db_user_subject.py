from tkinter import messagebox
import mysql.connector as mysql
import database as db
from functions import ERROR_TITLE

table = "user_subject"

class db_user_subject:
    def save(self, user_id: int, subject_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql1 = f"SELECT MAX(priority) FROM {table} WHERE subject_id={subject_id}"
            self.cursor.execute(self.sql1)
            priority = self.cursor.fetchone()
            priority = 0 if priority[0] is None else priority[0]
            self.cursor.close()
            
            self.cursor = self.conn.cursor()
            self.sql2 = f"INSERT INTO {table}(user_id, subject_id, priority) values (%s, %s, %s)"
            self.data = (
                user_id,
                subject_id,
                priority + 1
            )
            self.cursor.execute(self.sql2, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_user_subject: {err}")
            raise Exception(f"Error al guardar usuario-materia: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def remove(self, user_id: int, subject_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE user_id={user_id} AND subject_id={subject_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_user_subject: {err}")
            raise Exception(f"Error al eliminar usuario-materia: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def remove_all_by_user(self, user_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE user_id={user_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove_all_by_user in db_user_subject: {err}")
            raise Exception(f"Error al eliminar usuario-materia: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_subject_by_user(self, user_id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT s.name
                FROM user_subject us, subject s
                WHERE us.subject_id = s.id
                AND us.user_id={user_id}
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron registros en usuario-materia para este usuario")
            return [row[0] for row in rows]
        except Exception as err:
            print("[-] get_subject_by_user: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_subject_by_user_and_career(self, user_id: int, career_id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT s.name
                FROM user_subject us, subject s, subject_career sc
                WHERE us.subject_id = s.id
                AND s.id = sc.subject_id
                AND sc.career_id={career_id}
                AND us.user_id={user_id};
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron materias para este usuario en la carrera seleccionada")
            return [row[0] for row in rows]
        except Exception as err:
            print("[-] get_subject_by_user_and_career: ", err)
            messagebox.showerror(ERROR_TITLE, "Error obteniendo materias")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_carreer_by_user(self, user_id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT career FROM {table} WHERE user_id={user_id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchone()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontro la materia del usuario")
            return rows
        except Exception as err:
            print("[-] get_carreer_by_user: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_max_priority(self, subject_id: int) -> int:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT max(priority) FROM {table} WHERE subject_id={subject_id}"
            self.cursor.execute(self.sql)
            row = self.cursor.fetchone()
            self.conn.commit()
            if row is None:
                return 0
            return row[0]
        except Exception as err:
            print("[-] get_max_priority: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def close(self):
        self.conn.close()