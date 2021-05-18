from flask import session, render_template, redirect, jsonify
from ..controllers.OrganisationUser_ViewInfectionReportController import OrganisationUser_ViewInfectionReportController

class OrganisationUser_ViewInfectionReportUI:
	def __init__(self):
		pass

	def displayPage(self):
		"""
		Displays the page to show infection report
		"""
		# Ensure that the user is authroised to access this page, otherwise redirect to other page
		userType = session['userType']
		if userType != "Organisation":
			flash("Unauthorised to access this content", 'error')
			return redirect('/')

		controller = OrganisationUser_ViewInfectionReportController()

		return render_template('organisationUser_viewInfectionReport.html', userType = session['userType'],
																			dailyInfectionNumbers = controller.get2WeekInfectionCount())

	def getAffectedLocation(self, days_ago):
		"""
		Takes an int to determine the request is for (today - days_ago) days ago's data
		Return the result in as a string in JSON format
		"""
		# Create Controller Object
		controller = OrganisationUser_ViewInfectionReportController()

		# Get all infected on X days ago
		infectedPeopleArray = controller.getInfectedPeople(days_ago)

		# Get all location id visited by infected on X days ago
		locationIDArray = controller.getVisitedLocation(days_ago, infectedPeopleArray)
		
		# Get all location name
		locationNameArray = controller.getLocationName(locationIDArray)

		# Create a dictionary that contains all the information that will contain
		# all the information to be displayed on the webpage
		dictionary = {}
		dictionary['no_of_cases'] = len(infectedPeopleArray)
		dictionary['locations'] = locationNameArray

		return jsonify(dictionary)