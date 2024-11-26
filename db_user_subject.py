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
    
    def edit(self, user_id: int, subject_id: int, priority: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET priority={priority} WHERE user_id={user_id} AND subject_id={subject_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit in db_user_subject: {err}")
            raise Exception(f"Error al editar usuario-materia: {err}")
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

    def get_teachers_by_subject(self, subject_id: int) -> dict:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT s.name materia, u.name maestro, us.priority
                FROM user_subject us, user u, subject s
                WHERE u.id=us.user_id
                AND us.subject_id=s.id
                AND us.subject_id={subject_id}
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            return rows if rows is not None else ()
        except Exception as err:
            print("[-] get_teachers_by_subject: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_prioritys_by_subject(self, subject_id: int) -> dict:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT user_id, priority FROM {table} WHERE subject_id={subject_id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            return {int(row[0]): int(row[1]) for row in rows} if rows is not None else {}
        except Exception as err:
            print("[-] get_priority_by_subject: ", err)
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
    
    def teacher_priority_by_subject(self, subject_id: int) -> dict:
        try:
            print("subject_id en db_user_subject: ", subject_id)
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            # Obtener prioridades disponibles para la materia de forma ascendente (1, 2, 3, ...)
            self.sql = f"SELECT user_id, priority FROM user_subject WHERE subject_id = {subject_id} ORDER BY priority ASC"
            self.cursor.execute(self.sql)
            priority_rows = self.cursor.fetchall()
            priority_dict = {row[0]: row[1] for row in priority_rows}
            if priority_dict.values() == {}:
                priority_dict = {}
                raise Exception("No hay maestros disponibles para esta materia.")
            return priority_dict
            
        except Exception as err:
            print("[-] teacher_priority_by_subject: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        
        
    def close(self):
        self.conn.close()