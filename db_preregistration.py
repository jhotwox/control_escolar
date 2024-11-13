from tkinter import messagebox
import mysql.connector as mysql
import database as db
from functions import ERROR_TITLE

table = "pre_registration"

class db_preregistration:
    def save(self, user_id: int, subject_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(user_id, subject_id) values (%s,%s)"
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
            self.conn.close()
    
    def remove(self, user_id: int, subject_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE subject_id={subject_id} AND user_id={user_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_preregistration: {err}")
            raise Exception(f"Error al eliminar preregistro: {err}")
        finally:
            self.conn.close()

    def remove_all_by_user(self, user_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE user_id={user_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove_all_by_user in db_preregistration: {err}")
            raise Exception(f"Error al eliminar preregistros del estudiante: {err}")
        finally:
            self.conn.close()
    
    def get_all_preregistration(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
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
            self.conn.close()
    
    def get_subject_id_by_user(self, user_id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT subject_id FROM {table} WHERE user_id={user_id}"
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
            self.conn.close()
    
    #TODO: No esta bien hecho
    def get_subject_name_by_user(self, user_id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT subject_name FROM {table} WHERE user_id={user_id}"
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
            self.conn.close()
                
    def close(self):
        self.conn.close()