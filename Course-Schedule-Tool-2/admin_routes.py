from flask import Blueprint, render_template

admin_routes = Blueprint('admin_routes', __name__, template_folder='templates')

def setup_routes(app, mysql):
    @admin_routes.route('/admin')
    def admin():
        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()
        
        # Execute a SELECT query to get the courses from the database
        cur.execute("SELECT * FROM Course")
        courses = cur.fetchall()
        
        # Close the cursor
        cur.close()

        return render_template('admin.html', courses=courses)
