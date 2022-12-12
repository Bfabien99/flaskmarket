from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from wtforms.validators import Email


class RegisterForm(FlaskForm):

    username = StringField(label='Username', validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email', validators=[
                                Email(), DataRequired()])
    password1 = PasswordField(label="Password", validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[
                              EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')
