from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, TextAreaField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from portfolio.models import User, Project, Job, Skills, Testimonial
from flask_login import current_user


class LoginForm(FlaskForm):
    # email = FieldList(StringField('Email', validators=[
    #                   DataRequired(), Email()]), min_entries=2, max_entries=10)
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class Testimoni_form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    main = TextAreaField('Recommendation Data', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')

    def __init__(self, id=None, *args, **kwargs):
        self.id = id
        super(Testimoni_form, self).__init__(*args, **kwargs)

    def validate_name(self, name):
        if self.id:
            past_name = Testimonial.query.filter_by(id=self.id).first()
            if name.data != past_name.name:
                data = Testimonial.query.filter_by(name=name.data).first()
                if data:
                    raise ValidationError('This name already exists.')
        elif not self.id:
            data = Testimonial.query.filter_by(name=name.data).first()
            if data:
                raise ValidationError('This name already exists.')


class changepictureForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png'])])
    submit_pic = SubmitField('Save Changes')

    def __init__(self, id=None, *args, **kwargs):
        self.id = id
        super(changepictureForm, self).__init__(*args, **kwargs)


class SkillForm(FlaskForm):
    skillsname = StringField('Name', validators=[DataRequired()])
    skills = IntegerField('Value', validators=[DataRequired()])
    skill_type = RadioField('Select Type', choices=[
                            ('Web Design', 'Web Design'), ('Analytics', 'Analytics')], validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, id=None, *args, **kwargs):
        self.id = id
        super(SkillForm, self).__init__(*args, **kwargs)

    def validate_skills(self, skills):
        if skills.data >= 100:
            raise ValidationError('Skill value must be less than 100')

    def validate_skillsname(self, skillsname):
        if self.id:
            name = Skills.query.filter_by(id=self.id).first()
            if skillsname.data != name.sk_name:
                data = Skills.query.filter_by(sk_name=skillsname.data).first()
                if data:
                    raise ValidationError('Skill name already exists')
        elif not self.id:
            data = Skills.query.filter_by(sk_name=skillsname.data).first()
            if data:
                raise ValidationError('Skill name already exists')


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    Description = TextAreaField('Description')
    URL = StringField('Project URL')
    Organization = StringField('Organization (if any)')
    Credential = StringField('Credential id')
    Certificate = StringField('Certificate Url')
    proj_type = RadioField('Select Type', choices=[
        ('Certificate', 'Certificate'), ('Project', 'Project')], validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, id=None, *args, **kwargs):
        self.id = id
        super(ProjectForm, self).__init__(*args, **kwargs)

    def validate_title(self, title):
        if self.id:
            past_data = Project.query.filter_by(id=self.id).first()
            if past_data.p_name != title.data:
                data = Project.query.filter_by(p_name=title.data).first()
                if data:
                    raise ValidationError('Project name already exists')
        elif not self.id:
            data = Project.query.filter_by(p_name=title.data).first()
            if data:
                raise ValidationError('Project name already exists')

    def validate_Description(self, Description):
        if self.id:
            past_data = Project.query.filter_by(id=self.id).first()
            if past_data.p_description != Description.data:
                data = Project.query.filter_by(
                    p_description=Description.data).first()
                if data:
                    raise ValidationError('Project description already exists')
        elif not self.id:
            data = Project.query.filter_by(
                p_description=Description.data).first()
            if data:
                raise ValidationError('Project description already exists')


class JobForm(FlaskForm):
    role = StringField('Job Role', validators=[DataRequired()])
    company = StringField('Company Name', validators=[DataRequired()])
    current = BooleanField('This is my Current Job')
    start = DateField('Start Date', validators=[
                      DataRequired()], format=f'%Y-%m-%d')
    end = DateField('End Date', format=f'%Y-%m-%d')
    place = StringField('Location')
    jd = TextAreaField('Job Description', validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, id=None, *args, **kwargs):
        self.id = id
        super(JobForm, self).__init__(*args, **kwargs)

    def validate_company(self, company):
        if self.id:
            past_company = Job.query.filter_by(id=self.id).first()
            if company.data != past_company.company:
                data = Job.query.filter_by(company=company.data).first()
                if data:
                    raise ValidationError('Company name already exists')
        elif not self.id:
            data = Job.query.filter_by(company=company.data).first()
            if data:
                raise ValidationError('Company name already exists')

    def validate_end(self, end):
        if end.data:
            if end.data < self.start.data:
                raise ValidationError(
                    'End date nust be greater than start date')
        else:
            if self.current.data == False:
                raise ValidationError('Please check current job option')

    def validate_start(self, start):
        jobs = current_user.job
        for j in jobs:
            if j.id != self.id:
                if j.end:
                    if j.start.date() <= start.data <= j.end.date():
                        raise ValidationError(
                            f'Start date is overlapping with {j.company} duration')

    def validate_current(self, current):
        jobs = current_user.job
        for j in jobs:
            if j.id != self.id:
                if (j.end == None) & (current.data == True):
                    raise ValidationError(
                        f'Current job is already present for {j.company}')
