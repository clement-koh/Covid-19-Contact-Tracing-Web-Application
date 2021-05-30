from flask import session, flash, redirect, render_template
from ..controllers.PublicUser_ViewVaccineCertificateController import PublicUser_ViewVaccineCertificateController
from datetime import datetime

class PublicUser_ViewVaccineCertificateUI:
	def __init__(self):
		pass

	def displayPage(self):
		"""
		Displays the page showing either the current user's vaccination certificate
		or their current vaccination status if they are not fully vaccinated
		"""
		# Get current user type
		currentUserType = session['userType']

		# If unauthorized, redirect user
		if currentUserType != 'Public':
			flash('You do not have permission to access the requested functionality', 'error')
			return redirect('/')

		# Initialize controller for public user to view their vaccination certificate
		controller = PublicUser_ViewVaccineCertificateController()

		# Get the vaccination details of the user
		vaccinationDetails = controller.getVaccinationDetails(session['user'])
		
		return render_template('public_viewVaccineCertificate.html', userType=currentUserType,
																	 vaccinationDetails=vaccinationDetails)