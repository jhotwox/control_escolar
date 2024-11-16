from tkinter import messagebox
import mysql.connector as mysql
import database as db
from functions import ERROR_TITLE

table = "user_career"

class db_user_career:
    def save(self, user_id: int, career_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(user_id, career_id) values (%s,%s)"
            self.data = (
                user_id,
                career_id
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_user_career: {err}")
            raise Exception(f"Error al guardar usuario-carrera: {err}")
        finally:
            self.conn.close()
    
    def remove(self, user_id: int, career_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE user_id={user_id} AND career_id={career_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_user_career: {err}")
            raise Exception(f"Error al eliminar usuario-carrera: {err}")
        finally:
            self.conn.close()

    def remove_by_user(self, user_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE user_id={user_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove_by_user in db_user_career: {err}")
            raise Exception(f"Error al eliminar usuario-carrera: {err}")
        finally:
            self.conn.close()
    
    def get_all_user_carreer(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron registros en usuario-carrera")
            return rows
        except Exception as err:
            print("[-] get_all_user_career: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            self.conn.close()
    
    def get_carreer_by_user(self, user_id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT c.name
                FROM {table} uc, career c
                WHERE uc.career_id = c.id
                AND user_id={user_id}
                """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchone()
            self.conn.commit()
            return rows[0] if rows is not None else ""
        except Exception as err:
            print("[-] get_carreer_by_user: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            self.conn.close()
    
    def close(self):
        self.conn.close()