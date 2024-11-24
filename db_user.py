from tkinter import messagebox
import mysql.connector as mysql
import database as db
from user import user as user_class
from db_functions import max_id
from functions import ERROR_TITLE, WARNING_TITLE

table = "user"

class db_user:    
    def save(self, user: user_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {table}(id, name, p_surname, m_surname, password, email, type) values (%s,%s,%s,%s,%s,%s,%s)"
            self.data = (
                user.get_id(),
                user.get_name(),
                user.get_p_surname(),
                user.get_m_surname(),
                user.get_password(),
                user.get_email(),
                user.get_type()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_user: {err}")
            raise Exception(f"Error al guardar usuario: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def edit(self, user: user_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"UPDATE {table} SET name=%s, p_surname=%s, m_surname=%s, email=%s, type=%s, password=%s WHERE id={user.get_id()}"
            self.data = (
                user.get_name(),
                user.get_p_surname(),
                user.get_m_surname(),
                user.get_email(),
                user.get_type(),
                user.get_password()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except Exception as err:
            print(f"[-] edit in db_user: {err}")
            raise Exception(f"Error al editar usuario: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        
    def remove(self, user: user_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {table} WHERE id={user.get_id()}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_user: {err}")
            raise Exception(f"Error al eliminar usuario: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        
    def get_max_id(self) -> int:
        return max_id(table)
    
    def get_all_users(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron usuarios")
            return rows
        except Exception as err:
            print("[-] get_all_users: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_all_students(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT id, u.name, u.p_surname, u.m_surname, u.email FROM {table} u WHERE type='alumno'"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron alumnos")
            return rows
        except Exception as err:
            print("[-] get_all_students: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            
    def get_student_by_id(self, id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT id, u.name, u.p_surname, u.m_surname, u.email FROM {table} u WHERE type='alumno' AND id={id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontro el alumno")
            return rows
        except Exception as err:
            print("[-] get_student_by_id: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            
    def get_user_by_id(self, id: int) -> user_class:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table} WHERE id={id}"
            self.cursor.execute(self.sql)
            row = self.cursor.fetchone()
            self.conn.commit()
            if row is None:
                raise Exception("No se encontro el usuario")
            return user_class(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6])
        except Exception as err:
            print("[-] get_user_by_id: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def authenticate(self, user: user_class) -> user_class:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {table} WHERE email='{user.get_email()}'"
            self.cursor.execute(self.sql)
            row = self.cursor.fetchone()
            self.conn.commit()
            if row is not None:
                if user.get_password() == row[4]:
                    return user_class(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6])
                else:
                    messagebox.showwarning(WARNING_TITLE, "La contraseña no coincide")
                    raise Exception("La contraseña no coincide")
            else:
                messagebox.showwarning(WARNING_TITLE, "No se encontro el correo")
                raise Exception("No se encontro el correo")
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            messagebox.showerror(ERROR_TITLE, f"Error en la BD")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] {err}")
            raise Exception(f"Error al autenticar: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        
    def close(self):
        self.conn.close()