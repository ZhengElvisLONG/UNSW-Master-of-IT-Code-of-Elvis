-------------------------
-- Project 1 Solution
-- COMP9311 24T3
-- Name: Zheng LONG
-- zID: z5516222
-------------------------


-- Q1
CREATE OR REPLACE VIEW Q1(count) AS
SELECT COUNT(DISTINCT s.id) AS count
FROM students s
JOIN course_enrolments ce ON s.id = ce.student
JOIN courses c ON ce.course = c.id
JOIN subjects sub ON c.subject = sub.id
WHERE ce.mark > 85 AND sub.code LIKE 'COMP%';



-- Q2
CREATE OR REPLACE VIEW Q2(count) AS
SELECT COUNT(*) AS count
FROM (
    SELECT s.id
    FROM students s
    JOIN course_enrolments ce ON s.id = ce.student
    JOIN courses c ON ce.course = c.id
    JOIN subjects sub ON c.subject = sub.id
    WHERE sub.code LIKE 'COMP%' AND ce.mark IS NOT NULL
    GROUP BY s.id
    HAVING AVG(ce.mark) > 85
) AS high_avg_students;



-- Q3
DROP VIEW IF EXISTS Q3 CASCADE;
CREATE or REPLACE VIEW Q3(unswid,name) AS
SELECT p.unswid, p.name
FROM people p
JOIN students s ON p.id = s.id
JOIN course_enrolments ce ON s.id = ce.student
JOIN courses c ON ce.course = c.id
JOIN subjects subj ON c.subject = subj.id
WHERE subj.code LIKE 'COMP%' AND ce.mark IS NOT NULL
GROUP BY p.unswid, p.name
HAVING COUNT(DISTINCT c.id) >= 6 AND AVG(ce.mark) > 85;



-- Q4 missing tuples
CREATE OR REPLACE VIEW Q4(unswid, name) AS
WITH highest_marks AS (
    SELECT ce.student, subj.code AS subject_code, MAX(ce.mark) AS highest_mark, subj.uoc
    FROM course_enrolments ce
    JOIN courses c ON ce.course = c.id
    JOIN subjects subj ON c.subject = subj.id
    WHERE subj.code LIKE 'COMP%' AND ce.mark IS NOT NULL
    GROUP BY ce.student, subj.code, subj.uoc
)
SELECT p.unswid, p.name
FROM people p
JOIN students s ON p.id = s.id
JOIN highest_marks hm ON s.id = hm.student
GROUP BY p.unswid, p.name
HAVING COUNT(DISTINCT hm.subject_code) >= 6 
   AND SUM(hm.highest_mark * hm.uoc) / SUM(hm.uoc) > 85;



-- Q5
DROP VIEW IF EXISTS Q5 CASCADE;
CREATE OR REPLACE VIEW Q5(count) AS
SELECT COUNT(DISTINCT c.subject)
FROM courses c
JOIN semesters sem ON c.semester = sem.id
JOIN subjects subj ON c.subject = subj.id
JOIN orgunits org ON subj.offeredby = org.id
WHERE sem.year = 2012
  AND org.longname = 'School of Computer Science and Engineering';



-- Q6 incorrect
CREATE OR REPLACE VIEW Q6(count) AS
SELECT COUNT(DISTINCT p.id)
FROM people p
JOIN staff_roles sr ON p.id = sr.id
JOIN course_staff cs ON p.id = cs.staff
JOIN courses c ON cs.course = c.id
JOIN semesters sem ON c.semester = sem.id
WHERE sem.year = 2012
  AND sr.name = 'Course Lecturer'
  AND EXISTS (
    SELECT 1
    FROM affiliations aff
    JOIN orgunits org ON aff.orgunit = org.id
    WHERE aff.staff = p.id
      AND org.longname = 'School of Computer Science and Engineering'
  );



-- Q7 missing tuples
CREATE OR REPLACE VIEW Q7(course_id, unswid) AS
SELECT DISTINCT c.id AS course_id, p.unswid
FROM courses c
JOIN subjects subj ON c.subject = subj.id
JOIN orgunits org ON subj.offeredby = org.id
JOIN semesters sem ON c.semester = sem.id
JOIN course_staff cs ON c.id = cs.course
JOIN staff_roles sr ON cs.staff = sr.id AND sr.name = 'Course Lecturer'
JOIN people p ON sr.id = p.id
WHERE sem.year = 2012
  AND org.longname = 'School of Computer Science and Engineering'
  AND EXISTS (
    SELECT 1
    FROM affiliations aff
    JOIN orgunits org_staff ON aff.orgunit = org_staff.id
    WHERE aff.staff = p.id
      AND org_staff.longname = 'School of Computer Science and Engineering'
  );



-- Q8 missing tuples
DROP VIEW IF EXISTS Q8 CASCADE;
CREATE OR REPLACE VIEW Q8(course_id, unswid) AS
WITH cse_courses AS (
    SELECT c.id AS course_id
    FROM courses c
    JOIN subjects subj ON c.subject = subj.id
    JOIN orgunits org ON subj.offeredby = org.id
    JOIN semesters sem ON c.semester = sem.id
    WHERE sem.year = 2012
      AND org.longname = 'School of Computer Science and Engineering'
),
course_lecturers AS (
    SELECT cs.course, p.id AS staff_id, p.unswid
    FROM course_staff cs
    JOIN staff_roles sr ON cs.staff = sr.id AND sr.name = 'Course Lecturer'
    JOIN people p ON sr.id = p.id
),
cse_staff AS (
    SELECT DISTINCT aff.staff
    FROM affiliations aff
    JOIN orgunits org ON aff.orgunit = org.id
    WHERE org.longname = 'School of Computer Science and Engineering'
)
SELECT cc.course_id, cl.unswid
FROM cse_courses cc
JOIN course_lecturers cl ON cc.course_id = cl.course
WHERE NOT EXISTS (
    SELECT 1
    FROM course_lecturers cl2
    WHERE cl2.course = cc.course_id
      AND cl2.staff_id NOT IN (SELECT staff FROM cse_staff)
);



-- Q9
CREATE OR REPLACE FUNCTION Q9(subject1 INTEGER, subject2 INTEGER) RETURNS TEXT
AS $$
DECLARE
    subject1_code text;
    subject2_prereq text;
BEGIN
    SELECT code INTO subject1_code
    FROM subjects
    WHERE id = subject1;

    SELECT _prereq INTO subject2_prereq
    FROM subjects
    WHERE id = subject2;

    IF subject2_prereq ~ ('\m' || subject1_code || '\M') THEN
        RETURN subject1 || ' is a direct prerequisite of ' || subject2 || '.';
    ELSE
        RETURN subject1 || ' is not a direct prerequisite of ' || subject2 || '.';
    END IF;
END;
$$ LANGUAGE plpgsql;



-- Q10 10eIncorrect
CREATE OR REPLACE FUNCTION Q10(subject1 INTEGER, subject2 INTEGER) RETURNS TEXT
AS $$
DECLARE
    is_prereq boolean;
BEGIN
    WITH RECURSIVE prereq_chain(id, code, _prereq) AS (
        SELECT id, code, _prereq
        FROM subjects
        WHERE id = subject2
    UNION ALL
        SELECT s.id, s.code, s._prereq
        FROM subjects s, prereq_chain pc
        WHERE pc._prereq ~ ('\m' || s.code || '\M')
    )
    SELECT EXISTS (
        SELECT 1
        FROM prereq_chain
        WHERE id = subject1
    ) INTO is_prereq;

    IF is_prereq THEN
        RETURN subject1 || ' is a prerequisite of ' || subject2 || '.';
    ELSE
        RETURN subject1 || ' is not a prerequisite of ' || subject2 || '.';
    END IF;
END;
$$ LANGUAGE plpgsql;