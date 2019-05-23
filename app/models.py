from flask_login import UserMixin
from app import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash
import json, datetime

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
	games_history_red = db.relationship("GameHistory", backref="redp", lazy="dynamic", foreign_keys = 'GameHistory.red_player')
	games_history_yellow = db.relationship("GameHistory", backref="yellowp", lazy="dynamic", foreign_keys = 'GameHistory.yellow_player')
	#blocked = db.Column(db.Boolean)
	current_game = None

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def load_by_name(username):
		return User.query.filter_by(username = username).first()


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
		[-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1],
		[-1,-1,-1,-1,-1,-1]
	]
	current_turn = 1
	finished = False
	winner = db.Column(db.Integer, nullable=True)