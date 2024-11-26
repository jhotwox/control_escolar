from tkinter import messagebox
import mysql.connector as mysql
import database as db
from user import user as teacher_class
from db_functions import max_id
from functions import ERROR_TITLE, WARNING_TITLE

table = "classroom"

class db_classroom:
    
    def get_classroom_dict(self) -> dict:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT id, name FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            return {row[0]: row[1] for row in rows} if len(rows) > 0 else {0: ""}
        except Exception as err:
            print("[-] get_classroom_dict: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()