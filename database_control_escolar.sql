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