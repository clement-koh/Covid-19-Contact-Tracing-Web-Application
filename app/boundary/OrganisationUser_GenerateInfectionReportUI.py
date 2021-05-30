from operator import rshift
from flask import session, render_template, redirect, jsonify
from ..controllers.OrganisationUser_GenerateInfectionReportController import OrganisationUser_GenerateInfectionReportController

class OrganisationUser_GenerateInfectionReportUI:
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

		controller = OrganisationUser_GenerateInfectionReportController()

		return render_template('organisationUser_generateInfectionReport.html', userType = session['userType'],
																				dailyInfectionNumbers = controller.get2WeekInfectionCount())

	def getAffectedLocation(self, days_ago):
		"""
		Takes an int to determine the request is for (today - days_ago) days ago's data
		Return the result in as a string in JSON format
		"""
		# Create Controller Object
		controller = OrganisationUser_GenerateInfectionReportController()

		# Get all infected on X days ago and all location names
		result = controller.getInfectionData(days_ago)

		# Create a dictionary that contains all the information that will contain
		# all the information to be displayed on the webpage
		dictionary = {}
		dictionary['no_of_cases'] = result[0]
		dictionary['locations'] = result[1]

		return jsonify(dictionary)