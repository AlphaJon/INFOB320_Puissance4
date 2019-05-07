from flask_login import UserMixin
from app import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash
import json, datetime

#User array
logged_users = []

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
	#password = db.Column(db.String(255), nullable=False)
	#TODO: firstname, lastname, dob, address
	firstname = db.Column(db.String(255))
	lastname = db.Column(db.String(255))
	dob = db.Column(db.Date)
	address = db.Column(db.String(255))
	email = db.Column(db.String(255), unique=True, nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	tasks = db.relationship("Task", backref="towner", lazy="dynamic")
	taskgroups = db.relationship("TaskGroup", backref="tgowner", lazy="dynamic")
	ugroup = db.Column(db.Integer, db.ForeignKey("ugroup.id"))
	blocked = db.Column(db.Boolean)

	@property
	def is_active(self):
		return True
		#return self.dt >= datetime.datetime.now() - datetime.timedelta(minutes=5)

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
	#def set_active(self):
	#	self.dt = datetime.datetime.now().replace(microsecond=0)
	def is_admin(self):
		return self.group.admin_permissions

	@property
	def group(self):
		return Group.load(self.ugroup)


@login_manager.user_loader
def load_user(userid):
	return User.query.get(int(userid))

def load_all_users():
	return User.query.all()

class Group(db.Model):
	def __repr__(self):
		return "Group {id} : {name} (admin = {admin})".format(
			id=self.id,
			name=self.name,
			admin=self.admin_permissions
			)

	__tablename__ = "ugroup"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), nullable=False)
	admin_permissions = db.Column(db.Boolean, nullable=False, server_default="0")

	def load(id):
		return Group.query.get(id)

	def load_by_name(name):
		return Group.query.filter_by(name = name).first()

class Task(db.Model):

	def __repr__(self):
		return "Task ID {id} ({name}), owner ID {user}".format(
			id=self.id, 
			name=self.name, 
			user=self.owner)
		
	__tablename__ = "task"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), nullable=False)
	description = db.Column(db.String(255))
	deadline = db.Column(db.Date)
	complete = db.Column(db.Boolean)
	owner = db.Column(db.Integer, db.ForeignKey("user.id"))
	tgroupid = db.Column(db.Integer, db.ForeignKey("task_group.id"))

	def load(id):
		return Task.query.get(id)

	def obj(self):
		return {
			"id": self.id,
			"name": self.name,
			"description": self.description,
			"deadline": self.deadline.isoformat(),
			"complete": self.complete
		}

	def toJSON(self):
		return json.dumps(self.obj())

class TaskGroup(db.Model):
	def __repr__(self):
		return "Task group ID {id} ({name})".format(
			id=self.id,
			name=self.name)

	__tablename__ = "task_group"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), nullable=False)
	ownerid = db.Column(db.Integer, db.ForeignKey("user.id"))
	tasks = db.relationship("Task", cascade="all,delete", backref="tgroup", lazy="dynamic")

	def obj(self, fetch_tasks=False):
		tmpobj = {
			"id": self.id,
			"name": self.name
		}
		if fetch_tasks:
			tmpobj["tasks"] = [task.obj() for task in self.tasks]
		return tmpobj

	def toJSON(self, fetch_tasks=False):
		return json.dumps(self.obj(fetch_tasks))