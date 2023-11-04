# app/routes.py

from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.models.course import get_courses, add_course, get_course_by_code, update_course, delete_course, search_courses
from app.models.student import get_students, add_student, get_student_by_id, update_student, delete_student, search_students
from app.models.college import get_colleges, add_college, get_college_by_code, update_college, delete_college, search_colleges

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    students = get_students()
    return render_template('student.html', students=students, courses=get_courses())


@app.route('/add_student', methods=['POST'])
def add_student_route():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    course_code = request.form['course_code']
    year = request.form['year']
    gender = request.form['gender']

    add_student(firstname, lastname, course_code, year, gender)
    flash(f'Student successfully added!', 'success')
    return redirect('/students')

@app.route('/edit_student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'GET':
        student = get_student_by_id(student_id)
        courses = get_courses()  # Retrieve the list of courses
        return render_template('edit_student.html', student=student, courses=courses)  # Pass courses to the template
    elif request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        course_code = request.form['course_code']
        year = request.form['year']
        gender = request.form['gender']

        update_student(student_id, firstname, lastname, course_code, year, gender)

        return redirect(url_for('students'))

@app.route('/delete_student/<student_id>')
def delete_student_route(student_id):
    delete_student(student_id)
    return redirect('/students')

@app.route('/search_student', methods=['POST'])
def search_student():
    search_by = request.form['search_by']
    search_term = request.form['search_term']
    
    students = search_students(search_by, search_term)
    return render_template('student.html', students=students)













@app.route('/colleges')
def colleges():
    colleges = get_colleges()
    return render_template('college.html', colleges=colleges)

@app.route('/add_college', methods=['POST'])
def add_college_route():
    code = request.form['code']
    name = request.form['name']

    # Check if the college with the same code already exists
    existing_college = get_college_by_code(code)
    if existing_college:
        flash(f'College with code {code} already exists!', 'warning')
    else:
        # Add the college if it doesn't exist
        add_college(code, name)
        flash(f'College successfully added!', 'success')
    
    return redirect('/colleges')


@app.route('/search_college', methods=['POST'])
def search_college():
    search_by = request.form['search_by']
    search_term = request.form['search_term']

    colleges = search_colleges(search_by, search_term)

    return render_template('college.html', colleges=colleges)

@app.route('/edit_college/<college_code>', methods=['GET', 'POST'])
def edit_college(college_code):
    if request.method == 'GET':
        college = get_college_by_code(college_code)
        return render_template('edit_college.html', college=college)
    elif request.method == 'POST':
        name = request.form['name']

        update_college(college_code, name)

        return redirect(url_for('colleges'))

@app.route('/delete_college/<code>')
def delete_college_route(code):
    delete_college(code)
    return redirect('/colleges')

    









@app.route('/courses')
def courses():
    courses = get_courses()
    colleges = get_colleges()
    return render_template('course.html', courses=courses, colleges=colleges)

@app.route('/add_course', methods=['POST'])
def add_course_route():
    code = request.form['code']
    name = request.form['name']
    college_code = request.form['college_code']

    # Check if the course with the same code already exists
    existing_course = get_course_by_code(code)
    if existing_course:
        flash(f'Course with code {code} already exists!', 'warning')
    else:
        # Add the course if it doesn't exist
        add_course(code, name, college_code)
        flash(f'Course successfully added!', 'success')
    
    return redirect('/courses')


@app.route('/search_course', methods=['POST'])
def search_course():
    search_by = request.form['search_by']
    search_term = request.form['search_term']

    courses = search_courses(search_by, search_term)

    return render_template('course.html', courses=courses)

@app.route('/edit_course/<course_code>', methods=['GET', 'POST'])
def edit_course(course_code):
    if request.method == 'GET':
        course = get_course_by_code(course_code)
        colleges = get_colleges()  # Retrieve the list of colleges
        return render_template('edit_course.html', course=course, colleges=colleges)  # Pass colleges to the template
    elif request.method == 'POST':
        name = request.form['name']
        college_code = request.form['college_code']

        update_course(course_code, name, college_code)

        return redirect(url_for('courses'))

@app.route('/delete_course/<code>')
def delete_course_route(code):
    delete_course(code)
    return redirect('/courses')


