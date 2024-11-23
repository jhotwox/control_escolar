-- #region TABLAS
CREATE TABLE user (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(30),
    p_surname VARCHAR(30),
    m_surname VARCHAR(30),
    password VARCHAR(30),
    email VARCHAR(30),
    type enum ('administrador', 'maestro', 'alumno')
);

CREATE TABLE student (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    FOREIGN KEY (id) REFERENCES user(id)
);

CREATE TABLE teacher (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    cedula VARCHAR(30),
    FOREIGN KEY (id) REFERENCES user(id)
);

CREATE TABLE career (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(30)
);

CREATE TABLE subject (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(30)
);

CREATE TABLE schedule (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    day INT,
    start_time VARCHAR(6),
    end_time VARCHAR(6)
);

CREATE TABLE building (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(20)
);

CREATE TABLE classroom (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(20),
    building_id INT,
    FOREIGN KEY (building_id) REFERENCES building(id)
);

CREATE TABLE subject_career (
    subject_id INT NOT NULL,
    career_id INT NOT NULL,
    PRIMARY KEY(subject_id, career_id),
    FOREIGN KEY (subject_id) REFERENCES subject(id),
    FOREIGN KEY (career_id) REFERENCES career(id)
);

CREATE TABLE user_career (
    user_id INT NOT NULL,
    career_id INT NOT NULL,
    PRIMARY KEY(user_id, career_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (career_id) REFERENCES career(id)
);

CREATE TABLE user_subject (
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    priority INT NOT NULL,
    PRIMARY KEY(user_id, subject_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (subject_id) REFERENCES subject(id)
);

CREATE TABLE groups (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    schedule_id INT,
    teacher_id INT,
    classroom_id INT,
    subject_id INT,
    name VARCHAR(30),
    max_quota INT,
    quota INT,
    semester INT,
    FOREIGN KEY (schedule_id) REFERENCES schedule(id),
    FOREIGN KEY (teacher_id) REFERENCES teacher(id),
    FOREIGN KEY (classroom_id) REFERENCES classroom(id),
    FOREIGN KEY (subject_id) REFERENCES subject(id)
);

CREATE TABLE pre_registration (
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    PRIMARY KEY(user_id, subject_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (subject_id) REFERENCES subject(id)
);

CREATE TABLE registration (
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    PRIMARY KEY(user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- #region TRIGGERS
-- Restar registro de la quota al unirse al grupo
CREATE TRIGGER registration_quota_update
AFTER INSERT ON registration
FOR EACH ROW
BEGIN
    UPDATE groups
    SET quota = quota - 1
    WHERE id = NEW.group_id;
END

-- añadir registro de la quota al salirse del grupo
CREATE TRIGGER registration_quota_restore
AFTER DELETE ON registration
FOR EACH ROW
BEGIN
    UPDATE groups
    SET quota = quota + 1
    WHERE id = OLD.group_id;
END

-- #region UPDATE DELETE CASCADE
-- Eliminar restricciones actuales antes de volver a crearlas con eliminación en cascada
ALTER TABLE student DROP FOREIGN KEY student_ibfk_1;
ALTER TABLE teacher DROP FOREIGN KEY teacher_ibfk_1;
ALTER TABLE classroom DROP FOREIGN KEY classroom_ibfk_1;
ALTER TABLE subject_career DROP FOREIGN KEY subject_career_ibfk_1, DROP FOREIGN KEY subject_career_ibfk_2;
ALTER TABLE user_career DROP FOREIGN KEY user_career_ibfk_1, DROP FOREIGN KEY user_career_ibfk_2;
ALTER TABLE user_subject DROP FOREIGN KEY user_subject_ibfk_1, DROP FOREIGN KEY user_subject_ibfk_2;
ALTER TABLE groups DROP FOREIGN KEY groups_ibfk_1, DROP FOREIGN KEY groups_ibfk_2, DROP FOREIGN KEY groups_ibfk_3, DROP FOREIGN KEY groups_ibfk_4;
ALTER TABLE pre_registration DROP FOREIGN KEY pre_registration_ibfk_1, DROP FOREIGN KEY pre_registration_ibfk_2;
ALTER TABLE registration DROP FOREIGN KEY registration_ibfk_1, DROP FOREIGN KEY registration_ibfk_2;

-- Crear nuevamente las claves foráneas con eliminación en cascada
ALTER TABLE student
ADD CONSTRAINT fk_student_user
FOREIGN KEY (id) REFERENCES user(id)
ON DELETE CASCADE;

ALTER TABLE teacher
ADD CONSTRAINT fk_teacher_user
FOREIGN KEY (id) REFERENCES user(id)
ON DELETE CASCADE;

ALTER TABLE classroom
ADD CONSTRAINT fk_classroom_building
FOREIGN KEY (building_id) REFERENCES building(id)
ON DELETE CASCADE;

ALTER TABLE subject_career
ADD CONSTRAINT fk_subject_career_subject
FOREIGN KEY (subject_id) REFERENCES subject(id)
ON DELETE CASCADE,
ADD CONSTRAINT fk_subject_career_career
FOREIGN KEY (career_id) REFERENCES career(id)
ON DELETE CASCADE;

ALTER TABLE user_career
ADD CONSTRAINT fk_user_career_user
FOREIGN KEY (user_id) REFERENCES user(id)
ON DELETE CASCADE,
ADD CONSTRAINT fk_user_career_career
FOREIGN KEY (career_id) REFERENCES career(id)
ON DELETE CASCADE;

ALTER TABLE user_subject
ADD CONSTRAINT fk_user_subject_user
FOREIGN KEY (user_id) REFERENCES user(id)
ON DELETE CASCADE,
ADD CONSTRAINT fk_user_subject_subject
FOREIGN KEY (subject_id) REFERENCES subject(id)
ON DELETE CASCADE;

ALTER TABLE groups
ADD CONSTRAINT fk_groups_schedule
FOREIGN KEY (schedule_id) REFERENCES schedule(id)
ON DELETE CASCADE,
ADD CONSTRAINT fk_groups_teacher
FOREIGN KEY (teacher_id) REFERENCES teacher(id)
ON DELETE CASCADE,
ADD CONSTRAINT fk_groups_classroom
FOREIGN KEY (classroom_id) REFERENCES classroom(id)
ON DELETE CASCADE,
ADD CONSTRAINT fk_groups_subject
FOREIGN KEY (subject_id) REFERENCES subject(id)
ON DELETE CASCADE;

ALTER TABLE pre_registration
ADD CONSTRAINT fk_pre_registration_user
FOREIGN KEY (user_id) REFERENCES user(id)
ON DELETE CASCADE,
ADD CONSTRAINT fk_pre_registration_subject
FOREIGN KEY (subject_id) REFERENCES subject(id)
ON DELETE CASCADE;

ALTER TABLE registration
ADD CONSTRAINT fk_registration_user
FOREIGN KEY (user_id) REFERENCES user(id)
ON DELETE CASCADE,
ADD CONSTRAINT fk_registration_group
FOREIGN KEY (group_id) REFERENCES groups(id)
ON DELETE CASCADE;

-- #region PRUEBAS
SELECT s.name materia, u.name maestro, us.priority
FROM user_subject us, user u, subject s
WHERE u.id=us.user_id
AND us.subject_id=s.id
AND us.subject_id=5;

SELECT s.name materia, u.name maestro, us.priority
FROM user_subject us, user u, subject s
WHERE u.id=us.user_id
AND us.subject_id=s.id
AND us.subject_id={subject_id};