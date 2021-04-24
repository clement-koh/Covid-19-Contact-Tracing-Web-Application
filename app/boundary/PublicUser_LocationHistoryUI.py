from flask import render_template, session
from ..controllers.PublicUser_LocationHistoryController import PublicUser_LocationHistoryController


class PublicUser_LocationHistoryUI:
	# Empty Constructor
	def __init__(self):
		pass
	
	def displayPage(self):
		"""
		Displays the page showing a user's location history
		"""
		# Create Public User's Location History controller for the current user
		controller = PublicUser_LocationHistoryController(NRIC=session['user'])

		# Get the details for the current User
		date = controller.getDate()
		location = controller.getLocationName()
		timeIn = controller.getTimeIn()
		timeOut = controller.getTimeOut()

		# Create an empty array
		locationHistory = []

		# Populate the dictionary
		for i in range(len(date)):

			# Create an empty dictionary
			record = {}
			record['locationName'] = location[i]
			record['date'] = date[i]
			record['time_in'] = timeIn[i]
			record['time_out'] = timeOut[i]

			# Add the dictionary into the array
			locationHistory.append(record)

		# Displays the webpage
		return render_template('public_viewLocationHistory.html', userType=session['userType'],
															  	  locationHistory=locationHistory)
		