# db_operations.py
from flask import current_app as app

def add_student(student_id, first_name, last_name):
    mysql = app.config['MYSQL']
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO Student(student_id, first_name, last_nam) VALUES (%s, %s, %s)",
        (student_id, first_name, last_name)
    )
    mysql.connection.commit()
    cur.close()
