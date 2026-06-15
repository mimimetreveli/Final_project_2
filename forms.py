from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(FlaskForm):
    name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField("Surname", validators=[DataRequired(), Length(min=2, max=50)])
    student_id = StringField("Personal ID (11 digits)", validators=[DataRequired(), Length(min=11, max=11)])
    grade = IntegerField("Grade/Class", validators=[DataRequired()])
    email = StringField("EMIS Student Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=24)])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password", message="Passwords must match!")
    ])
    register = SubmitField("Register Account")

    def validate_email(self, field):
        if not field.data.strip().lower().endswith("@students.gov.ge"):
            raise ValidationError("You must register using an official @students.gov.ge EMIS address.")

class LoginForm(FlaskForm):
    email = StringField("EMIS Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Log In")

class PostForm(FlaskForm):
    title = StringField("Post Title", validators=[DataRequired(), Length(max=100)])
    content = TextAreaField("What's on your mind?", validators=[DataRequired()])
    image = FileField("Optional Image Attachment", validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only .jpg, .jpeg, and .png images are allowed!')
    ])
    submit = SubmitField("Publish Post")