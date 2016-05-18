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
Python version 2.7.10 or later must be installed on your machine. Python 
version 3 may be used, but is not guaranteed to work.

1 - In terminal/cmd, navigate to the directory where the files are located.
2 - Open psql and import catalog.sql
3 - Exit from psql 
5 - Run the command: python catalog.py

Copyright: 2016
Author: Danielle Detering
Date: 5/17/2016

Enjoy!