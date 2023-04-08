from flask import Blueprint, request, render_template, redirect, url_for
from .db_student_functions import add_student

student_bp = Blueprint('student', __name__)

@student_bp.route('/add_student', methods=['POST'])
def add_student_route():
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    add_student(f_name, l_name)
    return redirect(url_for('index'))
