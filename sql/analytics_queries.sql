-----------------------------------------------------
-- 1 Total Students
-----------------------------------------------------

SELECT COUNT(*) AS total_students
FROM warehouse.students;

-----------------------------------------------------
-- 2 Total Faculty
-----------------------------------------------------

SELECT COUNT(*) AS total_faculty
FROM warehouse.faculty;

-----------------------------------------------------
-- 3 Total Subjects
-----------------------------------------------------

SELECT COUNT(*) AS total_subjects
FROM warehouse.subjects;

-----------------------------------------------------
-- 4 Average Marks
-----------------------------------------------------

SELECT ROUND(AVG(marks),2)
FROM warehouse.results;

-----------------------------------------------------
-- 5 Top 10 Students
-----------------------------------------------------

SELECT
student_id,
AVG(marks) AS average_marks
FROM warehouse.results
GROUP BY student_id
ORDER BY average_marks DESC
LIMIT 10;

-----------------------------------------------------
-- 6 Lowest Performing Students
-----------------------------------------------------

SELECT
student_id,
AVG(marks) AS average_marks
FROM warehouse.results
GROUP BY student_id
ORDER BY average_marks
LIMIT 10;

-----------------------------------------------------
-- 7 Grade Distribution
-----------------------------------------------------

SELECT
grade,
COUNT(*)
FROM warehouse.results
GROUP BY grade
ORDER BY grade;

-----------------------------------------------------
-- 8 Attendance Percentage
-----------------------------------------------------

SELECT *
FROM warehouse.attendance_summary
ORDER BY attendance_percentage DESC
LIMIT 10;

-----------------------------------------------------
-- 9 Fee Collection Status
-----------------------------------------------------

SELECT *
FROM warehouse.fee_summary;

-----------------------------------------------------
--10 Top Recruiting Companies
-----------------------------------------------------

SELECT
company_name,
COUNT(*) AS students
FROM warehouse.placements
GROUP BY company_name
ORDER BY students DESC;

-----------------------------------------------------
--11 Subject Wise Average Marks
-----------------------------------------------------

SELECT
s.subject_name,
AVG(r.marks)
FROM warehouse.subjects s
JOIN warehouse.results r
ON s.subject_id=r.subject_id
GROUP BY s.subject_name
ORDER BY AVG(r.marks) DESC;

-----------------------------------------------------
--12 Students with Attendance <75%
-----------------------------------------------------

SELECT *
FROM warehouse.attendance_summary
WHERE attendance_percentage<75;