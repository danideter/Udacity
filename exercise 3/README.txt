Exercise 3 - Catalog
Version 1.0
---------------------------------

This application uses Flask to run the web app Bad Movie Science locally.

The zip folder contains the following folders and files.
-------------------------------------------

 1 - catalog.py
     This contains the server side functions to setup and deploy the website.

 2 - catalog.sql
     Creates the schema and views of the database used to run the website
	 including movies, genres, science and user tables

 3 - catalog_workspace
     The folder hierachy of the project as created by notepad++

 4 - templates folder
     Holds index.html, the main html page for the website which loads the 
	 angular framework.
	 
 5 - static folder
	Holds the css, html, javascript, and resource folders that run the front-
	end	of the website.

 5 - README.txt
     This is me. I am the README.txt file.

How to run the application
--------------------------
Python version 2.7.10 or later must be installed on your machine.
The latest version of postgresql mus also be installed om your machine.

1 - Clone the git repository:
	$ git clone https://github.com/danideter/Udacity
1 - In terminal/cmd, navigate to the directory where Udacity/exercise3 is located.
2 - Open psql and import catalog.sql
3 - Exit from psql 
4 - Run the command: python catalog.py
5 - The website will run on localhost:8080 and the program will populate the
    database with example data if there isn't any.

Copyright: 2016
Author: Danielle Detering
Date: 6/28/2016

Enjoy!