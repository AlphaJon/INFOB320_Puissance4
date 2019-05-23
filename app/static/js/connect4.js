var playerClasses = ["pred", "pyellow", "pred winning", "pyellow winning"];
var winFlag = 2; //0/2 -> 2 for red, 1/3 -> 3 for yellow
var localPlayerColor = null; //0 = red, 1 = yellow
var emptySpace = 4; //as to not interfere with the last 2 bits
var currentGame = null;

Connect4 = function(){
	this.gameState = [
		[4,4,4,4,4,4],
		[4,4,4,4,4,4],
		[4,4,4,4,4,4],
		[4,4,4,4,4,4],
		[4,4,4,4,4,4],
		[4,4,4,4,4,4],
		[4,4,4,4,4,4]
	];
	this.currentPlayer = 0;
	this.finished = false;
}

Connect4.prototype.play = function(position) {
	if (this.finished) {
		alert("The game has ended");
		return;
	}
	/*if (this.currentPlayer != localPlayerColor) {
		alert("This is not your turn yet");
		return;
	}*/
	if (this.gameState[position][5] != emptySpace) {
		alert("This column is full");
		return;
	}
	
	console.log(this.gameState);
	this.place(position);
};

Connect4.prototype.place = function(position) {
	var verticalPos = 0;
	while (this.gameState[position][verticalPos] != emptySpace){
		verticalPos++;
	}
	this.gameState[position][verticalPos] = this.currentPlayer;
	this.checkWin();
	this.currentPlayer = 1 - this.currentPlayer; //0->1, 1->0
	renderGameHtml(this.gameState);
}

Connect4.prototype.checkWin = function() {
	var grid = this.gameState;
	var win = false;
	for (var i = 0; i < 7; i++) {
		for (var j = 0; j < 6; j++) {
			//Skip empty cells
			if (grid[i][j] == emptySpace) {
				continue;
			}
			//Note: the & 0x1 everywhere serve to fetch only the last bit
			//(that's where the cell color is stored)
			//The method used below is somewhat inneficient, but we can find 
			//simultaneous lines and lines with more than 4 elements this way

			//Horizontal
			if (i <= 3 
				&& grid[i+1][j] != emptySpace
				&& grid[i+2][j] != emptySpace
				&& grid[i+3][j] != emptySpace
				&& ((grid[i][j] & 0x1) == (grid[i+1][j] & 0x1))
				&& ((grid[i][j] & 0x1) == (grid[i+2][j] & 0x1))
				&& ((grid[i][j] & 0x1) == (grid[i+3][j] & 0x1))) {
				grid[i+0][j] |= winFlag;
				grid[i+1][j] |= winFlag;
				grid[i+2][j] |= winFlag;
				grid[i+3][j] |= winFlag;
				win = true;
			}

			//Vertical
			if (j <= 2 
				&& grid[i][j+1] != emptySpace
				&& grid[i][j+2] != emptySpace
				&& grid[i][j+3] != emptySpace
				&& ((grid[i][j] & 0x1) == (grid[i][j+1] & 0x1))
				&& ((grid[i][j] & 0x1) == (grid[i][j+2] & 0x1))
				&& ((grid[i][j] & 0x1) == (grid[i][j+3] & 0x1))) {
				grid[i][j+0] |= winFlag;
				grid[i][j+1] |= winFlag;
				grid[i][j+2] |= winFlag;
				grid[i][j+3] |= winFlag;
				win = true;
			}

			//Diagonal \
			if (i <= 3 && j <= 2
				&& grid[i+1][j+1] != emptySpace
				&& grid[i+2][j+2] != emptySpace
				&& grid[i+3][j+3] != emptySpace
				&& ((grid[i][j] & 0x1) == (grid[i+1][j+1] & 0x1))
				&& ((grid[i][j] & 0x1) == (grid[i+2][j+2] & 0x1))
				&& ((grid[i][j] & 0x1) == (grid[i+3][j+3] & 0x1))) {
				grid[i+0][j+0] |= winFlag;
				grid[i+1][j+1] |= winFlag;
				grid[i+2][j+2] |= winFlag;
				grid[i+3][j+3] |= winFlag;
				win = true;
			}

			//Diagonal /
			if (i >= 3 && j <= 2
				&& grid[i-1][j+1] != emptySpace
				&& grid[i-2][j+2] != emptySpace
				&& grid[i-3][j+3] != emptySpace
				&& ((grid[i][j] & 0x1) == (grid[i-1][j+1] & 0x1))
				&& ((grid[i][j] & 0x1) == (grid[i-2][j+2] & 0x1))
				&& ((grid[i][j] & 0x1) == (grid[i-3][j+3] & 0x1))) {
				grid[i-0][j+0] |= winFlag;
				grid[i-1][j+1] |= winFlag;
				grid[i-2][j+2] |= winFlag;
				grid[i-3][j+3] |= winFlag;
				win = true;
			}
		}
	}
	if (win) {
		this.finished = true;
		alert("Game finished!");
	}
};

function renderGameHtml(grid){
	$("td.c4-cell").each(function(){
		var cellCol = $(this).attr("x-col");
		var cellRow = $(this.parentElement).attr("x-row");
		var classesToApply = playerClasses[grid[cellCol][cellRow]];
		$(this).removeClass("pred pyellow winning");
		$(this).addClass(classesToApply);
		//console.log("("+cellCol+","+cellRow+")");
	});
	//var strings = ["your turn", "the other player's turn"]
}

$("#group-add-btn").click(function(){
	var groupName = $("#group-add-input").val();
	$.ajax({
		url: "/api/taskgroups",
		method: "POST",
		data: {
			name: groupName
		},
		success: function(result){
			location.reload();
		}
	});
});

$("#main-game").click(function(ev){
	//custom attributes are prefixed with x-
	//(not required but preferred)
	var taskId = $(this).attr("x-task");
	//because we can't access this inside the ajax function
	var self = ev.target; 
	//Check if the clicked thing is the button
	//ev.target goes for the innermost tag
	if ($(self).hasClass("c4-cell")) {
		var cellCol = $(self).attr("x-col");
		currentGame.play(cellCol);
		ev.preventDefault();
		//console.log(this);
		return false;
	}
	
});

$(".game-new").click(function(){
	if ((currentGame.finished) || confirm("You will forfeit your current game if you continue. Proceed?")) {
		currentGame = new Connect4();
		renderGameHtml(currentGame.gameState);
	}
	
});

localPlayerColor = 0;
currentGame = new Connect4();