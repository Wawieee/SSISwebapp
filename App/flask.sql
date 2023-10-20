DROP DATABASE IF EXISTS ssiswebapp;
CREATE DATABASE IF NOT EXISTS ssiswebapp;

USE ssiswebapp;

DROP TABLE IF EXISTS college;
CREATE TABLE IF NOT EXISTS college (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS course;
CREATE TABLE IF NOT EXISTS course (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    college_code VARCHAR(10),
    FOREIGN KEY (college_code) REFERENCES college(code)
);

DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student (
    id CHAR(9) PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    course_code VARCHAR(10),
    year INT,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    FOREIGN KEY (course_code) REFERENCES course(code)
);
