from tkinter import messagebox
import mysql.connector as mysql
import database as db
from career import career as career_class
from db_functions import max_id
from functions import ERROR_TITLE

table = "career"

class db_carreer:
    def save(self, career: career_class) -> None:
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
            print(f"[-] save in db_career: {err}")
            raise Exception(f"Error al guardar carrera: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def edit(self, career: career_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET name=%s WHERE id={career.get_id()}"
            self.data = (
                career.get_name(),
                )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit in db_career: {err}")
            raise Exception(f"Error al editar carrera: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_all_careers(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT name FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron carreras")
            return [row[0] for row in rows] if len(rows) > 0 else [""]
        except Exception as err:
            print("[-] get_all_carrers: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    # Esta función es para el crud de carreras, la anterior solo devuelve los nombres
    def get_all_careers_for_career(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron carreras")
            return rows
        except Exception as err:
            print("[-] get_all_carrers: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def get_all_careers_dict(self) -> dict:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT id, name FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron carreras")
            return {row[0]: row[1] for row in rows} if len(rows) > 0 else {0: ""}
        except Exception as err:
            print("[-] get_all_carrers_dict: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            
    def get_carrer_by_id(self, id: int) -> career_class:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table} WHERE id={id}"
            self.cursor.execute(self.sql)
            row = self.cursor.fetchone()
            self.conn.commit()
            if row is None:
                raise Exception("No se encontro la carrera")
            return career_class(int(row[0]), row[1])
        except Exception as err:
            print("[-] get_career_by_id: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def get_id_by_name(self, name: str) -> int:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            # print("get_id_by_name: name ->", name)
            self.sql = f"SELECT id FROM {table} WHERE name='{name}'"
            self.cursor.execute(self.sql)
            row = self.cursor.fetchone()
            self.conn.commit()
            if row is None:
                raise Exception("No se encontro el id de la carrera")
            return row[0]
        except Exception as err:
            print("[-] get_id_by_name: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def close(self):
        self.conn.close()