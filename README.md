# cs130-cinder
Team "Need One More" from Lab 1A

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
All tests are executed with the seleniumExample.py script in /testing/examples. Instructions on running the script can be found in the README in the /testing directory

Test One - navbar is functional and a user can click through the pages. We expect clicking on the various page links will take you to the correct page.

Test Two - Sign-up workflow. We expect filling out the required information and hitting "Submit" will create and account and redirect you to the "Meet People" page.

Test Three - Feedback Response. We expect navigating to the "Feedback" page and clicking "Give Feedback" will open a pop-up feedback form.


Test Four - Swiping Right. We expect clicking the right pointing arrow on the "Meet People" page will 'swipe right' to a new user (currently dummy data).

Directory Structure
-----------------------
/cinder - main project files

/cinder/public - contains the html files used for the web app pages

/cinder/src - contains the images and css files for styling the html pages

/cinder/docs - autogenerate documentation with Sphinx

/cinder/config.py, sampleDB.py, manage.py, etc. are related to mongoDB

/public/main - server related files

/testing - testing files
