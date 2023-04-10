from flask import Blueprint, render_template, current_app, request, redirect, url_for

admin_routes = Blueprint('admin_routes', __name__, template_folder='templates')

@admin_routes.route('/admin')
def admin():
    mysql = current_app.config['mysql'] #MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    # Create a cursor to interact with the database
    cur = mysql.connection.cursor()
    
    # Execute a SELECT query to get the courses from the database
    cur.execute("SELECT * FROM Course")
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
    
    # Close the cursor
    cur.close()

    return render_template('admin.html', courses=courses, universities=universities, departments=departments, professors=professors, rooms=rooms)



@admin_routes.route('/delete_course', methods=['POST'])
def delete_course():
    mysql = current_app.config['mysql'] #MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    if request.method == 'POST':
        # Get the submitted form data
        course_id = request.form['course_id']

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Delete the course from the courses table
        delete_query = "DELETE FROM Course WHERE course_id = %s"
        cur.execute(delete_query, (course_id,))

        # Commit the changes to the database and close the cursor
        mysql.connection.commit()
        cur.close()

        # Redirect to the admin page
        return redirect(url_for('admin_routes.admin'))


    return render_template('admin.html')

@admin_routes.route('/add_course', methods=['POST'])
def add_course():
    mysql = current_app.config['mysql'] #MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    if request.method == 'POST':
        # Get the submitted form data
        course_name = request.form['course_name']

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Insert the course data into the courses table
        insert_query = "INSERT INTO Course (name) VALUES (%s)"
        cur.execute(insert_query, (course_name,))


        # Commit the changes to the database and close the cursor
        mysql.connection.commit()
        cur.close()

        # Redirect to the admin page
        return redirect(url_for('admin_routes.admin'))

    return render_template('admin.html')


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
        return redirect(url_for('admin_routes.admin'))

    return render_template('admin.html')


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
        return redirect(url_for('admin_routes.admin'))

    return render_template('admin.html')
  