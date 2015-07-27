2015.06.14
Athor: Mikhail Rozhkov


This is a Project 3 - Item Catalog under the Udacity Nanodegree program "Full Stack Web Developer"


A. Configuration Instruction
---------------------------- 
App structure: 
|-project3					- app folder
	|-static/				- contains style files and templated
		|-css/				- Bootstrap3 CSS files
		|-fonts/			- font files
		|-js/				- JavaSctipt files
		|-blank_user.gif	- default avatar for anonymous user
		|-styles.css		- main CSS 
		|-top-banner.jpeg	
	|-templates/			- contains HTML templates 
	|-client_secret_fb.json	- app secret for Facebook OAuth2 authentification
	|-client_secret_gl.json	- app secret for Google+ OAuth2 authentification
	|-database_setup.py 	- defines database structure and data models
	|-finalproject.py 		- main .py file to run app
	|-lotsofprojects.py 	- contains data for initial populating database 
	|-pg_config.sh 			- configuration of Vagrant, installs required Flask modules 
	|-README.txt			- this file
	|-Vagrantfile			- file required to launch Vagrant

Requrements:
This App was developed with Flask framework. It used: 
	Python 2.7.8 | Anaconda 2.1.0 (64-bit) interpreter
	Flask 0.10.1
	Random 
	SQLAlchemy 1.0.2
	OAuth2client
	Httplib2
	JSON
	Requests


B. Installation Instructions 
----------------------------
How to run the program?
1. Add your Facebook and Google dev IDs and SECRETs into the files: 
	-> client_secrets_fb.json
	-> client_secrets_gl.json
2. Navigate to the Full-Stack-Foundations/Lesson-4/Final-Project directory inside the vagrant environment
3. run database_setup.py to create the database
4. run lotsofprojects.py to populate the database
5. run finalproject.py and navigate to localhost:8080 in your browser


C. Operating Instructions: API description
------------------------------------------
(1) To get JSON APIs to view Category information:
	Route: 	'/category/<category_id>/projects/JSON'
    Params:	category_id - integer number ID of this category in database
    Returns:List of projects names, abstacts and image

(2) To get JSON APIs to view Project information:
	Route: 	'/category/<category_id>/projects/<project_id>/JSON'
    Params: category_id - integer number ID of this category in database
	    	project_id - integer number ID of this project in database
    Returns:Project's name, abstact, image, website

(3) To get JSON APIs to view catalog categories:
	Route:	'/catalog/JSON'
    Params:	category_id - integer number ID of this category in database
    Returns:List of categories IDs, names and images


D. Copyright and licensing information
-----------------------------------
This code was developed based on Udacity code samples from lessons:
	"Full Stack Foundations"
	"Authentication & Authorization: OAuth"
Code samples are considered as "Educational Content" and follows the terms of the Creative Commons 
Attribution-NonCommercial-NoDerivs 3.0 License (http://creativecommons.org/licenses/by-nc-nd/3.0/ 
and successor locations for such license) (the "CC License")
For more info: https://www.udacity.com/legal/ 