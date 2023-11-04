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

def add_student(firstname, lastname, course_code, year, gender):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO student (firstname, lastname, course_code, year, gender) VALUES (%s, %s, %s, %s, %s)",
                (firstname, lastname, course_code, year, gender))
    mysql.connection.commit()
    cur.close()

def get_student_by_id(student_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    return student

# Add a function to update a student's data
def update_student(student_id, firstname, lastname, course_code, year, gender):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE student SET firstname = %s, lastname = %s, course_code = %s, year = %s, gender = %s WHERE id = %s", (firstname, lastname, course_code, year, gender, student_id))
    mysql.connection.commit()
    cur.close()

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
        # Convert both the search term and gender column to lowercase for case-insensitive search
        cur.execute("SELECT * FROM student WHERE LOWER(gender) = LOWER(%s)", (search_term,))
    students = cur.fetchall()
    cur.close()
    return students
