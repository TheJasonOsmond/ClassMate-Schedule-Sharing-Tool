from flask import Flask, request, render_template, redirect, url_for
from students.student_routes import add_student_route
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

app.add_url_rule('/add_student', view_func=add_student_route, methods=['POST'])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
