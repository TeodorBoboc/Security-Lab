from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class RegistrationForm(FlaskForm):
    username=StringField('Username', 
                         validators=[DataRequired(message="Introduce-ti numele!"), Length(min=2,max=20,message="Introdu un nume intre 2 si 20 de caractere!")])
    email=StringField('Email', 
                         validators=[DataRequired(message="Introduce-ti E-mailul!"), Email(message="E-mailul nu este valid!")])
    password=PasswordField('Password',
                           validators=[DataRequired(message="Introduce-ti parola!")])
    confirm_password=PasswordField('Confirm_password',
                           validators=[DataRequired(message="Introduce-ti parola!"), EqualTo('password', message="Introdu acceasi parola!")])
    submit=SubmitField('Sign up')

class LoginForm(FlaskForm):
    email=StringField('Email',
                               validators=[DataRequired(message="Introdu numele sau E-mailul!")])
    password=PasswordField('Password', 
                           validators=[DataRequired(message="Introduce-ti parola!")])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')
