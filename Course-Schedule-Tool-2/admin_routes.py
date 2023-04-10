from flask import Blueprint, render_template, current_app, request, redirect, url_for

admin_routes = Blueprint('admin_routes', __name__, template_folder='templates')

@admin_routes.route('/courses')
def admin():
    mysql = current_app.config['mysql'] #MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    # Create a cursor to interact with the database
    cur = mysql.connection.cursor()
    
    # Execute a SELECT query to get the courses from the database
    cur.execute("SELECT * FROM Course")
    courses = cur.fetchall()
    
    # Close the cursor
    cur.close()

    return render_template('admin.html', courses=courses)

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