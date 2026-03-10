-- Active: 1769823356550@@127.0.0.1@3306@school_db
CREATE DATABASE school_db;

USE school_db;

CREATE Table students(
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    major TEXT,
    gpa REAL
);

CREATE TABLE courses(
    course_id INTEGER PRIMARY KEY,
    course_name TEXT,
    credits INTEGER
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    grade TEXT,
    FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);

INSERT INTO students VALUES
(1,'Alice',20,'Computer Science',3.8),
(2,'Bob',22,'Mathematics',3.4),
(3,'Charlie',19,'Physics',3.9),
(4,'David',21,'Computer Science',3.2),
(5,'Emma',20,'Mathematics',3.7);

INSERT INTO courses VALUES
(1,'Database Systems',4),
(2,'Linear Algebra',3),
(3,'Machine Learning',4),
(4,'Physics I',3);

INSERT INTO enrollments VALUES
(1,1,1,'A'),
(2,1,3,'A'),
(3,2,2,'B'),
(4,3,4,'A'),
(5,4,1,'C'),
(6,5,2,'A');



