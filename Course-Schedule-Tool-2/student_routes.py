from flask import Blueprint, render_template, current_app, request, redirect, url_for, session, flash

student_routes = Blueprint('student_routes', __name__, template_folder='templates')

@student_routes.route('/student')
def student():
    mysql = current_app.config['mysql']  # MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    cur = mysql.connection.cursor()
    
    # Access session data
    if 'loggedin' in session and session['loggedin']:
        username = session['username']
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))
    
    # Execute a SELECT query to get the courses from the database
    cur.execute("SELECT * FROM Courses")
    courses = cur.fetchall()
    
    cur.execute("SELECT * FROM Courses WHERE course_id IN (\
                SELECT course_id FROM CourseList WHERE student_id = %s)", (session['student_id'],))
    schedule = cur.fetchall()

    #TODO Join With login to get the usernames of friends
    cur.execute("SELECT * FROM Student WHERE student_id IN (SELECT student_id FROM Friends WHERE friend_id = %s \
                UNION \
                SELECT friend_id FROM Friends WHERE student_id = %s)", (session['student_id'], session['student_id']))
    friends = cur.fetchall()

    return render_template('student.html', username=username, courses=courses, schedule = schedule,  friends= friends)

@student_routes.route('/course-details/<int:course_id>')
def course_details(course_id):
    mysql = current_app.config['mysql']

    # Access session data
    if 'loggedin' not in session or not session['loggedin']:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

    course_info = get_course_details(mysql, course_id)
    return render_template('course_details.html', course_info=course_info)

# TODO: Adds course that you clicked to schedule
@student_routes.route('/add_course_to_schedule', methods=['POST'])
def add_course_to_schedule():
    mysql = current_app.config['mysql']
    if request.method == 'POST':
        course_id = request.form['course_id']
        student_id = session['student_id']
        cur = mysql.connection.cursor()

        # Check if the entry already exists
        cur.execute("SELECT * FROM CourseList WHERE student_id = %s AND course_id = %s", (student_id, course_id))
        existing_entry = cur.fetchone()

        # If the entry does not exist, insert it
        if existing_entry is None:
            cur.execute("INSERT INTO CourseList(student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
            mysql.connection.commit()

        cur.close()
        return redirect(url_for('student_routes.student'))
    else:
        return redirect(url_for('student_routes.student'))


@student_routes.route('/remove_course_from_schedule', methods=['POST'])
def remove_course_from_schedule():
    mysql = current_app.config['mysql']
    if request.method == 'POST':
        course_id = request.form['course_id']
        student_id = session['student_id']
        cur = mysql.connection.cursor()

        # Delete the entry from the CourseList table
        cur.execute("DELETE FROM CourseList WHERE student_id = %s AND course_id = %s", (student_id, course_id))
        mysql.connection.commit()

        cur.close()
        return redirect(url_for('student_routes.student'))
    else:
        return redirect(url_for('student_routes.student'))
    
    
# ========== FRIENDS LIST ==========

# Might be able to do something with this
@student_routes.route('/friends_list')
def friends_list():
    return redirect(url_for('student_routes.student'))

@student_routes.route('/add_friend', methods=['POST'])
def add_friend():
    mysql = current_app.config['mysql']
    if request.method == 'POST':
        friend_username = request.form['friend_username']
        student_id = session['student_id']
        cur = mysql.connection.cursor()

        # Check if the user with the given username exists
        cur.execute("SELECT student_id FROM LOGIN WHERE username = %s", (friend_username,))
        friend = cur.fetchone()

        if friend is None:
            flash('No user found with the given username', 'error')
            return redirect(url_for('student_routes.friends_list'))

        friend_id = friend[0]

        # Check if they are already friends
        cur.execute("SELECT * FROM Friends WHERE (student_id = %s AND friend_id = %s) OR (student_id = %s AND friend_id = %s)", (student_id, friend_id, friend_id, student_id))
        existing_friendship = cur.fetchone()

        if existing_friendship is not None:
            flash('You are already friends with this user', 'error')
            return redirect(url_for('student_routes.friends_list'))

        # Add the friend
        cur.execute("INSERT INTO Friends (student_id, friend_id) VALUES (%s, %s)", (student_id, friend_id))
        mysql.connection.commit()

        cur.close()
        flash('Friend added successfully!', 'success')
        return redirect(url_for('student_routes.friends_list'))
    else:
        return redirect(url_for('student_routes.friends_list'))

@student_routes.route('/remove_friend', methods=['POST'])
def remove_friend():
    mysql = current_app.config['mysql']
    if request.method == 'POST':
        friend_id = request.form['friend_id']
        student_id = session['student_id']
        cur = mysql.connection.cursor()

        # Delete the friend entry from the Friends table
        cur.execute("DELETE FROM Friends WHERE (student_id = %s AND friend_id = %s) OR (student_id = %s AND friend_id = %s)", (student_id, friend_id, friend_id, student_id))
        mysql.connection.commit()

        cur.close()
        return redirect(url_for('student_routes.friends_list'))
    else:
        return redirect(url_for('student_routes.friends_list'))
    
    
          

def get_student_schedule(mysql, student_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT c.course_id, c.name FROM Courses c JOIN Student_Courses sc ON c.course_id = sc.course_id WHERE sc.student_id = %s", (student_id,))
    schedule = cursor.fetchall()
    cursor.close()
    conn.close()
    return schedule

def get_course_details(mysql, course_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT c.course_id, c.name, CONCAT(p.f_name, ' ', p.l_name) as professor, c.info, CONCAT(c.time, ' at Building ', c.building_id, ', Room ', c.room_id) as time_location FROM Courses c JOIN Professor p ON c.professor_id = p.professor_id WHERE c.course_id = %s", (course_id,))
    course_info = cursor.fetchone()
    cursor.close()
    conn.close()
    return course_info
