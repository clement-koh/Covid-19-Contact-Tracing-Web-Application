from flask import session, render_template, jsonify, flash
from ..controllers.PublicUser_ViewAffectedLocationController import PublicUser_ViewAffectedLocationController
from datetime import datetime, timedelta

class PublicUser_ViewAffectedLocationUI:
	# Define constructor
	def __init__(self):
		pass

	def displayPage(self):
		"""
		Displays the page showing all locations that has been visited by infected individuals
		"""
		# Check if user has permission to access this page
		if session['userType'] != 'Public':
			flash("Unauthorised to access this content", 'error')
			return redirect('/')

		# Displays the webpage
		return render_template('public_viewAffectedLocations.html', userType=session['userType'])

	def getAffectedLocation(self, days_ago):
		"""
		Takes an int to determine the request is for (today - days_ago)'s data
		Return the result in as a string in JSON format
		"""
		controller = PublicUser_ViewAffectedLocationController()

		# Get all infected on X days ago
		infectedPeopleArray = controller.getInfectedPeople(days_ago)

		# Get all location id visited by infected on X days ago
		locationIDArray = controller.getVisitedLocation(days_ago, infectedPeopleArray)
		
		# Get all location name
		locationNameArray = controller.getLocationName(locationIDArray)

		# Get the date and time X days ago
		today = datetime.now()
		today = today.replace(hour=0, minute=0, second=0, microsecond=0)
		record_date = today - timedelta(days=days_ago)

		# Create a dictionary that contains all the information that will contain
		# all the information to be displayed on the webpage
		dictionary = {}
		dictionary['date'] = record_date.strftime('%d %b %Y')	# Date Month Year
		dictionary['no_of_cases'] = len(infectedPeopleArray)
		dictionary['locations'] = locationNameArray

		return jsonify(dictionary)

