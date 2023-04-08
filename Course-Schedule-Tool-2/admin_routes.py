# admin_routes.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from db_operations import add_student

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/add_student', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        add_student(student_id, first_name, last_name,email)
        flash('Student added successfully.', 'success')
        return redirect(url_for('admin_routes.admin'))

    return render_template('admin.html')

@admin_routes.route('/admin')
def admin():
    return render_template('admin.html')


