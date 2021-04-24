import os
from flask import Flask, session, redirect
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# Set templates and static directory
template_dir = os.path.abspath('./app/templates')
static_dir = os.path.abspath('./app/static')

# Configure app to run from this file
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Configure app to run if this file is executed
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

# Database Settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app/db.sqlite3'

# Sessions secret key
app.secret_key="mykey123456"

# Database Settings
db = SQLAlchemy(app)

# Makes a route unable to be visited unless logged in
def loginRequired(function):
	@wraps(function)
	def decorated_function(*args, **kwargs):
		# If user is not authenticated
		try:
			# If user is authenticated, proceed as per normal
			if session['isAuthenticated']:
				print("User authenticated")
				print(session['userType'])
				return function()
			
		except KeyError as e:
			# if session['isAuthenticated'] is None or not session['isAuthenticated']:
			print(e)
		print("User not authenticated, Redirecting")
		return redirect('/login')
	return decorated_function

from .app import routes

