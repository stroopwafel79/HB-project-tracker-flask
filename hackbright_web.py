"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/")
def show_homepage():

    student_list = hackbright.get_student_list()
    project_list = hackbright.get_project_list()

    return render_template("homepage.html",
                            students=student_list,
                            projects=project_list)


@app.route("/student/<github>")
def get_student(github):
    """Show information about a student."""

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

    return redirect("/")


@app.route("/project/<title>")
def get_project(title):
    """Given title, get title, descr, and max grade of project"""

    row = hackbright.get_project_by_title(title)
    student_list = hackbright.get_grades_by_title(title)

    return render_template("project_info.html",
                           row=row,
                           student_list=student_list)


@app.route("/new-project")
def new_project():
    """Display form to collect new project info."""

    return render_template("new_project.html")


@app.route("/add/project", methods=['POST'])
def add_project():
    """Adds a project to the database."""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    row = hackbright.make_new_project(title, description, max_grade)

    return redirect("/")

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, port=5555)
