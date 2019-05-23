from app import app, db
from app.forms import LoginForm,RegisterForm
from app.models import User
from app.models import load_user
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
import json, datetime

@app.route("/install")
def install():
	db.drop_all()
	db.create_all()

	user_account = User(
		username = "user1",
		email = "u1@a.com",
	)
	user_account.set_password("user1")

	user_account2 = User(
		username = "user2",
		email = "u2@a.com",
	)
	user_account2.set_password("user2")

	db.session.add(user_account)
	db.session.add(user_account2)

	db.session.commit()
	return redirect(url_for("root"))

@app.route("/")
#@login_required
def root():
	return render_template("index.html") 

@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("root"))
	form = LoginForm()
	if form.validate_on_submit():
		#on error: flash("error", "danger")
		name = form.username.data
		user = User.load_by_name(name)
		print(user)
		if (user is not None 
			and user.check_password(form.password.data)):

			login_user(user)
			next_page = request.args.get("next")
			#if next_page and url_parse(next_page).netloc == "":
			#	return redirect(next_page)
			return redirect(url_for("root"))
		else:
			flash("Invalid credentials", "warning")
			return redirect(url_for("login"))
	else:
		return render_template("login_form.html", form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("root"))

@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("root"))
	form = RegisterForm()
	if form.validate_on_submit():
		name = form.username.data
		if User.load_by_name(name) is not None:
			flash("Username is already taken", "warning")
			return redirect(url_for("register"))
		#populate user data
		user = User(
			username = name,
			email = form.email.data,
			)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for("root"))
	else:
		return render_template("register_form.html", form=form)
