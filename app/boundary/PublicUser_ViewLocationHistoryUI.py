from flask import render_template, session, redirect, flash
from ..controllers.PublicUser_ViewLocationHistoryController import PublicUser_ViewLocationHistoryController
from datetime import datetime


class PublicUser_ViewLocationHistoryUI:
	# Empty Constructor
	def __init__(self):
		pass
	
	def displayPage(self):
		"""
		Displays the page showing a user's location history
		"""
		# Ensure that the user is a public user, otherwise redirect to other page
		if session['userType'] != "Public":
			flash("Unauthorised to access this content", 'error')
			return redirect('/')

		# Create Public User's Location History controller for the current user
		controller = PublicUser_ViewLocationHistoryController()

		# Get the details for the current User
		locationHistory = controller.getLocationHistory(session['user'])

		# Displays the webpage with formatted data
		return render_template('public_viewLocationHistory.html', userType=session['userType'],
															  	  locationHistory=locationHistory)
		