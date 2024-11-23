from tkinter import messagebox
import mysql.connector as mysql
import database as db
from functions import ERROR_TITLE

table = "subject_career"

class db_subject_career:
    def save(self, subject_id: int, career_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(subject_id, career_id) values (%s,%s)"
            self.data = (
                subject_id,
                career_id
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_subject_career: {err}")
            raise Exception(f"Error al guardar materia-carrera: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def remove(self, subject_id: int, career_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE subject_id={subject_id} AND career_id={career_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_subject_career: {err}")
            raise Exception(f"Error al eliminar materia-carrera: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def remove_by_career(self, career_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE career_id={career_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove_by_career in db_subject_career: {err}")
            raise Exception(f"Error al eliminar las materias asociadas a la carrera: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_all_subject_carreer(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron registros en materia-carrera")
            return rows
        except Exception as err:
            print("[-] get_all_subject_career: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_subjects_by_career_dict(self, career_id: int) -> dict:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT s.id, s.name
                FROM subject_career sc, subject s
                WHERE sc.subject_id = s.id
                AND career_id={career_id}
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            return {row[0]: row[1] for row in rows} if len(rows) > 0 else {}
        except Exception as err:
            print("[-] get_subjects_by_career_dict: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def close(self):
        self.conn.close()