from app import app, db
from app.forms import LoginForm,RegisterForm
from app.models import User
from app.models import load_user
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
import json
from datetime import date, datetime

