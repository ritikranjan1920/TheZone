import os, datetime
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session, make_response
from zone.forms import StudentRegistrationForm, StudentLoginForm, DepartmentLoginForm, DepartmentRegistrationForm, CRCLoginForm, \
    CRCRegistrationForm, StudentUpdateForm, PlacedStudentForm, \
    ProjectForm, EducationForm, CertificateForm, SkillForm, AnnouncementForm, ResultForm
from zone.models import Student, PlacedStudent, Project, Faculty, Announcement, CRCAnnouncement, CRC, Education, Certificates, Result
from zone import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required


def which_user(user_id):
    if Student.query.filter_by(user_id=user_id).first():
        return 'student'
    elif Faculty.query.filter_by(user_id=user_id).first():
        return 'department'
    else:
        return 'crc'


def check(n):
    if n < 10:
        n = str(n)
        n = '0' + n
    n = str(n)
    return n


@app.route("/")
@app.route("/home")
def home():
    placed_students = PlacedStudent.query.order_by(PlacedStudent.id.desc())[:4]
    if current_user.is_authenticated:
        student = Student.query.filter_by(user_id=current_user.user_id).first()
    else:
        student = None
    info_data = db.session.query(Student.placement_info, db.func.count(Student.placement_info)).group_by(Student.placement_info).all()
    d = datetime.date.today().day
    y = datetime.date.today().year
    m = datetime.date.today().month
    num_data = []
    for i in range(1, d+1, 2):
        s = db.session.query(db.func.count(PlacedStudent.date_placed)).filter((PlacedStudent.date_placed <= str(y)+'-'+check(m)+'-'+check(i))).all()[0][0]
        num_data.append((check(i), s))
    packages = db.session.query(PlacedStudent.package).all()
    pack = [0, 0, 0, 0, 0]
    for package in packages:
        p = package[0].upper().split('L')[0]
        p = int(p)
        if p < 3:
            pack[0] = pack[0] + 1
        elif p < 5:
            pack[1] = pack[1] + 1
        elif p < 7:
            pack[2] = pack[2] + 1
        elif p < 10:
            pack[3] = pack[3] + 1
        else:
            pack[4] = pack[4] + 1
    return render_template('new_home.html', info_data=info_data, num_data=num_data, pack=pack, placed_students=placed_students, student=student)


@app.route("/demo")
def demo():
    return render_template('demo.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = StudentLoginForm()
    department_form = DepartmentLoginForm()
    crc_form = CRCLoginForm()
    if form.s_submit.data:
        if form.validate_on_submit():
            student = Student.query.filter_by(user_id=form.s_roll_no.data).first()
            if student and bcrypt.check_password_hash(student.password, form.s_password.data):
                login_user(student, remember=form.s_remember.data)
                next_page = request.args.get('next')
                session['user'] = 'student'
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check Roll_no and password', 'danger')
    elif department_form.d_submit.data:
        if department_form.validate_on_submit():
            faculty = Faculty.query.filter_by(user_id=department_form.d_emp_id.data).first()
            if faculty and bcrypt.check_password_hash(faculty.password, department_form.d_password.data):
                login_user(faculty, remember=department_form.d_remember.data)
                next_page = request.args.get('next')
                session['user'] = 'department'
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check Roll_no and password', 'danger')
    elif crc_form.c_submit.data:
        if crc_form.validate_on_submit():
            faculty = CRC.query.filter_by(user_id=crc_form.c_emp_id.data).first()
            if faculty and bcrypt.check_password_hash(faculty.password, crc_form.c_password.data):
                login_user(faculty, remember=crc_form.c_remember.data)
                next_page = request.args.get('next')
                session['user'] = 'crc'
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check Emp_ID and password', 'danger')
    return render_template('login.html', title='Register', form=form, department_form=department_form, crc_form=crc_form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = StudentRegistrationForm()
    department_form = DepartmentRegistrationForm()
    crc_form = CRCRegistrationForm()
    if form.s_submit.data:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.s_password.data).decode('utf-8')
            student = Student(name=form.s_name.data, email=form.s_email.data, user_id=form.s_roll_no.data,
                              year=form.s_year.data, mobile=form.s_mobile.data, password=hashed_password)
            db.session.add(student)
            db.session.commit()
            flash(f'Account created for {form.s_name.data}!', 'success')
            return redirect(url_for('login'))
    elif department_form.d_submit.data:
        if department_form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(department_form.d_password.data).decode('utf-8')
            faculty = Faculty(name=department_form.d_name.data, email=department_form.d_email.data,
                              user_id=department_form.d_emp_id.data, mobile=department_form.d_mobile.data,
                              password=hashed_password)
            db.session.add(faculty)
            db.session.commit()
            flash(f'Account created for {department_form.d_name.data}!', 'success')
            return redirect(url_for('login'))
    elif crc_form.c_submit.data:
        if crc_form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(crc_form.c_password.data).decode('utf-8')
            crc_faculty = CRC(name=crc_form.c_name.data, email=crc_form.c_email.data,
                              user_id=crc_form.c_emp_id.data, mobile=crc_form.c_mobile.data, password=hashed_password)
            db.session.add(crc_faculty)
            db.session.commit()
            flash(f'Account created for {crc_form.c_name.data}!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, department_form=department_form,
                           crc_form=crc_form)


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def save_picture(form_picture, name):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = name + ".jpg"
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i = crop_center(i, 200, 200)
    i.save(picture_path)

    return picture_fn


def save_project_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/project_images', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i = crop_center(i, 950, 600)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_pdf(pdf, name, t):
    _, f_ext = os.path.splitext(pdf.filename)
    fn = name + f_ext
    if t == 'letter':
        path = os.path.join(app.root_path, 'static/offer_letters', fn)
    else:
        path = os.path.join(app.root_path, 'static/noc', fn)

    pdf.save(path)

    return fn


@app.route("/student_account/<string:user_id>", methods=['GET', 'POST'])
@login_required
def student_account(user_id):
    student = Student.query.filter_by(user_id=user_id).first()
    student_classmates = Student.query.filter_by(branch=student.branch, year=student.year).all()
    projects = Project.query.filter_by(student_id=student.user_id).all()[:6]
    certificates = Certificates.query.filter_by(student_id=student.user_id).all()
    education = Education.query.filter_by(student_id=student.user_id).all()
    result = Result.query.filter_by(student_id=student.user_id).all()
    if student.skills is not None:
        skills = student.skills.split(',')
    else:
        skills = None
    if user_id == current_user.user_id:
        form = StudentUpdateForm()
        project_form = ProjectForm()
        education_form = EducationForm()
        certificate_form = CertificateForm()
        skill_form = SkillForm()
        ResultForm().semesters(student.user_id)
        result_form = ResultForm()
        form_validated = True
        if form.s_submit.data:
            form_validated = form.validate_on_submit()
            if form_validated:
                if form.s_picture.data:
                    picture_file = save_picture(form.s_picture.data, form.s_name.data)
                    student.image_file = picture_file
                if form.letter.data:
                    file = save_pdf(form.letter.data, student.name, 'letter')
                    student.letter = file
                student.year = form.s_year.data
                student.name = form.s_name.data
                student.branch = form.s_branch.data
                student.about = form.s_about.data
                student.headline = form.s_headline.data
                student.user_id = form.s_roll_no.data
                if form.placement.data != '0':
                    student.placement_info = form.placement.data
                db.session.commit()
                flash('Your account has been updated!', 'success')
                return redirect(url_for('student_account', user_id=student.user_id))
        elif project_form.p_submit.data:
            project_form_validated = project_form.validate_on_submit()
            if project_form_validated:
                picture_file = None
                if project_form.project_picture.data:
                    picture_file = save_project_picture(project_form.project_picture.data)
                project = Project(title=project_form.project_title.data, date_finished=project_form.date_finished.data,
                                  project_link=project_form.project_link.data, project_image=picture_file,
                                  description=project_form.description.data, student_id=student.user_id)
                db.session.add(project)
                db.session.commit()
                flash('Your project has been added!', 'success')
                return redirect(url_for('student_account', user_id=student.user_id))
        elif education_form.submit.data:
            print(222)
            if education_form.validate_on_submit():
                institute = Education(organisation_name=education_form.name.data, field=education_form.field.data,
                                      start_date=str(education_form.start_year.data), end_date=str(education_form.end_year.data),
                                      degree=education_form.degree.data, student_id=student.user_id)
                db.session.add(institute)
                db.session.commit()
                flash('Your education has been added!', 'success')
                return redirect(url_for('student_account', user_id=student.user_id))
        elif certificate_form.c_submit.data:
            print(1)
            if certificate_form.issue_year.data == '0' or certificate_form.issue_month.data == '0':
                certificate_form.issue_month.data = None
                certificate_form.issue_year.data = None
            if certificate_form.validate_on_submit():
                if certificate_form.expiration_year.data == '0' or certificate_form.expiration_month.data == '0':
                    date_expiry = None
                else:
                    date_expiry = str(certificate_form.expiration_month.data) + ', ' + str(certificate_form.expiration_year.data)
                if certificate_form.credential_url.data == '':
                    cred_url = None
                else:
                    cred_url = certificate_form.credential_url.data
                date_issued = str(certificate_form.issue_month.data)+', '+str(certificate_form.issue_year.data)
                certificate = Certificates(name=certificate_form.name.data, organisation_name=certificate_form.organisation.data,
                                           credential=certificate_form.credential.data, credential_url=cred_url,
                                           date_issued=date_issued, date_expiry=date_expiry, student_id=student.user_id)
                db.session.add(certificate)
                db.session.commit()
                flash('Your certificate has been added!', 'success')
                return redirect(url_for('student_account', user_id=student.user_id))
        elif skill_form.sk_submit.data:
            if skill_form.validate_on_submit():
                skill = skill_form.name.data.split(',')
                while '' in skill:
                    skill.remove('')
                skill = ','.join(skill)
                if student.skills:
                    student.skills = student.skills + ',' + skill
                else:
                    student.skills = skill
                print(skill)
                db.session.commit()
                flash('Your skills has been updated!', 'success')
                return redirect(url_for('student_account', user_id=student.user_id))
        elif skill_form.sk_remove.data:
            remove_skills = request.form.getlist('remove_skills')
            skill = student.skills.split(',')
            for i in remove_skills:
                skill.remove(i)
            if len(skill) != 0:
                student.skills = ','.join(skill)
            else:
                student.skills = None
            db.session.commit()
            flash('Your skills has been updated!', 'success')
            return redirect(url_for('student_account', user_id=student.user_id))
        elif result_form.add.data:
            if result_form.validate_on_submit():
                res = Result(sem=result_form.sem.data, nob=result_form.nob.data, percent=result_form.percent.data,
                             student_id=student.user_id)
                db.session.add(res)
                db.session.commit()
                flash('Your result has been updated!', 'success')
                return redirect(url_for('student_account', user_id=student.user_id))
        elif request.method == 'GET':
            form.s_year.data = student.year
            form.s_name.data = student.name
            form.s_branch.data = student.branch
            form.s_about.data = student.about
            form.s_headline.data = student.headline
            form.s_roll_no.data = student.user_id
        return render_template('account.html', form=form, project_form=project_form, certificate_form=certificate_form,
                               student=student, projects=projects, education=education, skill_form=skill_form,
                               certificates=certificates, skills=skills, validated=form_validated, education_form=education_form,
                               classmates=student_classmates, result_form=result_form, results=result,
                               edit_validated=True)
    else:
        return render_template('account.html', student=student, projects=projects, education=education,
                               certificates=certificates, skills=skills, classmates=student_classmates, results=result,
                               edit_validated=False)


@app.route("/edit/<int:project_id>", methods=['GET', 'POST'])
@login_required
def edit(project_id):
    form = ProjectForm()
    project = Project.query.get(project_id)
    form.project_link.data = project.project_link
    form.project_title.data = project.title
    form.date_finished.data = project.date_finished
    form.description.data = project.description
    picture_file = project.project_image
    if form.p_submit.data:
        print(1)
        form_validated = form.validate_on_submit()
        print(form_validated)
        if form_validated:
            if form.project_picture.data:
                picture_file = save_project_picture(form.project_picture.data)
            project = Project.query.get(project_id)
            print(project)
            project.title = form.project_title.data
            project.description = form.description.data
            project.project_link = form.project_link.data
            project.project_image = picture_file
            project.date_finished = form.date_finished.data
            db.session.commit()
            flash('Your project has been Updated successfully!', 'success')
            return redirect(url_for('student_account', user_id=current_user.user_id))
    return render_template('edit.html', project=project, project_update_form=form)


@app.route("/account/<string:user_id>", methods=['GET', 'POST'])
@login_required
def account(user_id):
    user = which_user(user_id=user_id)
    if user == 'student':
        return redirect(url_for('student_account', user_id=user_id))
    else:
        return redirect(url_for('home'))


@app.route("/placed_student_gallery", methods=['GET', 'POST'])
@login_required
def placed_student_gallery():
    page = request.args.get('page', 1, type=int)
    form = PlacedStudentForm()
    placed_students = PlacedStudent.query.paginate(page=page, per_page=16)
    if session['user'] == 'student':
        student = Student.query.filter_by(user_id=current_user.user_id).first()
    else:
        student = None
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = None
        if form.noc.data:
            file = save_pdf(form.noc.data, form.roll_no.data, 'noc')
        else:
            file = None
        student = PlacedStudent(student_id=form.roll_no.data, image_file=picture_file, package=form.package.data, company_name=form.company_name.data,
                                date_placed=form.date_placed.data, name=form.name.data, noc=file)
        db.session.add(student)
        db.session.commit()
        flash('Student Added', 'success')
        return redirect(url_for('placed_student_gallery'))
    return render_template('gallery.html', placed_students=placed_students, form=form, student=student)


@app.route("/students/<string:year>/<string:branch>")
@login_required
def students(year, branch):
    if session['user'] == 'student':
        student = Student.query.filter_by(user_id=current_user.user_id).first()
    else:
        student = None
    student_classmates = Student.query.filter_by(year=year, branch=branch).all()
    return render_template('classmates.html', classmates=student_classmates, student=student)


def save_notice(notice):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(notice.filename)
    fn = random_hex + f_ext
    path = os.path.join(app.root_path, 'static/notices', fn)
    notice.save(path)

    return fn


@app.route("/announcements/<string:by>", methods=['GET', 'POST'])
@login_required
def announcements(by):
    if session['user'] == 'student':
        student = Student.query.filter_by(user_id=current_user.user_id).first()
    else:
        student = None
    page = request.args.get('page', 1, type=int)
    form = AnnouncementForm()
    if by == 'CRC':
        announcement = CRCAnnouncement.query.paginate(page=page, per_page=16)
        if session['user'] == 'student':
            student.seen_crc = "True"
    else:
        announcement = Announcement.query.paginate(page=page, per_page=16)
        if session['user'] == 'student':
            student.seen_department = "True"
    db.session.commit()
    if session['user'] == 'student':
        by = 'not_allowed'
    if form.announce.data:
        if form.validate_on_submit():
            # file = request.files['inputFile']
            file = save_notice(form.pdf.data)
            all_students = Student.query.all()
            if session['user'] == 'crc':
                notice = CRCAnnouncement(title=form.title.data, date_issued=form.date.data, pdf=file)
                for stud in all_students:
                    stud.seen_crc = "False"
            elif session['user'] == 'department':
                notice = Announcement(title=form.title.data, date_issued=form.date.data, pdf=file)
                for stud in all_students:
                    stud.seen_department = "False"
            db.session.add(notice)
            db.session.commit()
            flash('Announcement Made', 'success')
            return redirect(url_for('announcements', by=by))
    return render_template('announcements.html', announcement=announcement, form=form, by=by.lower(), student=student)


@app.route("/delete/<int:item_id>")
@login_required
def delete(item_id):
    user = session['user']
    if user == 'department':
        notice = Announcement.query.get(item_id)
    elif user == 'crc':
        notice = CRCAnnouncement.query.get(item_id)
    else:
        return redirect(url_for('home'))
    db.session.delete(notice)
    db.session.commit()
    flash('Announcement deleted successfully!', 'success')
    return redirect(url_for('announcements', by=user.upper()))


@app.route("/project/delete/<int:user_id>/<int:item_id>")
@login_required
def project_delete(user_id, item_id):
    project = Project.query.get(item_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('student_account', user_id=user_id))


@app.route("/result/delete/<int:user_id>/<int:sem>")
@login_required
def result_delete(user_id, sem):
    if str(user_id) == str(current_user.user_id):
        result = Result.query.filter_by(student_id=user_id).filter_by(sem=sem).first()
        db.session.delete(result)
        db.session.commit()
        flash('Result has been updated successfully!', 'success')
        return redirect(url_for('student_account', user_id=user_id))
    else:
        return redirect(url_for("home"))


@app.route("/student/delete/<int:user_id>")
@login_required
def student_delete(user_id):
    if session['user'] == 'crc' or session['user'] == 'department':
        student = PlacedStudent.query.filter_by(student_id=user_id).first()
        db.session.delete(student)
        db.session.commit()
        flash('Student has been deleted successfully!', 'success')
        return redirect(url_for('placed_student_gallery'))
    else:
        return redirect(url_for("home"))


@app.route("/education/delete/<int:user_id>/<int:education_id>")
@login_required
def education_delete(user_id, education_id):
    if str(user_id) == str(current_user.user_id):
        education = Education.query.get(education_id)
        db.session.delete(education)
        db.session.commit()
        flash('Education has been deleted successfully!', 'success')
        return redirect(url_for('student_account', user_id=user_id))
    else:
        return redirect(url_for("home"))


@app.route("/certificate/delete/<int:user_id>/<int:certificate_id>")
@login_required
def certificate_delete(user_id, certificate_id):
    if str(user_id) == str(current_user.user_id):
        certificate = Certificates.query.get(certificate_id)
        db.session.delete(certificate)
        db.session.commit()
        flash('Certificate has been deleted successfully!', 'success')
        return redirect(url_for('student_account', user_id=user_id))
    else:
        return redirect(url_for("home"))


@app.route("/<string:user_id>/resume")
def resume(user_id):
    student = Student.query.filter_by(user_id=user_id).first()
    certificates = Certificates.query.filter_by(student_id=student.user_id).all()[:3]
    education = Education.query.filter_by(student_id=student.user_id).all()
    if student.skills is not None:
        skills = student.skills.split(',')[:10]
    else:
        skills = None
    return render_template('resume.html', student=student, certificates=certificates, education=education, skills=skills)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/new")
def new():
    return render_template('new_home.html')


@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")






