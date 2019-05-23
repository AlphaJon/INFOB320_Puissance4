from app import app, db
from app.forms import LoginForm,RegisterForm
from app.models import User, GameHistory
from app.models import load_user
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
import json
from datetime import date, datetime

waiting_player = None

@app.route("/game/start")
def game_start():
	global waiting_player
	if current_user.current_game is not None:
		current_user.current_game.finished = True
	if waiting_player is None:
		waiting_player = current_user
	else:
		new_game = GameHistory(
			red_player=waiting_player.id,
			yellow_player=current_user.id
			)
		waiting_player.current_game = new_game
		current_user.current_game = new_game
		waiting_player = None
	return ""

@app.route("/game/play/<int:col>")
def game_play(col):
	game = current_user.current_game
	if (game is not None
		and not game.finished
		and ((current_user.id == game.red_player and game.current_turn == 1)
			or (current_user.id == game.yellow_player and game.current_turn == 0))
		and (game.game_grid[col][5] == -1)):
		verticalPos = 0
		while (game.game_grid[pos][verticalPos] != -1):
			verticalPos += 1
		game.game_grid[pos][verticalPos] = game.current_turn
		game.finished = check_win()
		game.current_turn = 1 - game.current_turn
		return jsonify(game.game_grid)
	return "[]"
		

@app.route("/game/ping")
def game_ping():
	game = current_user.current_game
	if game is not None :
		return jsonify(game.game_grid)

def check_win(game_array):
	win = false
	emptySpace = -1
	for i in xrange(0,7):
		for j in xrange(0,6):
			#Skip empty cells
			if (game_array[i][j] == emptySpace):
				continue

			#Horizontal
			if (i <= 3 
				and game_array[i+1][j] != emptySpace
				and game_array[i+2][j] != emptySpace
				and game_array[i+3][j] != emptySpace
				and ((game_array[i][j] ) == (game_array[i+1][j] ))
				and ((game_array[i][j] ) == (game_array[i+2][j] ))
				and ((game_array[i][j] ) == (game_array[i+3][j] ))) :
				win = true

			#Vertical
			if (j <= 2 
				and game_array[i][j+1] != emptySpace
				and game_array[i][j+2] != emptySpace
				and game_array[i][j+3] != emptySpace
				and ((game_array[i][j] ) == (game_array[i][j+1] ))
				and ((game_array[i][j] ) == (game_array[i][j+2] ))
				and ((game_array[i][j] ) == (game_array[i][j+3] ))) :
				win = true

			#Diagonal \
			if (i <= 3 and j <= 2
				and game_array[i+1][j+1] != emptySpace
				and game_array[i+2][j+2] != emptySpace
				and game_array[i+3][j+3] != emptySpace
				and ((game_array[i][j] ) == (game_array[i+1][j+1] ))
				and ((game_array[i][j] ) == (game_array[i+2][j+2] ))
				and ((game_array[i][j] ) == (game_array[i+3][j+3] ))) :
				win = true

			#Diagonal /
			if (i >= 3 and j <= 2
				and game_array[i-1][j+1] != emptySpace
				and game_array[i-2][j+2] != emptySpace
				and game_array[i-3][j+3] != emptySpace
				and ((game_array[i][j] ) == (game_array[i-1][j+1] ))
				and ((game_array[i][j] ) == (game_array[i-2][j+2] ))
				and ((game_array[i][j] ) == (game_array[i-3][j+3] ))) :
				win = true
	return win