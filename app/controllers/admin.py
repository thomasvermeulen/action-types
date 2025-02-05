from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db
from app.models.student import Student
from app.models.response import Response
from app.models.teacher import Teacher
from sqlalchemy import func
import csv

bp = Blueprint('admin', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Teacher.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Ongeldige gebruikersnaam of wachtwoord')
            return redirect(url_for('admin.login'))
        login_user(user)
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = 20

    classes = db.session.query(Student.student_class).distinct().order_by(Student.student_class).all()
    classes = [c[0] for c in classes]

    teams = db.session.query(Student.team).distinct().order_by(Student.team).all()
    teams = [t[0] for t in teams if t[0]]

    query = db.session.query(Student).outerjoin(Response).group_by(Student.id)

    class_filter = request.args.get('class')
    team_filter = request.args.get('team')

    if class_filter:
        query = query.filter(Student.student_class == class_filter)
    if team_filter:
        query = query.filter(Student.team == team_filter)

    total_students = query.count()

    students = query.order_by(Student.student_number).offset((page - 1) * per_page).limit(per_page).all()

    return render_template('admin/dashboard.html', students=students, classes=classes, teams=teams, page=page, per_page=per_page, total_students=total_students, has_next=total_students > (page * per_page))

@bp.route('/student/add', methods=['POST'])
@login_required
def add_student():
    student_number = request.form.get('student_number')
    name = request.form.get('name')
    student_class = request.form.get('student_class')

    if not student_number or not name or not student_class:
        flash('Alle velden zijn verplicht!')
        return redirect(url_for('admin.dashboard'))

    existing_student = Student.query.filter_by(student_number=student_number).first()
    if existing_student:
        flash('Studentnummer bestaat al!')
        return redirect(url_for('admin.dashboard'))

    new_student = Student(student_number=student_number, name=name, student_class=student_class, team=None, action_type=None)
    db.session.add(new_student)
    db.session.commit()
    flash('Student succesvol toegevoegd!')
    return redirect(url_for('admin.dashboard'))

@bp.route('/student/delete/<int:student_number>', methods=['POST'])
@login_required
def delete_student(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        flash('Student verwijderd!')
    else:
        flash('Student niet gevonden!')
    return redirect(url_for('admin.dashboard'))

@bp.route('/teacher/add', methods=['POST'])
@login_required
def add_teacher():
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'on'

    if not username or not name or not password:
        flash('Alle velden zijn verplicht!')
        return redirect(url_for('admin.dashboard'))

    existing_teacher = Teacher.query.filter_by(username=username).first()
    if existing_teacher:
        flash('Gebruikersnaam bestaat al!')
        return redirect(url_for('admin.dashboard'))

    new_teacher = Teacher(username=username, name=name, is_admin=is_admin)
    new_teacher.set_password(password)
    db.session.add(new_teacher)
    db.session.commit()
    flash('Docent succesvol toegevoegd!')
    return redirect(url_for('admin.dashboard'))

@bp.route('/student/edit/<int:student_number>', methods=['POST'])
@login_required
def edit_student(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        flash('Student niet gevonden!')
        return redirect(url_for('admin.dashboard'))

    student.name = request.form.get('name')
    student.student_class = request.form.get('student_class')
    student.team = request.form.get('team')
    db.session.commit()
    flash('Studentgegevens bijgewerkt!')
    return redirect(url_for('admin.dashboard'))

@bp.route("/export", methods=["GET"])
def export_csv():
    student_class = request.args.get("class", "")
    team = request.args.get("team", "")

    query = db.session.query(
        Student,
        func.max(Response.response_date).label("completion_date")
    ).outerjoin(Response).group_by(Student.id)

    if student_class:
        query = query.filter(Student.student_class == student_class)
    if team:
        query = query.filter(Student.team == team)

    students = query.all()

    output = "Studentnummer,Naam,Klas,Team,Action Type,Datum\n"
    for student, completion_date in students:
        output += f"{student.student_number},{student.name},{student.student_class},{student.team or '-'},"
        output += f"{student.action_type or '-'},"
        output += f"{completion_date.strftime('%Y-%m-%d %H:%M') if completion_date else '-'}\n"

    response = make_response(output)
    response.headers["Content-Disposition"] = "attachment; filename=student_export.csv"
    response.headers["Content-Type"] = "text/csv"

    return response