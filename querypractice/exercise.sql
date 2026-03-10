--exercise 1
SELECT *
FROM students;

--exercose 2 Show only names and GPA

SELECT name, gpa
from students

--ex3 Show students whose GPA is greater than 3.5.
SELECT name, gpa
FROM students
where gpa>3.5 

--ex4 Show all students whose major is "Computer Science"
SELECT name 
from students
where major = 'Computer Science'

--ex5 Return students whose age > 20.
SELECT name, age
from students
where age > 20;

--ex6 Show all students sorted by GPA from highest to lowest.
SELECT name, gpa 
from students
ORDER BY gpa DESC;

--ex7 Return the total number of students
Select COUNT(student_id)  as total
from students;

--ex8 Find the average GPA of all students.
SELECT AVG(gpa) as average 
from students;

--ex9 Show all courses where credits = 4
Select *
from courses;

--ex10 Courses with 4 credits
SELECT course_name, credits
from courses
where credits = 4;

--ex11 Show all rows in enrollments where: student_id = 1

SELECT s.name, e.grade
from students s
JOIN enrollments e
On s.student_id = e.student_id

--ex 12

SELECT s.name, c.course_name, e.grade
FROM students s
JOIN enrollments e
ON s.student_id = e.student_id
JOIN courses c
ON e.course_id = c.course_id;

--ex13

SELECT *
FROM enrollments;

Select s.student_id, s.name, c.course_name
from students s
join enrollments e
on s.student_id = e.student_id
join courses c
on e.course_id = c.course_id
WHERE course_name = 'Database Systems';

--14 

SELECT major, COUNT(*) as number_of_students
from students
GROUP BY major;

--15

SELECT name, gpa
from students
order BY gpa desc
limit 1;