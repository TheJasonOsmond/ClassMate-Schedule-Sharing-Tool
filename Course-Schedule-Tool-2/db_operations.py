# db_operations.py
from flask import current_app as app

def add_student(student_id, first_name, last_name, email):
    mysql = app.config['MYSQL']
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO Student(student_id, first_name, last_name, email) VALUES (%s, %s, %s, %s)",
        (student_id, first_name, last_name, email)
    )
    mysql.connection.commit()
    cur.close()
