from flask import session, render_template, redirect
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