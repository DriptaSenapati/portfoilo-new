from flask import Flask, render_template, send_from_directory, redirect, url_for, request, flash, Blueprint, jsonify, current_app
from portfolio.forms import LoginForm, Testimoni_form, SkillForm, ProjectForm, JobForm, changepictureForm
import os
from PIL import Image
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from portfolio import db
from portfolio.models import Testimonial, User, Job, Project, Skills
import uuid


main = Blueprint('main', __name__, static_folder='static',
                 static_url_path='/static/')


@main.route('/')
def home():
    testimoni = Testimonial.query.all()
    sk_data = Skills.query.all()
    project = Project.query.all()
    job = Job.query.all()
    job.reverse()
    exp_list = []
    for j in job:
        if j.end:
            start = j.start
            end = j.end
            diff = end-start
            exp_year = divmod(diff.days, 365)
            exp_month = divmod(exp_year[1], 30)
            exp_string = f'{exp_year[0]} year {exp_month[0]} month {exp_month[1]} days'
            exp_list.append(exp_string)
        elif not j.end:
            start = j.start
            end = datetime.now()
            diff = end-start
            exp_year = divmod(diff.days, 365)
            exp_month = divmod(exp_year[1], 30)
            exp_string = f'{exp_year[0]} year {exp_month[0]} month {exp_month[1]} days'
            exp_list.append(exp_string)
    return render_template('main.html', testimoni_data=testimoni, skills=sk_data, projects=project, jobs=job, exp=exp_list)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.data'))
    login = LoginForm()
    # print(login.hidden_tag())
    if login.validate_on_submit():
        user_data = User.query.filter_by(email=login.email.data).first()
        if user_data and user_data.password == login.password.data:
            login_user(user_data)
            return redirect(url_for('main.data'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    # print(login.errors)
    return render_template('login.html', form=login)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/formdata', methods=['GET', 'POST'])
@login_required
def data():
    testimonial_data = Testimonial.query.all()
    skill_data = Skills.query.all()
    project_data = Project.query.all()
    jobdata = Job.query.all()

    return render_template('admin.html', testimoni=testimonial_data, skills=skill_data, projects=project_data, jobs=jobdata)


def save_picture(form_picture):
    # random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    # picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        main.root_path, 'static/img', form_picture.filename)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return form_picture.filename


@main.route('/formdata/<path:form_type>/<int:data_id>', methods=['GET', 'POST'])
@login_required
def edit_post(data_id, form_type):
    if form_type == 'testimoni':
        testimoni_data = Testimonial.query.filter_by(id=data_id).first()
        test_form = Testimoni_form(id=data_id)
        pic_form = changepictureForm(id=data_id)
        if test_form.submit.data and test_form.validate_on_submit():
            testimoni_data.name = test_form.name.data
            testimoni_data.desc = test_form.desc.data
            testimoni_data.testimony = test_form.main.data
            db.session.commit()
            return redirect(url_for('main.data'))
        elif request.method == 'GET':
            test_form.name.data = testimoni_data.name
            test_form.desc.data = testimoni_data.desc
            test_form.main.data = testimoni_data.testimony
            return render_template('edit_data.html', form=test_form, type=form_type, pic=True, image=testimoni_data, form_pic=pic_form)
        return render_template('edit_data.html', form=test_form, type=form_type, pic=True, image=testimoni_data, form_pic=pic_form)
    elif form_type == 'skill':
        skilldata = Skills.query.filter_by(id=data_id).first()
        skill_add_form = SkillForm(id=data_id)
        if skill_add_form.validate_on_submit():
            skilldata.sk_name = skill_add_form.skillsname.data
            skilldata.sk_value = skill_add_form.skills.data
            skilldata.sk_type = skill_add_form.skill_type.data
            db.session.commit()
            return redirect(url_for('main.data'))
        elif request.method == 'GET':
            skill_add_form.skillsname.data = skilldata.sk_name
            skill_add_form.skills.data = skilldata.sk_value
            skill_add_form.skill_type.data = skilldata.sk_type
            return render_template('edit_data.html', form=skill_add_form, type='testimoni', image=None)
        return render_template('edit_data.html', form=skill_add_form, type='testimoni', image=None)

    elif form_type == 'project':
        projectdata = Project.query.filter_by(id=data_id).first()
        projectform = ProjectForm(id=data_id)
        if projectform.validate_on_submit():
            for filled_data in projectform:
                if filled_data.data == '':
                    filled_data.data = None
            projectdata.p_name = projectform.title.data
            projectdata.p_description = projectform.Description.data
            projectdata.Organization = projectform.Organization.data
            projectdata.p_url = projectform.URL.data
            projectdata.cred_id = projectform.Credential.data
            projectdata.certi_url = projectform.Certificate.data
            projectdata.proj_type = projectform.proj_type.data
            db.session.commit()
            return redirect(url_for('main.data'))
        elif request.method == 'GET':
            projectform.title.data = projectdata.p_name
            projectform.Description.data = projectdata.p_description
            projectform.Organization.data = projectdata.Organization
            projectform.URL.data = projectdata.p_url
            projectform.Credential.data = projectdata.cred_id
            projectform.Certificate.data = projectdata.certi_url
            projectform.proj_type.data = projectdata.proj_type
            return render_template('edit_data.html', form=projectform, type='testimoni')
        return render_template('edit_data.html', form=projectform, type='testimoni')
    elif form_type == 'job':
        jobdata = Job.query.filter_by(id=data_id).first()
        jobform = JobForm(id=data_id)
        if jobform.validate_on_submit():
            jobdata.role = jobform.role.data
            jobdata.company = jobform.company.data
            jobdata.start = datetime.strptime(
                jobform.start.data.strftime("%d %B %Y"), "%d %B %Y")
            if jobform.end.data == None:
                jobform.end.data = None
            else:
                jobform.end.data = datetime.strptime(
                    jobform.end.data.strftime("%d %B %Y"), "%d %B %Y")
            jobdata.end = jobform.end.data
            jobdata.place = jobform.place.data
            jobdata.jd = jobform.jd.data
            db.session.commit()
            return redirect(url_for('main.data'))
        elif request.method == 'GET':
            jobform.role.data = jobdata.role
            jobform.company.data = jobdata.company
            jobform.start.data = jobdata.start
            if jobdata.end == None:
                jobform.current.data = True
            else:
                jobform.end.data = jobdata.end
            jobform.place.data = jobdata.place
            jobform.jd.data = jobdata.jd
            return render_template('edit_data.html', form=jobform, type=form_type)
        return render_template('edit_data.html', form=jobform, type=form_type)


@main.route('/update/<int:data_id>', methods=['POST'])
def update_pic(data_id):
    testimoni_data = Testimonial.query.filter_by(id=data_id).first()
    pic_form = changepictureForm(id=data_id)
    if pic_form.picture.data:
        pic_file = save_picture(pic_form.picture.data)
        testimoni_data.image_file = pic_file
    else:
        testimoni_data.image_file = 'recom.jpg'
    db.session.commit()
    print(testimoni_data.image_file)
    return redirect(url_for('main.edit_post', data_id=data_id, form_type='testimoni'))


@main.route('/formdata/<path:form_type>/<int:data_id>/del_post', methods=['GET', 'POST'])
@login_required
def delete_post(data_id, form_type):
    if form_type == 'testimoni':
        Testimonial.query.filter_by(id=data_id).delete()
        db.session.commit()
    elif form_type == 'skill':
        Skills.query.filter_by(id=data_id).delete()
        db.session.commit()
    elif form_type == 'project':
        Project.query.filter_by(id=data_id).delete()
        db.session.commit()
    elif form_type == 'job':
        Job.query.filter_by(id=data_id).delete()
        db.session.commit()
    return redirect(url_for('main.data'))


@main.route('/formdata/<path:form_type>/add_entry', methods=['GET', 'POST'])
@login_required
def add_entry(form_type):
    if form_type == 'testimoni':
        test_form = Testimoni_form()
        if test_form.validate_on_submit():
            if test_form.picture.data:
                pic_file = save_picture(test_form.picture.data)
                new_data = Testimonial(
                    name=test_form.name.data, desc=test_form.desc.data, testimony=test_form.main.data, image_file=pic_file, author=current_user)
            else:
                new_data = Testimonial(
                    name=test_form.name.data, desc=test_form.desc.data, testimony=test_form.main.data, author=current_user)
            db.session.add(new_data)
            db.session.commit()
            return redirect(url_for('main.data'))
        return render_template('new_data_test.html', form=test_form, type=form_type, pic=True, title='New Testimoni Data')
    if form_type == 'skill':
        skill_add_form = SkillForm()
        if skill_add_form.validate_on_submit():
            print(skill_add_form.skill_type.data)
            skilldata = Skills(sk_name=skill_add_form.skillsname.data,
                               sk_value=skill_add_form.skills.data, sk_type=skill_add_form.skill_type.data,
                               author=current_user)
            db.session.add(skilldata)
            db.session.commit()
            return redirect(url_for('main.data'))
        return render_template('new_data_test.html', form=skill_add_form, type='testimoni', title='New Skill Data')
    if form_type == 'project':
        projectform = ProjectForm()
        if projectform.validate_on_submit():
            for filled_data in projectform:
                if filled_data.data == '':
                    filled_data.data = None
            project_data = Project(p_name=projectform.title.data, p_description=projectform.Description.data,
                                   Organization=projectform.Organization.data, p_url=projectform.URL.data,
                                   cred_id=projectform.Credential.data, certi_url=projectform.Certificate.data,
                                   proj_type=projectform.proj_type.data, author=current_user)
            db.session.add(project_data)
            db.session.commit()
            return redirect(url_for('main.data'))
        return render_template('new_data_test.html', form=projectform, type='testimoni', title='New Project Data')
    if form_type == 'job':
        jobform = JobForm()
        if jobform.validate_on_submit():
            if jobform.end.data == None:
                jobform.end.data = None
            else:
                jobform.end.data = datetime.strptime(
                    jobform.end.data.strftime("%B %Y"), "%B %Y")
            newjob = Job(role=jobform.role.data, company=jobform.company.data, start=datetime.strptime(jobform.start.data.strftime("%B %Y"), "%B %Y"),
                         end=jobform.end.data, place=jobform.place.data, jd=jobform.jd.data, author=current_user)
            db.session.add(newjob)
            db.session.commit()
            return redirect(url_for('main.data'))
        return render_template('new_data_test.html', form=jobform, type=form_type, title='New Job Data')


@main.route('/download_resume', methods=['GET'])
def getpdf():
    # print(main.static_folder)
    return send_from_directory(f'{main.static_folder}', "Dripta_Resume.pdf")


@main.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    path = os.path.join("static", 'download')
    return send_from_directory(path, filename)


@main.route('/upload_resume', methods=['POST'])
def upload():
    file = request.files['file']
    # name = file.filename
    # current_app.config["resume_name_hex"] = f"{name.split('.')[0]}{uuid.uuid1().hex}.pdf"
    save_path = os.path.join(main.static_folder, "Dripta_Resume.pdf")
    file.save(save_path)
    return jsonify({"massage": "all ok"})
