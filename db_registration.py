from tkinter import messagebox
import mysql.connector as mysql
import database as db
from functions import ERROR_TITLE
from db_functions import max_id

TABLE = "registration"

class db_registration:
    def save(self, user_id: int, group_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"INSERT INTO {TABLE}(user_id, group_id) values (%s,%s)"
            self.data = (
                user_id,
                group_id
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()
        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_registration: {err}")
            raise Exception(f"Error al guardar registro: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def remove(self, user_id: int, group_id: int) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {TABLE} WHERE group_id={group_id} AND user_id={user_id}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print(f"[-] remove in db_registration: {err}")
            raise Exception(f"Error al eliminar registro: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    # def remove_all_by_user(self, user_id: int) -> None:
    #     try:
    #         self.conn = db.conection().open()
    #         self.cursor = self.conn.cursor()
    #         self.sql = f"DELETE FROM {TABLE} WHERE user_id={user_id}"
    #         self.cursor.execute(self.sql)
    #         self.conn.commit()
    #     except Exception as err:
    #         print(f"[-] remove_all_by_user in db_registration: {err}")
    #         raise Exception(f"Error al eliminar registros del estudiante: {err}")
    #     finally:
    #         if self.cursor:
    #             self.cursor.close()
    #         if self.conn:
    #             self.conn.close()
    
    def get_all_registration(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT * FROM {TABLE}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron registros")
            return rows
        except Exception as err:
            print("[-] get_all_registration: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def get_all_registration_dict(self) -> dict:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT group_id, user_id FROM {TABLE} ORDER BY group_id ASC"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            return {row[0]: row[1] for row in rows} if rows else {}
        except Exception as err:
            print("[-] get_all_registration_dict: ", err)
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
            
            # Obtener lista de id's de grupos de la tabla registration
            self.sql = f"SELECT DISTINCT group_id FROM {TABLE} ORDER BY group_id ASC"
            self.cursor.execute(self.sql)
            groups_list = self.cursor.fetchall()
            groups_list: list = [group[0] for group in groups_list]
            self.conn.commit()
            
            result = {}
            for group in groups_list:
                self.sql = f"SELECT user_id FROM {TABLE} WHERE group_id={group}"
                self.cursor.execute(self.sql)
                users = self.cursor.fetchall()
                self.conn.commit()
                users = [user[0] for user in users]
                result[group] = users
            
            return result if result else {}

        except Exception as err:
            print("[-] get_dict_of_list_by_subject: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_groups_id_by_user(self, user_id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT group_id FROM {TABLE} WHERE user_id={user_id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron grupos con el estudiante seleccionado")
            return [row[0] for row in rows]
        except Exception as err:
            print("[-] get_groups_id_by_user: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_quantity_by_group(self, group_id: int) -> int:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"SELECT COUNT(*) FROM {TABLE} WHERE group_id={group_id}"
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchone()
            self.conn.commit()
            return rows[0] if rows else 0
        except Exception as err:
            print("[-] get_quantity_by_group: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def schedule_crossed(self, user_id: int, schedule_id: int) -> bool:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT r.group_id
                FROM registration r, groups g
                WHERE r.group_id = g.id
                AND r.user_id = {user_id}
                AND g.schedule_id = {schedule_id}
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            return True if rows else False
        except Exception as err:
            print("[-] schedule_crossed: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
    
    def delete_all(self) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"DELETE FROM {TABLE}"
            self.cursor.execute(self.sql)
            self.conn.commit()
        except Exception as err:
            print("[-] delete_all: ", err)
            messagebox.showerror(ERROR_TITLE, "Error al eliminar todos los registros")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
    
    def get_max_id(self) -> int:
        return max_id(TABLE)
    
    def close(self):
        self.conn.close()