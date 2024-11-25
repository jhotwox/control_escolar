from tkinter import messagebox
import mysql.connector as mysql
import database as db
from subject import subject as subject_class
from db_functions import max_id
from functions import ERROR_TITLE

table = "subject"

class db_subject:
    def save(self, career: subject_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(id, name) values (%s,%s)"
            self.data = (
                career.get_id(),
                career.get_name()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_subject: {err}")
            raise Exception(f"Error al guardar materia: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def edit(self, career: subject_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET name=%s WHERE id={career.get_id()}"
            self.data = (career.get_name(),)
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit in db_subject: {err}")
            raise Exception(f"Error al editar materia: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def remove(self, career: subject_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={career.get_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_subject: {err}")
            raise Exception(f"Error al eliminar materia: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_max_id_from_table(self) -> int:
        max_id = 0
        for item in self.table.get_children():
            item_values = self.table.item(item, "values")
            current_id = int(item_values[0])
            max_id = max(max_id, current_id)
        return max_id + 1
    
    def get_all_subjects(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron materias")
            return rows
        except Exception as err:
            print("[-] get_all_subjects: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            
    def get_subject_by_id(self, id: int) -> subject_class:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table} WHERE id={id}"
            self.cursor.execute(self.sql)
            row = self.cursor.fetchone()
            self.conn.commit()
            if row is None:
                raise Exception("No se encontro la materia")
            return subject_class(int(row[0]), row[1])
        except Exception as err:
            print("[-] get_subject_by_id: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_subjects_by_career(self, career_id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT s.name subject
                FROM subject_career sc, subject s
                WHERE sc.subject_id = s.id
                AND career_id={career_id}
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron materias")
            return [row[0] for row in rows] if len(rows) > 0 else [""]
        except Exception as err:
            print("[-] get_subjects_by_career: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_subjects_dict(self) -> dict:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT s.id, s.name
                FROM subject s
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron materias")
            return {row[0]: row[1] for row in rows} if len(rows) > 0 else {}
        except Exception as err:
            print("[-] get_subjects_dict: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_subjects_in_subject_career_dict(self) -> dict:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT s.id, s.name
                FROM subject_career sc, subject s
                WHERE sc.subject_id = s.id
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron materias")
            return {row[0]: row[1] for row in rows} if len(rows) > 0 else {0: ""}
        except Exception as err:
            print("[-] get_subjects_dict_in_subject_career_dict: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def close(self):
        self.conn.close()