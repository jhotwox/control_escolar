import mysql.connector as mysql
from group import group as group_class
from db_functions import max_id
from functions import ERROR_TITLE, WARNING_TITLE
from tkinter import messagebox
import database as db

table = "groups"

class db_group:
    
    def save(self, grupo: group_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            
            # Validar que no existe a partir del horario y maestro
            self.sql = f"SELECT * FROM {table} WHERE schedule_id = %s AND teacher_id = %s"
            self.cursor.execute(self.sql, (grupo.get_schedule_id(), grupo.get_teacher_id()))
            existing_group = self.cursor.fetchone()
            if existing_group:
                raise Exception("El grupo con este horario y maestro ya existe.")
            
            # Validar que el salon no esta ocupado
            self.sql = f"SELECT * FROM {table} WHERE schedule_id = %s AND classroom_id = %s"
            self.cursor.execute(self.sql, (grupo.get_schedule_id(), grupo.get_classroom_id()))
            existing_classroom = self.cursor.fetchone()
            if existing_classroom:
                raise Exception("El salón está ocupado en este horario.")
            
            # Buscar maestro disponible
            self.sql = "SELECT user_id FROM user_subject WHERE subject_id = %s AND priority = 1"
            self.cursor.execute(self.sql, (grupo.get_subject_id(),))
            teacher_id = self.cursor.fetchone()
            if teacher_id:
                grupo.teacher_id = teacher_id[0]
            else:
                self.sql = "SELECT user_id FROM user_subject WHERE subject_id = %s AND priority = 2"
                self.cursor.execute(self.sql, (grupo.get_subject_id(),))
                teacher_id = self.cursor.fetchone()
                if teacher_id:
                    grupo.teacher_id = teacher_id[0]
                else:
                    raise Exception("No se encontró un maestro disponible para esta materia.")

            # Validar que el horario no este ocupado
            self.sql = "SELECT * FROM groups WHERE subject_id = %s AND schedule_id BETWEEN %s AND %s"
            schedule_range = self.get_schedule_range(grupo.get_subject_id())
            data = (grupo.get_subject_id(), schedule_range[0], schedule_range[1])
            self.cursor.execute(self.sql, data)
            existing_schedule = self.cursor.fetchall()
            if existing_schedule:
                raise Exception(f"El horario de esta materia ya está ocupado en el rango de {schedule_range[0]} a {schedule_range[1]}.")

            
            self.sql = f"INSERT INTO {table}(schedule_id, teacher_id, classroom_id, subject_id, name, max_quota, quota, semester) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            self.data = (
                grupo.get_schedule_id(),
                grupo.get_teacher_id(),
                grupo.get_classroom_id(),
                grupo.get_subject_id(),
                grupo.get_name(),
                grupo.get_max_quota(),
                grupo.get_quota(),
                grupo.get_semester()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()

        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_grupos: {err}")
            raise Exception(f"Error al guardar grupo: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def get_max_id(self) -> int:
        return max_id(table)
    
    def get_schedule_range(self, subject_id: int):
        return (1, 7)
    
    def close(self):
        self.conn.close()
