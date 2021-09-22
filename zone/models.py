from datetime import date
from zone import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    student = Student.query.get(user_id)
    department_faculty = Faculty.query.get(user_id)
    crc_faculty = CRC.query.get(user_id)
    if student:
        return student
    elif department_faculty:
        return department_faculty
    else:
        return crc_faculty


class Student(db.Model, UserMixin):
    user_id = db.Column(db.String(12), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.String(1), nullable=False)
    branch = db.Column(db.String(30), nullable=False)
    headline = db.Column(db.String(100), nullable=False, default='Student')
    about = db.Column(db.String(300))
    clg_name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.String(10), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='profile_default.jpg')
    skills = db.Column(db.String(500))
    password = db.Column(db.String(60), nullable=False)
    placement_info = db.Column(db.String(20), nullable=False, default="Not Placed")
    letter = db.Column(db.String(20))
    projects = db.relationship('Project', backref='creator', lazy=True)
    placement = db.relationship('PlacedStudent', backref='placed')

    def __repr__(self):
        return f"Student('{self.name}', '{self.email}', '{self.user_id}', '{self.year}', '{self.branch}', '{self.clg_name}'," \
               f" '{self.mobile}', '{self.image_file}')"

    def get_id(self):
        return self.user_id


class Faculty(db.Model, UserMixin):
    user_id = db.Column(db.String(12), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    branch = db.Column(db.String(30), nullable=False)
    clg_name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.String(10), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='profile_default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Faculty('{self.name}', '{self.email}', '{self.user_id}', '{self.branch}', '{self.clg_name}'," \
               f" '{self.mobile}', '{self.image_file}')"

    def get_id(self):
        return self.user_id


class CRC(db.Model, UserMixin):
    user_id = db.Column(db.String(12), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    clg_name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.String(10), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='profile_default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Faculty('{self.name}', '{self.email}', '{self.user_id}', '{self.clg_name}'," \
               f" '{self.mobile}', '{self.image_file}')"

    def get_id(self):
        return self.user_id


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_finished = db.Column(db.Date)
    description = db.Column(db.Text, nullable=False)
    project_link = db.Column(db.Text)
    project_image = db.Column(db.String(20), nullable=False, default='project_default.jpg')
    student_id = db.Column(db.Integer, db.ForeignKey('student.user_id'), nullable=False)

    def __repr__(self):
        return f"Project('{self.title}', '{self.date_finished}', '{self.project_image}', {self.project_link})"


class PlacedStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='profile_default.jpg')
    date_placed = db.Column(db.Date, nullable=False, default=date)
    package = db.Column(db.String(7), nullable=False)
    company_name = db.Column(db.String(30), nullable=False)
    noc = db.Column(db.String(20))
    student_id = db.Column(db.Integer, db.ForeignKey('student.user_id'), nullable=False)

    def __repr__(self):
        return f"PlacedStudent('{self.name}', '{self.date_placed}', '{self.company_name}', {self.package}, {self.noc})"


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False, default=date)
    pdf = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Announcement('{self.name}', '{self.date_issued}', '{self.context}' )"


class CRCAnnouncement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False, default=date)
    pdf = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Announcement('{self.name}', '{self.date_issued}', '{self.context}' )"


class Certificates(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credential = db.Column(db.String(50), unique=True, nullable=False)
    credential_url = db.Column(db.String(100), unique=True)
    date_issued = db.Column(db.String(10), nullable=False)
    date_expiry = db.Column(db.String(10))
    organisation_name = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.user_id'), nullable=False)

    def __repr__(self):
        return f"Certificate('{self.name}', '{self.credential}', '{self.student_id}', '{self.date_issued}'," \
               f" '{self.organisation_name}', '{self.image_file}')"


class Education(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.String(4), nullable=False)
    end_date = db.Column(db.String(4), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    organisation_name = db.Column(db.String(100), nullable=False)
    field = db.Column(db.String(10))
    student_id = db.Column(db.Integer, db.ForeignKey('student.user_id'), nullable=False)

    def __repr__(self):
        return f"Faculty('{self.name}', '{self.email}', '{self.user_id}', '{self.clg_name}'," \
               f" '{self.mobile}', '{self.image_file}')"


class Result(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sem = db.Column(db.String(2), nullable=False)
    nob = db.Column(db.String(2), nullable=False)
    percent = db.Column(db.String(6), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.user_id'), nullable=False)

