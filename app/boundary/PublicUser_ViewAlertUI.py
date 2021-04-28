from flask import session, flash, redirect, render_template
from ..controllers.PublicUser_ViewAlertController import PublicUser_ViewAlertController

class PublicUser_ViewAlertUI:
	# Empty Constructor
	def __init__(self):
		pass

	def displayPage(self):
		"""
		Displays the page showing all alerts for the current user
		"""
		# Get current user type
		currentUserType = session['userType']

		# If unauthorized, redirect user
		if currentUserType != 'Public':
			flash('You do not have permission to access the requested functionality', 'error')
			return redirect('/')
		
		# Initialize controller for public user to view alerts
		controller = PublicUser_ViewAlertController()

		# Get all alerts for the user
		all_alerts = controller.getAllAlerts(session['user'])

		# Format data to be displayed
		formatted_alert = []
		for alert in all_alerts:
			alertData = {}
			alertData['id'] = alert[0]
			alertData['sent_on'] = alert[2]
			alertData['message'] = alert[5]
			alertData['is_read'] = bool(alert[7])
			formatted_alert.append(alertData)

		# Renders the webpage for with alerts for the user
		return render_template('public_viewAlert.html', userType=currentUserType,
														all_alerts=formatted_alert)

