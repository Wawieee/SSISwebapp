from app import mysql

def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    students = cur.fetchall()
    cur.close()
    return students

def get_courses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT code FROM course")
    courses = cur.fetchall()
    cur.close()
    return courses

def add_student(id, firstname, lastname, course_code, year, gender):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO student (id, firstname, lastname, course_code, year, gender) VALUES (%s, %s, %s, %s, %s, %s)",
                (id, firstname, lastname, course_code, year, gender))
    mysql.connection.commit()
    cur.close()

def is_student_id_unique(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM student WHERE id = %s", (id,))
    count = cur.fetchone()[0]
    cur.close()
    return count == 0

def get_student_by_id(student_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    return student

def update_student(original_student_id, student_id, firstname, lastname, course_code, year, gender):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE student SET id = %s, firstname = %s, lastname = %s, course_code = %s, year = %s, gender = %s WHERE id = %s",
        (student_id, firstname, lastname, course_code, year, gender, original_student_id))
    mysql.connection.commit()
    cur.close()


def check_student_id_exists(student_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    result = cur.fetchone()
    cur.close()
    return result is not None

def delete_student(student_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE id = %s", (student_id,))
    mysql.connection.commit()
    cur.close()

def search_students(search_by, search_term):
    cur = mysql.connection.cursor()
    if search_by == 'id':
        cur.execute("SELECT * FROM student WHERE id LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'firstname':
        cur.execute("SELECT * FROM student WHERE firstname LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'lastname':
        cur.execute("SELECT * FROM student WHERE lastname LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'course_code':
        cur.execute("SELECT * FROM student WHERE course_code LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'year':
        cur.execute("SELECT * FROM student WHERE year = %s", (int(search_term),))
    elif search_by == 'gender':
        cur.execute("SELECT * FROM student WHERE LOWER(gender) = LOWER(%s)", (search_term,))
    students = cur.fetchall()
    cur.close()
    return students


def search_students_with_course(search_by, search_term): 
    cur = mysql.connection.cursor()

    if search_by == 'id':
        cur.execute("SELECT s.*, c.name AS course_name FROM student s LEFT JOIN course c ON s.course_code = c.code WHERE s.id LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'firstname':
        cur.execute("SELECT s.*, c.name AS course_name FROM student s LEFT JOIN course c ON s.course_code = c.code WHERE s.firstname LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'lastname':
        cur.execute("SELECT s.*, c.name AS course_name FROM student s LEFT JOIN course c ON s.course_code = c.code WHERE s.lastname LIKE %s", ('%' + search_term + '%',))
    elif search_by == 'course_code':
        cur.execute("SELECT s.*, c.name AS course_name FROM student s LEFT JOIN course c ON s.course_code = c.code WHERE s.course_code LIKE %s OR c.name LIKE %s", ('%' + search_term + '%', '%' + search_term + '%'))
    elif search_by == 'year':
        cur.execute("SELECT s.*, c.name AS course_name FROM student s LEFT JOIN course c ON s.course_code = c.code WHERE s.year = %s", (int(search_term),))
    elif search_by == 'gender':
        cur.execute("SELECT s.*, c.name AS course_name FROM student s LEFT JOIN course c ON s.course_code = c.code WHERE LOWER(s.gender) = LOWER(%s)", (search_term,))

    students = cur.fetchall()
    cur.close()
    return students


def get_students_with_course():
    cur = mysql.connection.cursor()
    cur.execute("SELECT student.id, student.firstname, student.lastname, student.course_code, student.year, student.gender, course.name FROM student JOIN course ON student.course_code = course.code")
    students = cur.fetchall()
    cur.close()
    return students
