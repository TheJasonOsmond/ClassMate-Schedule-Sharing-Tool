from flask import Blueprint, render_template, current_app, request, redirect, url_for, session

student_routes = Blueprint('student_routes', __name__, template_folder='templates')

@student_routes.route('/student')
def student():
    mysql = current_app.config['mysql']  # MUST BE ADDED TO EACH ROUTE IN SUB_ROUTES LIKE THIS
    
    # Access session data
    if 'loggedin' in session and session['loggedin']:
        username = session['username']
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

    return render_template('student.html', username=username)


