"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    row = hackbright.get_grades_by_github(github) 

    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           row=row)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/new-student")
def new_student():
    """Display form to collect new student info."""

    return render_template("new_student.html")

@app.route("/add/student", methods=['POST'])
def add_student():
    """Adds a student to the database."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_info.html", first=first_name, last=last_name, github=github)

@app.route("/project/<title>")
def get_project(title):
    """Given title, get title, descr, and max grade of project"""

    row = hackbright.get_project_by_title(title)

    return render_template("project_info.html", row=row)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, port=5555)
