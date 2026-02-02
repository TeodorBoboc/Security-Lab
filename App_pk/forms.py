from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from App_pk.models import User

class RegistrationForm(FlaskForm):
    username=StringField('Username', 
                         validators=[DataRequired(message="Introduceti numele!"), Length(min=2,max=20,message="Introdu un nume intre 2 si 20 de caractere!")])
    email=StringField('Email', 
                         validators=[DataRequired(message="Introduceti E-mailul!"), Email(message="E-mailul nu este valid!")])
    password=PasswordField('Password',
                           validators=[DataRequired(message="Introduceti parola!")])
    confirm_password=PasswordField('Confirm_password',
                           validators=[DataRequired(message="Introduceti parola!"), EqualTo('password', message="Introdu aceeasi parola!")])
    submit=SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Numele este deja luat!')

    def validate_email(self,email):
        mail = User.query.filter_by(email=email.data).first()
        if mail:
            raise ValidationError('Acest email exista deja')


class LoginForm(FlaskForm):
    email=StringField('Email',
                               validators=[DataRequired(message="Introdu E-mailul!")])
    password=PasswordField('Password', 
                           validators=[DataRequired(message="Introduceti parola!")])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username=StringField('Username', 
                            validators=[DataRequired(message="Introduceti numele!"), Length(min=2,max=20,message="Introdu un nume intre 2 si 20 de caractere!")])
    email=StringField('Email', 
                            validators=[DataRequired(message="Introduceti E-mailul!"), Email(message="E-mailul nu este valid!")])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Update')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Numele este deja luat!')

    def validate_email(self,email):
        if email.data != current_user.email:
            mail = User.query.filter_by(email=email.data).first()
            if mail:
                raise ValidationError('Acest email exista deja')
    
class PostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(message="N-ai dat un titlu postarii"), Length(min=2, max=100,message="Introdu un titlu intre 2 si 100 de caractere!")])
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    picture = FileField('Adauga_o_imagine',
                        validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Post')
    
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset') 
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
                    raise ValidationError('Nu există un cont cu acest email. Trebuie să te înregistrezi mai întâi!')
        
class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',
                           validators=[DataRequired(message="Introduceti parola!")])
    confirm_password=PasswordField('Confirm_password',
                           validators=[DataRequired(message="Introduceti parola!"), EqualTo('password', message="Introdu aceeasi parola!")])
    submit = SubmitField('Reset Password')