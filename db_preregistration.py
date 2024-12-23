from tkinter import messagebox
import mysql.connector as mysql
import database as db
from functions import ERROR_TITLE
from db_functions import max_id

TABLE = "pre_registration"

class db_preregistration:
    def save(self, user_id: int, subject_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {TABLE}(user_id, subject_id) values (%s,%s)"
            self.data = (
                user_id,
                subject_id
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_preregistration: {err}")
            raise Exception(f"Error al guardar preregistro: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def remove(self, user_id: int, subject_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {TABLE} WHERE subject_id={subject_id} AND user_id={user_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_preregistration: {err}")
            raise Exception(f"Error al eliminar preregistro: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def remove_all_by_user(self, user_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {TABLE} WHERE user_id={user_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove_all_by_user in db_preregistration: {err}")
            raise Exception(f"Error al eliminar preregistros del estudiante: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_all_preregistration(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {TABLE}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron preregistros")
            return rows
        except Exception as err:
            print("[-] get_all_preregistration: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def get_all_preregistration_dict(self) -> dict:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT subject_id, user_id FROM {TABLE} ORDER BY subject_id ASC"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            return {row[0]: row[1] for row in rows} if rows else {}
        except Exception as err:
            print("[-] get_all_preregistration: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def get_dict_of_list_by_subject(self) -> dict:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            
            # Obtener lista de id de materias de la tabla pre_registration
            self.sql = f"SELECT DISTINCT subject_id FROM {TABLE} ORDER BY subject_id ASC"
            self.cursor.execute(self.sql)
            subjects_list = self.cursor.fetchall()
            subjects_list: list = (subject[0] for subject in subjects_list)
            self.conn.commit()
            
            result = {}
            for subject in subjects_list:
                self.sql = f"SELECT user_id FROM {TABLE} WHERE subject_id={subject}"
                self.cursor.execute(self.sql)
                users = self.cursor.fetchall()
                self.conn.commit()
                users = [user[0] for user in users]
                result[subject] = users
            
            return result if result else {}

        except Exception as err:
            print("[-] get_dict_of_list_by_subject: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_subjects_id_by_user(self, user_id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT subject_id FROM {TABLE} WHERE user_id={user_id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron preregistros")
            return [row[0] for row in rows]
        except Exception as err:
            print("[-] get_preregistration_by_user: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_subjects_name_by_user(self, user_id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT s.name FROM {TABLE} p, subject s WHERE s.id = p.subject_id AND user_id={user_id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                return []
            return [row[0] for row in rows]
        except Exception as err:
            print("[-] get_preregistration_by_user: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_quantity_by_subject(self, subject_id: int) -> int:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT COUNT(*) FROM {TABLE} WHERE subject_id={subject_id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchone()
            self.conn.commit()
            return rows[0] if rows else 0
        except Exception as err:
            print("[-] get_quantity_by_subject: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_max_id(self) -> int:
        return max_id(TABLE)
    
    def close(self):
        self.conn.close()