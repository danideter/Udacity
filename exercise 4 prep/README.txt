Exercise 4 Prep - App Engine
Version 1.0
---------------------------------

This application is to test a data structure for udacity's project 4 in the 
fullstack nano-degree program. This is an alpha of the game, and input 
validations are not in place yet.

The zip folder contains the following folders and files.
-------------------------------------------

 1 - liarsDice.py
     This contains test functions for a liar's dice web app.

 2 - README.txt
     This is me. I am the README.txt file.

How to run the application
--------------------------
Python version 2.7.10 or later (but less than 3.x) must be installed on your 
machine.
The SQLAlchemy 1.0.13 module must also be available in your python environment.

1 - In the terminal/cmd change diectory to where the files are located.
2 - Open the python interpretor and import liarsDice
3 - Enjoy playing the game with friends and managing a liar's dice database!

The following methods are available: 
* startGame(password, players, dice_per_player, dice_sides, wild)
  start a game of liar's dice. 
  args:
	password: the password to access the game *does not do anything yet
	players: the number of players in the game. Must be greater than or equal to 
		1.
	dice_per_plaer: the number of dice per player. Typically 5 for a 3-4 player
		game.
	dice_sides: the number of sides (or faces) on a die. Typically 6
	wild: Which side of the dice is considered wild. If no wild wanted, enter 0.

* getGame(game_id)
	gives general info about a game such as what the bid is and who the last 
	bidder was.
	args:
		game_id: the id of the game to inspect. Given when the game is started with
			startGame()

* getDice(game_id, player_number)
	gets a player's dice in a particular game
	args:
		game_id: the id of the game to inspect. Given when the game is started with
			startGame()
	player_number: the turn order of the plater in the game

* raiseBid(game_id, die_face, die_total)
	raise the bid in a game. For this varient of liars dice, either the face value
	must increase with the total resetting to 1, or the face value can remain the
	same with the total increasing.
	args:
		game_id: the id of the game to inspect. Given when the game is started with
			startGame()
		die_face: the face on the die to raise the bid to.
		die_total: the number of dice to raise the bid to.

* callLiar(game_id)
	call the last player a liar. This ends the game.
	args:
		game_id: the id of the game to inspect. Given when the game is started with
			startGame()

* deleteGame(game_id)
	delete a game, never to see it again.
	args:
		game_id: the id of the game to inspect. Given when the game is started with
			startGame()


Copyright: 2016
Author: Danielle Detering
Date: 7/18/2016

Enjoy!
