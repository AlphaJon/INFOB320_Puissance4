from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField
from wtforms.validators import InputRequired, Length, Email
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username :', 
		validators=[InputRequired(), Length(min=3, max=16)])
	password = PasswordField('Password :', 
		validators=[InputRequired()])
	submit = SubmitField('Send')
	
class RegisterForm(FlaskForm):
	username = StringField('Username :',
		validators=[InputRequired(), Length(min=3, max=16)])
	password = PasswordField('Password :',
		validators=[InputRequired()])
	email = StringField('E-mail :',
		validators=[Email()])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError("Username is already taken")

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email is not None:
			raise ValidationError("Email is already taken")