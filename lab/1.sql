-- Active: 1769830323903@@127.0.0.1@3306@db_uni047
-- Active: 1769823356550@@127.0.0.1@3306
CREATE DATABASE Db_uni047
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;


SHOW DATABASES;


USE Db_Uni047;
SELECT DATABASE();

-- Students table
CREATE TABLE Students047 (
    Sno047 VARCHAR(6),
    Sname047 VARCHAR(20) NOT NULL,
    Semail047 VARCHAR(50),
    Scredit047 DECIMAL(5,1),
    Sroom047 VARCHAR(5),
    CONSTRAINT PK_Stu047 PRIMARY KEY (Sno047),
    CONSTRAINT CK_Stu_Scredit047 CHECK (Scredit047 >= 0)
) ENGINE=InnoDB;


-- Teachers table
CREATE TABLE Teachers047 (
    Tno047 VARCHAR(6),
    Tname047 VARCHAR(20) NOT NULL,
    Temail047 VARCHAR(50),
    Tsalary047 DECIMAL(5,1),
    CONSTRAINT PK_Tea047 PRIMARY KEY (Tno047)
) ENGINE=InnoDB;


-- Courses table
CREATE TABLE Courses047 (
    Cno047 VARCHAR(6),
    Cname047 VARCHAR(20) NOT NULL,
    Ccredit047 DECIMAL(5,1),
    CONSTRAINT PK_Cou047 PRIMARY KEY (Cno047)
) ENGINE=InnoDB;


-- Reports table (create LAST)
CREATE TABLE Reports047 (
    Sno047 VARCHAR(6),
    Tno047 VARCHAR(6),
    Cno047 VARCHAR(6),
    Score047 DECIMAL(5,1),

    CONSTRAINT PK_Rep047 PRIMARY KEY (Sno047, Tno047, Cno047),

    CONSTRAINT FK_Stu_Rep047 FOREIGN KEY (Sno047)
        REFERENCES Students047(Sno047),

    CONSTRAINT FK_Tea_Rep047 FOREIGN KEY (Tno047)
        REFERENCES Teachers047(Tno047),

    CONSTRAINT FK_Cou_Rep047 FOREIGN KEY (Cno047)
        REFERENCES Courses047(Cno047)
) ENGINE=InnoDB;


SHOW TABLES;

-- 1. Add new column Ssex
ALTER TABLE Students047
ADD COLUMN Ssex047 VARCHAR(3);

-- 2. Remove CHECK constraint on Scredit (may not work depending on MySQL version)
ALTER TABLE Students047
DROP CHECK CK_Stu_Scredit047;

-- 3. Modify column lengths to 30
ALTER TABLE Students047
MODIFY Sname047 VARCHAR(30);

ALTER TABLE Teachers047
MODIFY Tname047 VARCHAR(30);

ALTER TABLE Courses047
MODIFY Cname047 VARCHAR(30);

DESCRIBE Students047;
DESCRIBE Teachers047;
DESCRIBE Courses047;
ALTER TABLE Students047
DROP COLUMN Sroom047;

DESCRIBE Students047;

DROP TABLE IF EXISTS Reports047;

CREATE TABLE Reports047 (
    Sno047 VARCHAR(6),
    Tno047 VARCHAR(6),
    Cno047 VARCHAR(6),
    Score047 DECIMAL(5,1),

    CONSTRAINT PK_Rep047 PRIMARY KEY (Sno047, Tno047, Cno047),

    CONSTRAINT FK_Stu_Rep047 FOREIGN KEY (Sno047)
        REFERENCES Students047(Sno047),

    CONSTRAINT FK_Tea_Rep047 FOREIGN KEY (Tno047)
        REFERENCES Teachers047(Tno047),

    CONSTRAINT FK_Cou_Rep047 FOREIGN KEY (Cno047)
        REFERENCES Courses047(Cno047)
) ENGINE=InnoDB;

SHOW CREATE TABLE Reports047;

CREATE INDEX idx_Cno047_desc
ON Courses047 (Cno047 DESC);

SHOW INDEX FROM Courses047;
USE Db_Uni047;

SHOW INDEX FROM Courses047;

CREATE INDEX idx_Sno047_asc
ON Students047 (Sno047 ASC);

SHOW INDEX FROM Students047;


CREATE UNIQUE INDEX idx_Sname047_unique
ON Students047 (Sname047 ASC);

SHOW INDEX FROM Students047;

-- Drop index on Students (Sno047)
DROP INDEX idx_Sno047_asc ON Students047;

-- Drop index on Courses (Cno047)
DROP INDEX idx_Cno047_desc ON Courses047;

SHOW INDEX FROM Students047;
SHOW INDEX FROM Courses047;


ALTER TABLE students047
Modify Ssex047 VARCHAR(10);
INSERT INTO students047
VALUES ('S01','Wang Jianping','WJP@zjut.edu.cn', 23.1,'Male'),
       ('S02','Liu Hua','LH@zjut.edu.cn', 24.6,'Female'),
       ('S03','Fan Linjun','FLJ@zjut.edu.cn', 16.6,'Female'),
       ('S04','Li Wei','LW@zjut.edu.cn', 15.8,'Male'),
       ('S26','Huang He','HUanghe@zjut.edu.cn', 13.4,'Male'),
       ('S52','Chang Jiang','Changjiang@zjut.edu.cn', 12.4,'Male');

INSERT INTO teachers047
VALUES ('T01','Liu Tao','LT@zjut.edu.cn', 4300),
       ('T02','Wu Biyan','WBY@zjut.edu.cn', 2500),
       ('T03','Zhang Ying','ZY@zjut.edu.cn', 3000),
       ('T04','Zhang Ningya','ZNY@zjut.edu.cn', 5500),
       ('T05','Ye Shuai','YS@zjut.edu.cn', 3800),
       ('T06','Yang Guangmei','YGM@zjut.edu.cn', 3500),
       ('T07','Cheng Qian','CQ@zjut.edu.cn', 5000);


ALTER table courses047
MODIFY Cname047 VARCHAR(50);

INSERT INTO courses047
VALUES ('C01','C++',4),
       ('C02','UML',4),
       ('C03','JAVA',3),
       ('C04','Algorithm Analysis and Design',3),
       ('C05','Database Principles and Applications',3),
       ('C06','Data Structures and Algorithms',4),
       ('C07','Computer Organization Principles',4),
       ('C08','English',6),
       ('C09','Digital Life',2),
       ('C10','Music Appreciation',2),
       ('C11','Physical Education 1',2);
      

INSERT INTO Reports047
VALUES ('S01','T01','C01',83),
       ('S01','T03','C03',85),
       ('S02','T01','C01',75),
       ('S02','T02','C02',45),
       ('S02','T03','C03',NULL),
       ('S02','T04','C04',NULL),
       ('S02','T05','C05',70),
       ('S02','T04','C06',83),
       ('S02','T05','C07',90),
       ('S02','T01','C08',83),
       ('S02','T02','C09',77),
       ('S02','T07','C10',83),
       ('S02','T06','C11',88),
       ('S03','T01','C08',63),
       ('S03','T02','C02',93),
       ('S03','T01','C01',78),
       ('S04','T06','C06',89),
       ('S04','T05','C05',93),
       ('S26','T07','C10',45),
       ('S26','T04','C04',86),
       ('S52','T07','C10',91),
       ('S52','T06','C11',90),
       ('S52','T05','C05',NULL),
       ('S52','T01','C08',64),
       ('S52','T02','C09',81);


SELECT Sname047
from students047
where Ssex047 = "Male"
ORDER BY Sno047 ASC; 

SELECT r.Sno047, c.Cno047,
CASE 
    WHEN `Score047` >= 60  THEN  (1 + (`Score047` - 60) * 0.1) * C.Ccredit047
    ELSE  0
END as Credit
From reports047 r
JOIN courses047 c ON r.`Cno047` = c.`Cno047`;

SELECT Cname047
FROM courses047
where `Ccredit047` IN (3,4);


SELECT `Cno047`
from courses047
where `Cname047` like "%Algorithm%";
SELECT DISTINCT cno047
from reports047; 

SELECT AVG(Tsalary047) as AvgSalary
from teachers047;

SELECT Tno, Avg(Score) as AvgScore
FROM reports047
GROUP BY `Tno047`
ORDER BY 

SELECT Cno047,
       COUNT(DISTINCT Sno047) AS StudentCount,
       AVG(Score047) AS AvgScore
FROM reports047
GROUP BY Cno047;

SELECT s.Sno047, s.Sname047
from students047 s
join reports047 r ON s.`Sno047` = r.`Sno047`
GROUP BY s.`Sno047`, s.Sname047 
having count(DISTINCT r.`Cno047`) >=3;

SELECT c.Cname047, r.Score047
from reports047 r
JOIN courses047 c On r.Cno047 = c.Cno047
where r.Sno047 = "S26";

SELECT DISTINCT s.Sno047, s.Sname047
FROM students047 s
JOIN reports047 r ON s.Sno047 = r.Sno047
JOIN courses047 c ON r.Cno047 = c.Cno047
WHERE c.Cname047 = 'Database Principles and Applications';


SELECT A.Sno047, B.Sno047, A.Cno047
FROM reports047 A
JOIN reports047 B 
ON A.Cno047 = B.Cno047 AND A.Sno047 < B.Sno047;

SELECT DISTINCT Sno047
FROM reports047
WHERE Cno047 IN (
    SELECT Cno047
    FROM reports047
    WHERE Sno047 = 'S26'
);

SELECT s.*, r.Cno047, r.Score047
FROM students047 s
LEFT JOIN reports047 r ON s.Sno047 = r.Sno047;

SELECT s.Sname047, c.Cname047, r.Score047
FROM students047 s
JOIN reports047 r ON s.Sno047 = r.Sno047
JOIN courses047 c ON r.Cno047 = c.Cno047
WHERE s.Sno047 = 'S52';

SELECT *
FROM students047
WHERE `Ssex047` = (
    SELECT `Ssex047`
    FROM students047
    WHERE Sno047 = 'S52'
);

SELECT DISTINCT s.*
FROM students047 s
JOIN reports047 r ON s.Sno047 = r.Sno047;

SELECT c.Cno047, c.Cname047
FROM courses047 c
LEFT JOIN reports047 r ON c.Cno047 = r.Cno047
WHERE r.Cno047 IS NULL;

SELECT s.Sno047, s.Sname047
FROM students047 s
JOIN reports047 r ON s.Sno047 = r.Sno047
WHERE r.Cno047 = 'C01';

SELECT DISTINCT s.Sno047, s.Sname047
FROM students047 s
JOIN reports047 r ON s.Sno047 = r.Sno047
WHERE r.Cno047 IN ('C01','C02');

SELECT Cname047
FROM courses047
WHERE Ccredit047 IN (
    SELECT Ccredit047
    FROM courses047
    WHERE Cname047 IN ('UML','C++')
);

SELECT s.Sname047
FROM students047 s
JOIN reports047 r ON s.Sno047 = r.Sno047
WHERE r.Cno047 = 'C01';


SELECT s.Sname047
FROM students047 s
WHERE NOT EXISTS (
    SELECT *
    FROM courses047 c
    WHERE NOT EXISTS (
        SELECT *
        FROM reports047 r
        WHERE r.Sno047 = s.Sno047 
          AND r.Cno047 = c.Cno047
    )
);

SELECT s.Sno047, s.Sname047
FROM students047 s
JOIN reports047 r ON s.Sno047 = r.Sno047
WHERE r.Cno047 = 'C01'

UNION

SELECT s.Sno047, s.Sname047
FROM students047 s
JOIN reports047 r ON s.Sno047 = r.Sno047
WHERE r.Cno047 = 'C03';

SELECT DISTINCT Sno047
FROM reports047
WHERE Cno047 = 'C01'
AND Sno047 NOT IN (
    SELECT Sno047
    FROM reports047
    WHERE Cno047 = 'C03'
);

SELECT s.Sno047, s.Sname047
FROM students047 s
WHERE s.Sno047 IN (
    SELECT Sno047 FROM reports047 WHERE Cno047 = 'C01'
)
AND s.Sno047 IN (
    SELECT Sno047 FROM reports047 WHERE Cno047 = 'C03'
);


INSERT into students047 (Sno047, Sname047, Semail047, Scredit047, Ssex047)
VALUES ('S78', 'Li Di', 'LD@zjut.edu.cn', 0, 'Male');

CREATE TABLE CourseStats047 (
    Cno047 VARCHAR(6),
    StudentCount INT,
    AvgScore DECIMAL(5,2)
);

INSERT INTO CourseStats047 (Cno047, StudentCount, AvgScore)
SELECT Cno047,
       COUNT(Score047),   -- counts only non-null scores
       AVG(Score047)
FROM reports047
GROUP BY Cno047;

UPDATE students047
SET Sno047 = 'S70'
WHERE Sname047 = 'Li Di';


UPDATE teachers047
SET `Tsalary047` = `Tsalary047` + 500;

UPDATE reports047 
SET `Score047` = `Score047` + 6
where `Sno047` = (
    SELECT `Sno047` FROM students047 where `Sname047` = "Liu Hua"
)
And `Cno047` = (
    SELECT `Cno047` FROM courses047
    where Cname047 = 'Principles and Applications of Database'
);

DELETE from students047
where Sname047 = "Li Di";

DELETE from reports047
Where Cno047 = (
    SELECT `Cno047` from courses047 where `Cname047` = "JAVA"
);

DELETE FROM reports047
WHERE Cno047 IN (
    SELECT Cno047 FROM courses047 WHERE Ccredit047 <= 4
);


SHOW TABLES;


CREATE VIEW CS_View_047 AS
SELECT R.SID047, C.TID047, R.CID047, R.Grade047
FROM reports047 R
JOIN courses047 C ON R.CID047 = C.CID047
WHERE R.Grade047 >= 60;

CREATE VIEW CS_View_047 AS
SELECT R.Sno047, R.Tno047, R.Cno047, R.Score047
FROM Reports047 R
WHERE R.Score047 >= 60;
SELECT * FROM CS_View_047;

CREATE VIEW SCT_View_047 AS
SELECT S.Sname047, C.Cname047, T.Tname047
FROM Students047 S
JOIN Reports047 R ON S.Sno047 = R.Sno047
JOIN Courses047 C ON R.Cno047 = C.Cno047
JOIN Teachers047 T ON R.Tno047 = T.Tno047;
SELECT * FROM SCT_View_047;


CREATE VIEW EXP_View_047 AS
SELECT S.Sname047,
       C.Cname047,
       R.Score047 + 5 AS NewScore047
FROM Students047 S
JOIN Reports047 R ON S.Sno047 = R.Sno047
JOIN Courses047 C ON R.Cno047 = C.Cno047;
SELECT * FROM EXP_View_047;

CREATE VIEW Group_View_047 AS
SELECT Sno047, AVG(Score047) AS AvgScore047
FROM Reports047
GROUP BY Sno047;


CREATE VIEW VV_View_047 AS
SELECT Sno047,
       COUNT(Cno047) AS CourseCount047,
       AVG(Score047) AS AvgScore047
FROM CS_View_047
GROUP BY Sno047;


DROP VIEW SCT_View_047;
DROP VIEW EXP_View_047;
DROP VIEW Group_View_047;


DROP VIEW CS_View_047;

CREATE VIEW CS_View_opt_047 AS
SELECT Sno047, Tno047, Cno047, Score047
FROM Reports047
WHERE Score047 >= 60
WITH CHECK OPTION;


CREATE TABLE Stu_Union1_047 (
    Sno047 CHAR(8) NOT NULL UNIQUE,
    Sname047 CHAR(8),
    Ssex047 CHAR(3),
    Sage047 INT,
    Sdept047 CHAR(20)
);

DROP TABLE Stu_Union1_047;

CREATE TABLE Stu_Union2_047 (
    Sno047 CHAR(8),
    Sname047 CHAR(8),
    Ssex047 CHAR(3),
    Sage047 INT,
    Sdept047 CHAR(20),
    CONSTRAINT PK_Stu_Union2_047 PRIMARY KEY (Sno047)
);

CREATE TABLE Stu_Union3_047 (
    Sno047 CHAR(8),
    Sname047 CHAR(8) UNIQUE,
    Ssex047 CHAR(3),
    Sage047 INT,
    Sdept047 CHAR(20),
    CONSTRAINT PK_Stu_Union3_047 PRIMARY KEY (Sno047)
);


CREATE TABLE Stu_Union4_047 (
    Sno047 CHAR(8) NOT NULL UNIQUE,
    Sname047 CHAR(8),
    Ssex047 CHAR(3),
    Sage047 INT,
    Sdept047 CHAR(20)
);

ALTER TABLE Stu_Union4_047
ADD CONSTRAINT PK_Stu_Union4_047 PRIMARY KEY (Sno047);

CREATE TABLE Report1_047 (
    Sno047 VARCHAR(6),
    Tno047 VARCHAR(6),
    Cno047 VARCHAR(6),
    Score047 DECIMAL(5,1),
    CONSTRAINT PK_Report1_047 PRIMARY KEY (Sno047, Tno047, Cno047)
);


INSERT INTO Stu_Union2_047
VALUES ('S01','Wang','M',20,'CS');

INSERT INTO Stu_Union2_047
VALUES (NULL,'Test','M',20,'CS');


UPDATE Stu_Union2_047
SET Sno047 = NULL
WHERE Sno047 = 'S01';

INSERT INTO Stu_Union2_047 VALUES ('S02','Ali','M',21,'CS');

UPDATE Stu_Union2_047
SET Sno047 = 'S01'
WHERE Sno047 = 'S02';

START TRANSACTION;

INSERT INTO Stu_Union2_047 VALUES ('S10','A','M',20,'CS');
INSERT INTO Stu_Union2_047 VALUES ('S11','B','F',21,'EE');

COMMIT;

START TRANSACTION;

INSERT INTO Stu_Union2_047 VALUES ('S20','C','M',22,'CS');
INSERT INTO Stu_Union2_047 VALUES ('S01','Dup','M',23,'EE'); -- error

ROLLBACK;


SELECT * FROM Stu_Union2_047 WHERE Sno047='S20';

CREATE TABLE Scholarship047 (
    M_ID047 VARCHAR(10),
    Stu_id047 VARCHAR(6),
    R_Money047 INT
);

INSERT INTO Scholarship047 VALUES ('M01','S01',5000);
INSERT INTO Scholarship047 VALUES ('M01','SXX',8000); -- invalid student

SELECT * FROM Scholarship047;

ALTER TABLE Scholarship047
ADD CONSTRAINT PK_Sch047 PRIMARY KEY (M_ID047);

ALTER TABLE Scholarship047
ADD CONSTRAINT FK_Sch047
FOREIGN KEY (Stu_id047)
REFERENCES Students047(Sno047);

DROP TABLE Scholarship047;