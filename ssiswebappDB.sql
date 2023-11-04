CREATE DATABASE ssiswebapp;
USE ssiswebapp;

CREATE TABLE college (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE course (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    college_code VARCHAR(10),
    FOREIGN KEY (college_code) REFERENCES college(code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE student (
    id CHAR(9) PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    course_code VARCHAR(10),
    year INT,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    FOREIGN KEY (course_code) REFERENCES course(code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DELIMITER //
CREATE TRIGGER before_student_insert
BEFORE INSERT ON student
FOR EACH ROW
BEGIN
    DECLARE current_year INT;
    DECLARE next_student_id INT;

    SET current_year = YEAR(NOW());

    SELECT IFNULL(MAX(CONVERT(SUBSTRING(id, 6), SIGNED)), 0) + 1 INTO next_student_id
    FROM student
    WHERE SUBSTRING(id, 1, 4) = current_year;

    SET NEW.id = CONCAT(current_year, '-', LPAD(next_student_id, 4, '0'));
END;
//
DELIMITER ;
