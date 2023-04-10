from flask import Blueprint, render_template, current_app

admin_routes = Blueprint('admin_routes', __name__, template_folder='templates')

@admin_routes.route('/courses')
def courses():
    # Get the MySQL connection from the main app
    mysql = current_app.config.get('mysql')

    # ... (rest of the code)

    cur = mysql.connection.cursor()

    # Fetch all courses from the Course table
    cur.execute("SELECT course_id, name FROM Course")
    courses = cur.fetchall()

    # Close the cursor
    cur.close()

    return render_template('admin.html', courses=courses)
