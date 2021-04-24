from flask import render_template, session, redirect, flash
from ..controllers.PublicUser_LocationHistoryController import PublicUser_LocationHistoryController
from datetime import datetime


class PublicUser_LocationHistoryUI:
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
		controller = PublicUser_LocationHistoryController()

		# Get the details for the current User
		results = controller.getLocationHistory(session['user'])

		# Create an empty array
		locationHistory = []

		# Check if result is empty
		if results is not None:
			# Populate the dictionary after formating the results to be display
			for result in results:
				
				checkInTime = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S.%f')
				checkoutTime = datetime.strptime(result[4], '%Y-%m-%d %H:%M:%S.%f')

				# Create an empty dictionary
				record = {}

				# Records the location name
				record['locationName'] = controller.getLocationName(result[2])
				
				# Gets the date
				record['date'] = checkInTime.strftime('%d %b %Y') 
				
				# Format the time in 24 hours timing (eg. 13:45)
				record['time_in'] = '{:02d}:{:02d}'.format(checkInTime.hour,
														   checkInTime.minute)
				record['time_out'] = '{:02d}:{:02d}'.format(checkoutTime.hour,
														    checkoutTime.minute)

				# Add the dictionary into the array
				locationHistory.append(record)

		# Displays the webpage with formatted data
		return render_template('public_viewLocationHistory.html', userType=session['userType'],
															  	  locationHistory=locationHistory)
		