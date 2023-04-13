from flask import Blueprint, render_template, current_app, request, redirect, url_for

admin_routes = Blueprint('admin_routes', __name__, template_folder='templates')

@admin_routes.route('/admin')
@admin_routes.route('/admin/<active_tab>')
def admin(active_tab=None):
    mysql = current_app.config['mysql'] #MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    # Create a cursor to interact with the database
    cur = mysql.connection.cursor()
    
    # Execute a SELECT query to get the courses from the database
    cur.execute("SELECT * FROM Courses")
    courses = cur.fetchall()

    cur.execute("SELECT * FROM University")
    universities = cur.fetchall()

    cur.execute("SELECT * FROM Department")
    departments = cur.fetchall()

    # Fetch Professors data
    cur.execute("SELECT * FROM Professor")
    professors = cur.fetchall()

    # Fetch Rooms data
    cur.execute("SELECT * FROM Room")
    rooms = cur.fetchall()
    
    if active_tab == None:
        active_tab = 'coursesTab'

    # Close the cursor
    cur.close()

    return render_template('admin.html', courses=courses, universities=universities, departments=departments, professors=professors, rooms=rooms, active_tab=active_tab)

# ============== COURSES ============== #

@admin_routes.route('/delete_course', methods=['POST'])
def delete_course():
    mysql = current_app.config['mysql'] #MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    if request.method == 'POST':
        # Get the submitted form data
        course_id = request.form['course_id']

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Delete the course from the courses table
        delete_query = "DELETE FROM Courses WHERE course_id = %s"
        cur.execute(delete_query, (course_id,))

        # Commit the changes to the database and close the cursor
        mysql.connection.commit()
        cur.close()

        # Redirect to the admin page
        return redirect(url_for('admin_routes.admin', active_tab='coursesTab'))
    
    return redirect(url_for('admin_routes.admin', active_tab='coursesTab'))

@admin_routes.route('/add_course', methods=['POST'])
def add_course():
    mysql = current_app.config['mysql'] #MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    if request.method == 'POST':
        # Get the submitted form data
        course_name = request.form['course_name']
        university = request.form['university']
        department = request.form['department']
        professor_id = request.form['professor'] or None
        building_id = request.form['building_id'] or None
        room_id = request.form['room_id'] or None
        time = request.form['time'] or None
        info = request.form['info'] or None
        days = request.form['days'] or None
        
        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Insert the course data into the courses table
        insert_query = "INSERT INTO Courses (name, university, department, building_id, room_id, time, info, days, professor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(insert_query, (course_name, university, department, building_id, room_id, time, info, days, professor_id))

        # Commit the changes to the database and close the cursor
        mysql.connection.commit()
        cur.close()

        # Redirect to the admin page
        return redirect(url_for('admin_routes.admin', active_tab='coursesTab'))

    return redirect(url_for('admin_routes.admin', active_tab='coursesTab'))


# ============== UNIVERSITIES ============== #


@admin_routes.route('/add_university', methods=['POST'])
def add_university():
    mysql = current_app.config['mysql'] #MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    if request.method == 'POST':
        # Get the submitted form data
        name = request.form['name']
        location = request.form['location']

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Insert the university data into the University table
        insert_query = "INSERT INTO University (name, location) VALUES (%s, %s)"
        cur.execute(insert_query, (name, location))

        # Commit the changes to the database and close the cursor
        mysql.connection.commit()
        cur.close()

        # Redirect to the admin page
        return redirect(url_for('admin_routes.admin', active_tab='universitiesTab'))

    return redirect(url_for('admin_routes.admin', active_tab='universitiesTab'))


@admin_routes.route('/delete_university', methods=['POST'])
def delete_university():
    mysql = current_app.config['mysql'] #MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    if request.method == 'POST':
        # Get the submitted form data
        name = request.form['name']

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Delete the university from the University table
        delete_query = "DELETE FROM University WHERE name = %s"
        cur.execute(delete_query, [name])

        # Commit the changes to the database and close the cursor
        mysql.connection.commit()
        cur.close()

        # Redirect to the admin page
        return redirect(url_for('admin_routes.admin', active_tab='universitiesTab'))

    return redirect(url_for('admin_routes.admin', active_tab='universitiesTab'))


# ============== DEPARTMENTS ============== #


@admin_routes.route('/add_department', methods=['POST'])
def add_department():
    mysql = current_app.config['mysql']
    if request.method == 'POST':
        # Get the submitted form data
        name = request.form['name']
        university = request.form['university']

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Insert the department data into the Department table
        insert_query = "INSERT INTO Department (name, university) VALUES (%s, %s)"
        cur.execute(insert_query, (name, university))

        # Commit the changes to the database and close the cursor
        mysql.connection.commit()
        cur.close()

        # Redirect to the admin page
        return redirect(url_for('admin_routes.admin', active_tab='departmentsTab'))

    return redirect(url_for('admin_routes.admin', active_tab='departmentsTab'))
  
@admin_routes.route('/delete_department', methods=['POST'])
def delete_department():
    mysql = current_app.config['mysql']  # MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    if request.method == 'POST':
        # Get the submitted form data
        name = request.form['name']

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Delete the department from the Department table
        delete_query = "DELETE FROM Department WHERE name = %s"
        cur.execute(delete_query, [name])

        # Commit the changes to the database and close the cursor
        mysql.connection.commit()
        cur.close()

        # Redirect to the admin page
        return redirect(url_for('admin_routes.admin', active_tab='departmentsTab'))

    return redirect(url_for('admin_routes.admin', active_tab='departmentsTab'))

# ============== PROFESSORS ============== #

@admin_routes.route('/add_professor', methods=['POST'])
def add_professor():
    mysql = current_app.config['mysql']
    if request.method == 'POST':
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        department = request.form['department']
        university = request.form['university']

        cur = mysql.connection.cursor()

        insert_query = "INSERT INTO Professor (f_name, l_name, department, university) VALUES (%s, %s, %s, %s)"
        cur.execute(insert_query, (f_name, l_name, department, university))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin_routes.admin', active_tab='professorsTab'))

    return redirect(url_for('admin_routes.admin', active_tab='professorsTab'))


@admin_routes.route('/delete_professor', methods=['POST'])
def delete_professor():
    mysql = current_app.config['mysql']
    if request.method == 'POST':
        professor_id = request.form['professor_id']

        cur = mysql.connection.cursor()

        delete_query = "DELETE FROM Professor WHERE professor_id = %s"
        cur.execute(delete_query, [professor_id])

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin_routes.admin', active_tab='professorsTab'))

    return redirect(url_for('admin_routes.admin', active_tab='professorsTab'))

# ============== ROOMS ============== #
@admin_routes.route('/add_room', methods=['POST'])
def add_room():
    mysql = current_app.config['mysql']
    if request.method == 'POST':
        building_id = request.form['building_id']
        room_id = request.form['room_id']
        university = request.form['university']

        cur = mysql.connection.cursor()

        insert_query = "INSERT INTO Room (building_id, room_id, university) VALUES (%s, %s, %s)"
        cur.execute(insert_query, (building_id, room_id, university))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin_routes.admin', active_tab='roomsTab'))

    return redirect(url_for('admin_routes.admin', active_tab='roomsTab'))


@admin_routes.route('/delete_room', methods=['POST'])
def delete_room():
    mysql = current_app.config['mysql']
    if request.method == 'POST':
        building_id = request.form['building_id']
        room_id = request.form['room_id']
        university = request.form['university']

        cur = mysql.connection.cursor()

        delete_query = "DELETE FROM Room WHERE building_id = %s AND room_id = %s AND `university` = %s"
        cur.execute(delete_query, (building_id, room_id, university))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('admin_routes.admin', active_tab='roomsTab'))

    return redirect(url_for('admin_routes.admin', active_tab='roomsTab'))

