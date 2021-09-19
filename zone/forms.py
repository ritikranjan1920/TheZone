from datetime import date
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from zone.models import Student, Faculty, CRC, PlacedStudent, Result

year = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]
placement_choice = [('0', 'Select'), ('Not Placed', 'Not Placed'), ('Placed', 'Placed'), ('Not Interested', 'Not Interested')]


class StudentRegistrationForm(FlaskForm):
    s_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    s_email = StringField('Email', validators=[DataRequired(), Email()])
    s_roll_no = StringField('University Roll No.', validators=[DataRequired(), Length(min=10, max=12)])
    s_year = SelectField('Year', choices=year)
    s_branch = StringField('Branch', validators=[DataRequired(), Length(min=2, max=30)])
    s_clg_name = StringField('College Name', validators=[DataRequired(), Length(min=2, max=30)])
    s_mobile = StringField('Mobile No.', validators=[DataRequired(), Length(10)])
    s_password = PasswordField('Password', validators=[DataRequired()])
    s_confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('s_password', message='password must match')])
    s_submit = SubmitField('Sign Up')

    def validate_s_roll_no(self, roll_no):
        student = Student.query.filter_by(user_id=roll_no.data).first()
        if student:
            raise ValidationError('Account with this Roll_no is already created')

    def validate_s_email(self, email):
        student = Student.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('Account with this email is already created')

    def validate_s_mobile(self, mobile):
        student = Student.query.filter_by(mobile=mobile.data).first()
        if student:
            raise ValidationError('This mobile is already used')


class DepartmentRegistrationForm(FlaskForm):
    d_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    d_email = StringField('Email', validators=[DataRequired(), Email()])
    d_emp_id = StringField('Employee ID.', validators=[DataRequired(), Length(min=10, max=12)])
    d_clg_name = StringField('College Name', validators=[DataRequired(), Length(min=2, max=30)])
    d_branch = StringField('Branch', validators=[DataRequired(), Length(min=2, max=30)])
    d_mobile = StringField('Mobile No.', validators=[DataRequired(), Length(10)])
    d_password = PasswordField('Password', validators=[DataRequired()])
    d_confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('d_password', message='Password must match')])
    d_submit = SubmitField('Sign Up')

    def validate_d_emp_id(self, emp_id):
        faculty = Faculty.query.filter_by(user_id=emp_id.data).first()
        if faculty:
            raise ValidationError('Account with this Employee ID. is already created')

    def validate_d_email(self, email):
        faculty = Faculty.query.filter_by(email=email.data).first()
        if faculty:
            raise ValidationError('Account with this email is already created')

    def validate_d_mobile(self, mobile):
        faculty = Faculty.query.filter_by(email=mobile.data).first()
        if faculty:
            raise ValidationError('This mobile is already used')


class CRCRegistrationForm(FlaskForm):
    c_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    c_email = StringField('Email', validators=[DataRequired(), Email()])
    c_emp_id = StringField('Employee ID.', validators=[DataRequired(), Length(min=10, max=12)])
    c_clg_name = StringField('College Name', validators=[DataRequired(), Length(min=2, max=30)])
    c_mobile = StringField('Mobile No.', validators=[DataRequired(), Length(10)])
    c_password = PasswordField('Password', validators=[DataRequired()])
    c_confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('c_password', message='Password must match')])
    c_submit = SubmitField('Sign Up', )

    def validate_c_emp_id(self, emp_id):
        faculty = CRC.query.filter_by(user_id=emp_id.data).first()
        if faculty:
            raise ValidationError('Account with this Employee ID. is already created')

    def validate_c_email(self, email):
        faculty = CRC.query.filter_by(email=email.data).first()
        if faculty:
            raise ValidationError('Account with this email is already created')

    def validate_c_mobile(self, mobile):
        faculty = CRC.query.filter_by(email=mobile.data).first()
        if faculty:
            raise ValidationError('This mobile is already used')


class StudentLoginForm(FlaskForm):
    s_roll_no = StringField('University Roll No.', validators=[DataRequired(), Length(min=10, max=12)])
    s_password = PasswordField('Password', validators=[DataRequired()])
    s_remember = BooleanField('Remember Me')
    s_submit = SubmitField('Login')


class DepartmentLoginForm(FlaskForm):
    d_emp_id = StringField('Employee ID.', validators=[DataRequired(), Length(min=10, max=12)])
    d_password = PasswordField('Password', validators=[DataRequired()])
    d_remember = BooleanField('Remember Me')
    d_submit = SubmitField('Login')


class CRCLoginForm(FlaskForm):
    c_emp_id = StringField('Employee ID.', validators=[DataRequired(), Length(min=10, max=12)])
    c_password = PasswordField('Password', validators=[DataRequired()])
    c_remember = BooleanField('Remember Me')
    c_submit = SubmitField('Login')


class StudentUpdateForm(FlaskForm):
    s_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    s_year = SelectField('Year', choices=year)
    s_branch = StringField('Branch', validators=[DataRequired(), Length(min=2, max=30)])
    s_headline = StringField('Headline', validators=[DataRequired(), Length(min=2, max=30)])
    s_roll_no = StringField('University Roll No', validators=[DataRequired(), Length(min=10, max=12)])
    s_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    s_about = TextAreaField('About Me')
    placement = SelectField('Placement Info', choices=placement_choice)
    letter = FileField('Offer Letter', validators=[FileAllowed(['pdf'])])
    s_submit = SubmitField('Update')

    def validate_s_roll_no(self, roll_no):
        if roll_no.data != current_user.user_id:
            student = Student.query.filter_by(user_id=roll_no.data).first()
            if student:
                raise ValidationError('Account with this Roll_no is already created')


class PlacedStudentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    package = StringField('Package', validators=[DataRequired(), Length(1)])
    date_placed = DateField('Placement Date', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=30)])
    picture = FileField('Student Photo', validators=[FileAllowed(['jpg', 'png'])])
    roll_no = StringField('University Roll No', validators=[DataRequired(), Length(min=10, max=12)])
    noc = FileField('Offer Letter', validators=[FileAllowed(['pdf'])])
    submit = SubmitField('Save')

    def validate_s_roll_no(self, roll_no):
        placed_student = PlacedStudent.query.filter_by(user_id=roll_no.data).first()
        if placed_student:
            raise ValidationError('This student is already created!')


# class PlacedStudentUpdateForm(FlaskForm):
#     name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
#     package = StringField('Package', validators=[DataRequired(), Length(1)])
#     date_placed = DateField('Placement Date', validators=[DataRequired()])
#     company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=30)])
#     picture = FileField('Student Photo', validators=[FileAllowed(['jpg', 'png'])])
#     roll_no = StringField('University Roll No', validators=[DataRequired(), Length(min=10, max=12)])
#     submit = SubmitField('Save')
#
#     def validate_s_roll_no(self, roll_no):
#         if roll_no.data != current_user.user_id:
#             student = Student.query.filter_by(user_id=roll_no.data).first()
#             if student:
#                 raise ValidationError('Account with this Roll_no is already created')


class ProjectForm(FlaskForm):
    project_title = StringField('Project Title', validators=[DataRequired(), Length(min=2, max=100)])
    project_picture = FileField('Project Photo', validators=[FileAllowed(['jpg', 'png'])])
    date_finished = DateField('Finished')
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=500)])
    project_link = StringField('Paste a link to your project')
    p_submit = SubmitField('Save')


start_choices = [tuple((str(date.today().year-i), str(date.today().year-i))) for i in range(100)]

start_choices.insert(0, ('0', 'Year'))

end_choices = [tuple((str(date.today().year-i+10), str(date.today().year-i+10))) for i in range(100)]

end_choices.insert(0, ('0', 'Year'))

months = [('0', 'month'), ('Jan', 'January'), ('Feb', 'February'), ('Mar', 'March'), ('Apr', 'April'), ('May', 'May'),
          ('Jun', 'June'), ('Jul', 'July'), ('Aug', 'August'), ('Sep', 'September'), ('Oct', 'October'),
          ('Nov', 'November'), ('Dec', 'December')]


class EducationForm(FlaskForm):
    name = StringField('Institute Name', validators=[DataRequired(), Length(min=2, max=100)])
    degree = StringField('Degree/Class', validators=[DataRequired(), Length(min=2, max=50)])
    field = StringField('Specialization', validators=[Length(max=100)])
    start_year = SelectField('Start Year', choices=start_choices)
    end_year = SelectField('End Year(or expected)', choices=end_choices)
    submit = SubmitField('Save')


class CertificateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    organisation = StringField('Issuing organisation', validators=[DataRequired(), Length(min=2, max=50)])
    credential = StringField('Credential ID', validators=[Length(max=50)])
    credential_url = StringField('Credential URL', validators=[Length(max=100)])
    issue_month = SelectField('Issue Date', choices=months, validators=[DataRequired()])
    issue_year = SelectField('Issue Date', choices=start_choices, validators=[DataRequired()])
    expiration_month = SelectField('Expiration Date(If does not expire, leave empty)', choices=months)
    expiration_year = SelectField('Expiration Date(If does not expire, leave empty)', choices=end_choices)
    c_submit = SubmitField('Save')


class SkillForm(FlaskForm):
    name = StringField("Skill (To add multiple skills write them separating with comma ( ' , ' )", validators=[DataRequired()])
    sk_submit = SubmitField('Add')
    sk_remove = SubmitField('Remove')


class AnnouncementForm(FlaskForm):
    title = StringField("Announcement title", validators=[DataRequired(), Length(min=2, max=100)])
    date = DateField("Date", validators=[DataRequired()])
    pdf = FileField('Notice PDF', validators=[FileAllowed(['pdf']), DataRequired()])
    announce = SubmitField("Announce")


class ResultForm(FlaskForm):

    sems = []

    def semesters(self, student):
        self.sems.clear()
        results = Result.query.filter_by(student_id=student).all()

        semester = []
        for result in results:
            semester.append(result.sem)

        for i in range(1, 9):
            if str(i) not in semester:
                self.sems.append((str(i), str(i)))

    sem = SelectField('Semester', choices=sems)
    nob = StringField("No. of backlogs", validators=[DataRequired()])
    percent = StringField("Percentage(Upto 2 decimal)", validators=[DataRequired()])
    add = SubmitField("Add")

    def validate_percent(self, percent):
        percent = percent.data.strip()
        if 5 >= len(percent) >= 1:
            try:
                float(percent)
            except:
                raise ValidationError('Please enter valid value')
        else:
            raise ValidationError('Please enter valid value')







