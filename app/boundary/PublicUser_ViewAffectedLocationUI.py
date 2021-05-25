from flask import session, render_template, jsonify, flash
from ..controllers.PublicUser_ViewAffectedLocationController import PublicUser_ViewAffectedLocationController


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

		# Get Daily Affected Location Data
		affectedLocationRecords = controller.getAffectedLocationRecords(days_ago)

		return jsonify(affectedLocationRecords)