from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder='templates')


# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nawawi",
    database="SSISwebapp"
)
cursor = db.cursor()



@app.route('/')
def index():
    # Display a list of students, courses, and colleges
    # You'll need to implement the database queries here
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    
    cursor.execute("SELECT * FROM college")
    colleges = cursor.fetchall()
    
    return render_template('index.html', students=students, courses=courses, colleges=colleges)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course_code = request.form['course_code']
        year = request.form['year']
        gender = request.form['gender']

        # Get the current year
        current_year = datetime.now().year

        # Find the next available student ID for the current year
        cursor.execute("SELECT IFNULL(MAX(CONVERT(SUBSTRING(id, 6), SIGNED)), 0) + 1 FROM student WHERE SUBSTRING(id, 1, 4) = %s", (current_year,))
        next_student_id = cursor.fetchone()[0]

        # Generate the new student ID
        new_id = f"{current_year}-{str(next_student_id).zfill(4)}"

        # Insert data into the database
        cursor.execute("INSERT INTO student (id, firstname, lastname, course_code, year, gender) VALUES (%s, %s, %s, %s, %s, %s)",
                       (new_id, firstname, lastname, course_code, year, gender))
        db.commit()

        return redirect('/students')  # Redirect to the students' list
    else:
        cursor.execute("SELECT * FROM course")
        courses = cursor.fetchall()
        return render_template('add_student.html', courses=courses)

@app.route('/students')
def list_students():
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    return render_template('students.html', students=students)

@app.route('/edit_student/<string:id>')
def edit_student(id):
    cursor.execute("SELECT * FROM student WHERE id = %s", (id,))
    student = cursor.fetchone()
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    return render_template('edit_student.html', student=student, courses=courses)

@app.route('/update_student/<string:id>', methods=['POST'])
def update_student(id):
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    course_code = request.form['course']
    year = request.form['year']
    gender = request.form['gender']
    
    cursor.execute("UPDATE student SET firstname=%s, lastname=%s, course_code=%s, year=%s, gender=%s WHERE id=%s", (firstname, lastname, course_code, year, gender, id))
    db.commit()
    
    return redirect(url_for('list_students'))

@app.route('/delete_student/<string:id>')
def delete_student(id):
    cursor.execute("DELETE FROM student WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('list_students'))

@app.route('/search_students', methods=['POST'])
def search_students():
    search_column = request.form['search_column']
    search_query = request.form['search_query']

    # Perform a case-insensitive search query in your database using ILIKE
    cursor.execute(f"SELECT * FROM student WHERE {search_column} = %s", (search_query,))
    students = cursor.fetchall()

    return render_template('students.html', students=students)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        college_code = request.form['college_code']  # Updated field name
        
        # Insert data into the database
        cursor.execute("INSERT INTO course (code, name, college_code) VALUES (%s, %s, %s)", (code, name, college_code))
        db.commit()
        
        return redirect('/courses')  # Redirect to the courses list
    else:
        cursor.execute("SELECT * FROM college")
        colleges = cursor.fetchall()
        return render_template('add_course.html', colleges=colleges)



@app.route('/courses')
def list_courses():
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    return render_template('courses.html', courses=courses)

@app.route('/edit_course/<string:code>')
def edit_course(code):
    cursor.execute("SELECT * FROM course WHERE code = %s", (code,))
    course = cursor.fetchone()
    cursor.execute("SELECT * FROM college")
    colleges = cursor.fetchall()
    return render_template('edit_course.html', course=course, colleges=colleges)

@app.route('/update_course/<string:code>', methods=['POST'])
def update_course(code):
    name = request.form['name']
    college_code = request.form['college']
    
    cursor.execute("UPDATE course SET name=%s, college_code=%s WHERE code=%s", (name, college_code, code))
    db.commit()
    
    return redirect(url_for('list_courses'))


@app.route('/delete_course/<string:code>', methods=['GET'])
def delete_course(code):
    # First, delete the students associated with the course
    cursor.execute("DELETE FROM student WHERE course_code = %s", (code,))
    
    # Next, delete the course
    cursor.execute("DELETE FROM course WHERE code = %s", (code,))
    
    db.commit()
    
    return redirect('/courses')


@app.route('/search_courses', methods=['POST'])
def search_courses():
    search_column = request.form['search_column']
    search_query = request.form['search_query']

    # Modify your database query to search in the specified column
    cursor.execute("SELECT * FROM course WHERE {} LIKE %s".format(search_column), ('%' + search_query + '%',))
    courses = cursor.fetchall()

    return render_template('courses.html', courses=courses)

@app.route('/add_college', methods=['GET', 'POST'])
def add_college():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        
        # Insert data into the database
        cursor.execute("INSERT INTO college (code, name) VALUES (%s, %s)", (code, name))
        db.commit()
        
        return redirect('/colleges')  # Redirect to the colleges list
    else:
        return render_template('add_college.html')


@app.route('/colleges')
def list_colleges():
    cursor.execute("SELECT * FROM college")
    colleges = cursor.fetchall()
    return render_template('colleges.html', colleges=colleges)

@app.route('/edit_college/<string:code>')
def edit_college(code):
    cursor.execute("SELECT * FROM college WHERE code = %s", (code,))
    college = cursor.fetchone()
    return render_template('edit_college.html', college=college)

@app.route('/update_college/<string:code>', methods=['POST'])
def update_college(code):
    name = request.form['name']
    cursor.execute("UPDATE college SET name = %s WHERE code = %s", (name, code))
    db.commit()
    return redirect(url_for('list_colleges'))
    

@app.route('/delete_college/<string:code>', methods=['GET'])
def delete_college(code):
    # First, retrieve all courses associated with the college
    cursor.execute("SELECT code FROM course WHERE college_code = %s", (code,))
    courses = cursor.fetchall()
    
    # Next, delete all the students associated with those courses
    for course in courses:
        cursor.execute("DELETE FROM student WHERE course_code = %s", (course[0],))
    
    # Next, delete the courses associated with the college
    cursor.execute("DELETE FROM course WHERE college_code = %s", (code,))
    
    # Finally, delete the college
    cursor.execute("DELETE FROM college WHERE code = %s", (code,))
    
    db.commit()
    
    return redirect(url_for('list_colleges'))


@app.route('/search_colleges', methods=['POST'])
def search_colleges():
    search_column = request.form['search_column']
    search_query = request.form['search_query']

    # Modify your database query to search in the specified column
    cursor.execute("SELECT * FROM college WHERE {} LIKE %s".format(search_column), ('%' + search_query + '%',))
    colleges = cursor.fetchall()

    return render_template('colleges.html', colleges=colleges)


if __name__ == '__main__':
    app.run(debug=True)
