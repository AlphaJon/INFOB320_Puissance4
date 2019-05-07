from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField
from wtforms.validators import InputRequired, Length, Email
from app.models import User, Task

class TodoLoginForm(FlaskForm):
	username = StringField('Username :', 
		validators=[InputRequired(), Length(min=3, max=16)])
	password = PasswordField('Password :', 
		validators=[InputRequired()])
	submit = SubmitField('Send')
	
class TodoRegisterForm(FlaskForm):
	username = StringField('Username :',
		validators=[InputRequired(), Length(min=3, max=16)])
	password = PasswordField('Password :',
		validators=[InputRequired()])
	email = StringField('E-mail :',
		validators=[Email()])
	firstname = StringField('First name :')
	lastname = StringField('Last name :')
	dob = DateField('Date of birth :')
	address = StringField('Address :')
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError("Username is already taken")

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email is not None:
			raise ValidationError("Email is already taken")

class TodoTaskForm(FlaskForm):
	'''def __init__(self):
		super(ClassName, self).__init__()'''
	name = StringField('Name :',
		validators=[InputRequired()])
	description = StringField('Description :')
	deadline = DateField('Deadline :')
	complete = BooleanField('Done')
	submit = SubmitField('Send')