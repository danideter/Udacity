Exercise 2 - Tournament Database
Version 1.0
---------------------------------

This application allows interactivity with a PostgreSQL tournament database
through python methods. Let the program take care of the sql for you as you
manage a swiss pairing tournament for games like PokemonTCG and Warhammer!
* Accelerated swiss pairings now supported!

The zip folder contains the following files.
-------------------------------------------

 1 - tournament.py
     This contains a list of methods in order to interact with a PostgreSQL 
     database to operate a tournament. Please open this file in an editor to
     see a list of methods and their arguments.

 2 - tournament.exe
     This is tournament.py compiled.

 3 - tournament_test.py
     This file tests tournament.py to make sure the functions are running
     correctly. It is useful in pinpointing errors if tournament.py is altered 
     and not running as expected. It is provided by Udacity.

 4 - tournament.sql
     This file creates the tournament database, player and matches tables 
     within the database, and their respective schemas. Before tournament.py
     can be used, this file must be imported by a PostgreSQL system.

 5 - README.txt
     This is me. I am the README.txt file.

How to run the application
--------------------------
Python version 2.7.10 or later must be installed on your machine. Python 
version 3 may be used, but is not guaranteed to work.

1 - In terminal/cmd, navigate to the directory where the files are located.
2 - Open psql and import tournament.sql
3 - Exit from psql 
4 - Open the python interpreter and import tournament
5 - Run the methods and enjoy supervising a tournament!

Copyright: 2015
Author: Danielle Detering
Date: 12/16/2015

Enjoy!