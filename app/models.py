from flask_login import UserMixin
from app import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash
import json, datetime

#User array
logged_users = []

#Game array
ongoing_games = []

class User(UserMixin, db.Model):
	#def __init__(self, name):
	#	super(User, self).__init__()
	#	self.id = name
	#	self.name = name
	#	#self.group = "user"

	def __repr__(self):
		#return self.username
		return "User ID {id} ({username})".format(id=self.id, username=self.username)

	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(16), unique=True, nullable=False)
	email = db.Column(db.String(255), unique=True, nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	games_history = db.relationship("GameHistory", backref="towner", lazy="dynamic")
#	blocked = db.Column(db.Boolean)
	current_game = None

	@property
	def is_authenticated(self):
		return (self in logged_users) #self.logged logged_users

	def set_logged(self, state=True):
		if state and not (self in logged_users):
			logged_users.append(self)
		if not state and (self in logged_users):
			logged_users.remove(self)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def load_by_name(username):
		return User.query.filter_by(username = username).first()

	@property
	def group(self):
		return Group.load(self.ugroup)


@login_manager.user_loader
def load_user(userid):
	return User.query.get(int(userid))

#def load_all_users():
#	return User.query.all()

class GameHistory(db.Model):
	__tablename__ = "game_history"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	red_player = db.Column(db.Integer, db.ForeignKey("user.id"))
	yellow_player = db.Column(db.Integer, db.ForeignKey("user.id"))
	move_history = db.Column(db.String(6*7))
	game_grid = [
		[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,0,0,0,0,0]
	]
	
