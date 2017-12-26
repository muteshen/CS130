# cs130-cinder

Cinder is a dating app where you can swipe left or right to match with other people, schedule a date with your matches, and provide/receive feedback from your matches after the scheduled date time has passed. Class project for CS130, Software Engineering.

HTML files found in ~/cinder/public
CSS found in ~/cinder/src/css, particularly style.css

First Time Setup
-------------------
In the outermost folder, make sure you have python 2.7 installed and pip
Maybe, use a virtual environment

`pip install -r requirements.txt`

Running Server
------------------
In the outmost folder run the command:

`python manage.py runserver -d`

The -d makes it restart the server on any file save so you don't have to

To select port:
  `python manage.py runserver -d -p [PORT]`

Templating
-------------------
Use flask's Jinja2 templating engine for some stuff:
http://jinja.pocoo.org/docs/2.10/

Testing
-------------------
All tests are executed with the testC.py in the testing folder under cs130-cinder/testing. Instructions on running the script can be found in the README in the /testing directory

Again we are using selenium Webdriver and Python to make unit test cases for our website.

Test case 1: login into an existing account and navigate
to the matches page

Test case 2: login into the same account and navigate through the feedback page
Ensures the features of the feedback pages are displayed and functions correctly

Test case 3: create a new user account and fill in random data, and navigate through the profile page to see if the database have been updated.
This test also test if the upload picture works and is stored in the database and shows if the profile picture is correctly displayed on the profile page.
This test tells if the backend and the frontend is connected or not

Test case 4: sign in into the new account to see if we can sign in with the email and password that we previously input.
This test ensures that we can re login into the same account when we open a new session. In addition, it ensures whether the backend is storing the user's’ login information correctly.

Test case 5: sign in into existing user account with a give feedback available, and test if it can actually submit feedback to prior date.
This test is to ensure that the feedback submit form reaches the backend. Note: this test will fail because we cleared the database and a feedback only shows up
when the two parties have been on a date, which we can only do if we wait till the date or we manually modify the database in mllabs


Directory Structure
-----------------------
/cinder - main project files

/cinder/public - contains the html files used for the web app pages

/cinder/src - contains the images and css files for styling the html pages

/cinder/docs - autogenerate documentation with Sphinx

/cinder/config.py, sampleDB.py, manage.py, etc. are related to mongoDB

/public/main - server related files

/testing - testing files
