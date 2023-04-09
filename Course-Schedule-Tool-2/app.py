from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
from admin_routes import admin_routes

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '3GUv878pnS@n'
app.config['MYSQL_DB'] = 'sql_schedule_database'

mysql = MySQL(app)

# Set a secret key for session management
app.secret_key = 'your_secret_key'

app.register_blueprint(admin_routes)


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/create-account')
def create_account():
    return render_template('create_account.html')


#Processes the create account page
@app.route('/create_account', methods=['POST'])
def createAccount():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        f_name = request.form['f_name']
        f_name = request.form['l_name']
        
        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()
        
        # Check if the submitted username exists in the Login table
        cur.execute("SELECT student_id, admin_id FROM Login WHERE username = %s", (username,))
        account = cur.fetchone()
        
        # If an account is found, display an error message
        if account:
            error_message = "Error: account with this username already exists"
            return render_template('create_account.html', status_message=error_message)

        cur.execute("INSERT INTO Login (username, password, f_name, l_name) VALUES (%s, %s, %s, %s)", (username, password, f_name, l_name))
        
        # Commit the changes to the database and close the cursor
        mysql.connection.commit()
        cur.close()
        
        # Redirect the user to the create account page with a success message
        success_message = "Account successfully created"
        return render_template('create_account.html', status_message=success_message)

    
    
#Processes the login page
@app.route('/login', methods=['POST'])
def authenticate():
    if request.method == 'POST':
        # Get the submitted form data
        username = request.form['username']
        password = request.form['password']

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Check if the submitted username and password exist in the Login table
        cur.execute("SELECT student_id, admin_id FROM Login WHERE username = %s AND password = %s", (username, password))

        account = cur.fetchone()

        # If an account is found, log in the user
        if account:
            session['loggedin'] = True
            session['username'] = username

            # Check if the account is an admin or student account
            if account[0] is None:  # Check if the account is an admin account (student_id is None)
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('student'))
        else:
            flash('Incorrect username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        # Get the submitted form data
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Insert the student data into the students table
        insert_query = "INSERT INTO Student (student_id, f_name, l_name) VALUES (%s, %s, %s)"
        cur.execute(insert_query, (student_id, first_name, last_name))

        # Commit the changes to the database and close the cursor
        mysql.connection.commit()
        cur.close()


        # Redirect to the admin page
        return redirect(url_for('admin'))

    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)
