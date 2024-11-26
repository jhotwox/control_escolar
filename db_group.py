import mysql.connector as mysql
from group import group as group_class
from db_functions import max_id
from functions import ERROR_TITLE, WARNING_TITLE
from tkinter import messagebox
import database as db

table = "groups"

class db_group:
    

    def assign_teacher_and_classroom(self, group: group_class) -> None:
        try:
            max_priority = 3
            teacher_assigned = False
            for priority in range(1, max_priority + 1):
                self.sql = "SELECT user_id FROM user_subject WHERE subject_id = %s AND priority = %s"
                self.cursor.execute(self.sql, (group.get_subject_id(), priority))
                teacher_id = self.cursor.fetchone()
                if teacher_id:
                    self.sql = "SELECT * FROM groups WHERE teacher_id = %s AND schedule_id = %s"
                    self.cursor.execute(self.sql, (teacher_id[0], group.get_schedule_id()))
                    existing_teacher_schedule = self.cursor.fetchone()
                    if not existing_teacher_schedule:
                        group.teacher_id = teacher_id[0]
                        teacher_assigned = True
                        break
            if not teacher_assigned:
                raise Exception("No se encontró un maestro disponible para esta materia.")

            self.sql = "SELECT id FROM classrooms WHERE id NOT IN (SELECT classroom_id FROM groups WHERE schedule_id = %s)"
            self.cursor.execute(self.sql, (group.get_schedule_id(),))
            classroom_id = self.cursor.fetchone()
            if classroom_id:
                group.classroom_id = classroom_id[0]
            else:
                raise Exception("No hay aulas disponibles para este horario.")
        except Exception as err:
            print(f"[-] assign_teacher_and_classroom: {err}")
            raise Exception(f"Error al asignar maestro o aula: {err}")
        
    

    def save(self, group: group_class) -> None:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            
            self.sql = f"INSERT INTO {table}(id, schedule_id, teacher_id, classroom_id, subject_id, name, max_quota, quota, semester) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.data = (
                group.get_id(),
                group.get_schedule_id(),
                group.get_teacher_id(),
                group.get_classroom_id(),
                group.get_subject_id(),
                group.get_name(),
                group.get_max_quota(),
                group.get_quota(),
                group.get_semester()
            )
            self.cursor.execute(self.sql, self.data)
            self.conn.commit()

        except mysql.Error as err:
            print(f"[-] Mysql: {err}")
            raise Exception(f"Error en la BD: {err}")
        except Exception as err:
            print(f"[-] save in db_groups: {err}")
            raise Exception(f"Error al guardar group: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    # Save Erick 
    # def save(self, grupo: group_class) -> None:
    #     try:
    #         self.conn = db.conection().open()
    #         self.cursor = self.conn.cursor()
            
    #         # Validar que no existe a partir del horario y maestro
    #         self.sql = f"SELECT * FROM {table} WHERE schedule_id = %s AND teacher_id = %s"
    #         self.cursor.execute(self.sql, (grupo.get_schedule_id(), grupo.get_teacher_id()))
    #         existing_group = self.cursor.fetchone()
    #         if existing_group:
    #             raise Exception("El grupo con este horario y maestro ya existe.")
            
    #         # Validar que el salon no esta ocupado
    #         self.sql = f"SELECT * FROM {table} WHERE schedule_id = %s AND classroom_id = %s"
    #         self.cursor.execute(self.sql, (grupo.get_schedule_id(), grupo.get_classroom_id()))
    #         existing_classroom = self.cursor.fetchone()
    #         if existing_classroom:
    #             raise Exception("El salón está ocupado en este horario.")
            
    #         # Buscar maestro disponible
    #         self.sql = "SELECT user_id FROM user_subject WHERE subject_id = %s AND priority = 1"
    #         self.cursor.execute(self.sql, (grupo.get_subject_id(),))
    #         teacher_id = self.cursor.fetchone()
    #         if teacher_id:
    #             grupo.teacher_id = teacher_id[0]
    #         else:
    #             self.sql = "SELECT user_id FROM user_subject WHERE subject_id = %s AND priority = 2"
    #             self.cursor.execute(self.sql, (grupo.get_subject_id(),))
    #             teacher_id = self.cursor.fetchone()
    #             if teacher_id:
    #                 grupo.teacher_id = teacher_id[0]
    #             else:
    #                 raise Exception("No se encontró un maestro disponible para esta materia.")

    #         # Validar que el horario no este ocupado
    #         self.sql = "SELECT * FROM groups WHERE subject_id = %s AND schedule_id BETWEEN %s AND %s"
    #         schedule_range = self.get_schedule_range(grupo.get_subject_id())
    #         data = (grupo.get_subject_id(), schedule_range[0], schedule_range[1])
    #         self.cursor.execute(self.sql, data)
    #         existing_schedule = self.cursor.fetchall()
    #         if existing_schedule:
    #             raise Exception(f"El horario de esta materia ya está ocupado en el rango de {schedule_range[0]} a {schedule_range[1]}.")

            
    #         self.sql = f"INSERT INTO {table}(schedule_id, teacher_id, classroom_id, subject_id, name, max_quota, quota, semester) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    #         self.data = (
    #             grupo.get_schedule_id(),
    #             grupo.get_teacher_id(),
    #             grupo.get_classroom_id(),
    #             grupo.get_subject_id(),
    #             grupo.get_name(),
    #             grupo.get_max_quota(),
    #             grupo.get_quota(),
    #             grupo.get_semester()
    #         )
    #         self.cursor.execute(self.sql, self.data)
    #         self.conn.commit()

    #     except mysql.Error as err:
    #         print(f"[-] Mysql: {err}")
    #         raise Exception(f"Error en la BD: {err}")
    #     except Exception as err:
    #         print(f"[-] save in db_grupos: {err}")
    #         raise Exception(f"Error al guardar grupo: {err}")
    #     finally:
    #         if self.cursor:
    #             self.cursor.close()
    #         if self.conn:
    #             self.conn.close()

    def teacher_and_schedule_available(self, priority_dict: dict) -> list:
        try:    
            self.conn = db.conection().open()
            self.cursor0 = self.conn.cursor()
            self.cursor = self.conn.cursor()
            
            # Comprobar que el maestro no tenga un grupo en el mismo horario
            # Recorrer maestros por prioridad
            for teacher_id, priority in priority_dict.items():
                
                # Obtener lista de id de horarios
                self.sql0 = f"SELECT id FROM schedule"
                self.cursor0.execute(self.sql0)
                schedules = self.cursor0.fetchall()
                schedules = [schedule[0] for schedule in schedules]
                
                # Recorrer horarios
                for schedule_id in schedules:
                    # Comprobar si el maestro tiene un grupo en el horario
                    self.sql = f"SELECT COUNT(*) FROM {table} WHERE schedule_id = %s AND teacher_id = %s"
                    self.cursor.execute(self.sql, (schedule_id, teacher_id))
                    existing_group = self.cursor.fetchone()[0]
                    # Si no hay grupos con el maestro en el mismo horario
                    print(f"existing_group with schedule: {schedule_id} and teacher: {teacher_id} -> ", existing_group)
                    if existing_group == 0:
                        return (teacher_id, schedule_id)
                    # Si el maestro con la prioridad más baja esta ocupado en todos los horarios posibles, lanzar excepción
                    # print("Priority_dict.values() -> ", priority_dict.values())
                    if priority == list(priority_dict.values())[-1] and schedule_id == schedules[-1]:
                        raise Exception("Los maestros asignados a esta materia estan ocupados.")
        except Exception as err:
            print(f"[-] teacher_and_schedule_available in db_group: {err}")
            raise Exception(f"Error al buscar maestro disponible: {err}")
        finally:
            if self.cursor0:
                self.cursor0.close()
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
    
    def get_all_groups(self) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = """
                SELECT id, schedule_id, teacher_id, classroom_id, subject_id, name, max_quota, quota, semester
                FROM groups;
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontraron maestros")
            return rows
        except Exception as err:
            print("[-] get_all_teachers: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def get_group_by_id(self, id: int) -> list:
        try:
            self.conn = db.conection().open()
            self.cursor = self.conn.cursor()
            self.sql = f"""
                SELECT id, schedule_id, teacher_id, classroom_id, subject_id, name, max_quota, quota, semester
                FROM groups
                WHERE id={id}
            """
            self.cursor.execute(self.sql)
            rows = self.cursor.fetchall()
            self.conn.commit()
            if rows is None:
                raise Exception("No se encontro el maestro")
            return rows
        except Exception as err:
            print("[-] get_teacher_by_id: ", err)
            messagebox.showerror(ERROR_TITLE, "Error en la consulta")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
