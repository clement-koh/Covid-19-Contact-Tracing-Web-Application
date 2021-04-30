from flask import render_template, flash, redirect, session
from ..controllers.BusinessUser_ViewAffectedOutletController import BusinessUser_ViewAffectedOutletController
import json

class BusinessUser_ViewAffectedOutletUI:
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
		if currentUserType != 'Business':
			flash('You do not have permission to access the requested functionality', 'error')
			return redirect('/')

		# Initialise controller
		controller = BusinessUser_ViewAffectedOutletController()

		# Get which business the user belongs to
		businessID = controller.getUserBusinessID(session['user'])
		
		# Get the locations for this business
		locationIDArray = controller.getAllBusinessLocation(businessID)

		# Get the results for the past 14 days by providing the array
		results = controller.getBusinessInfectedRecord(locationIDArray)
		print(results)

		# Render the webpage
		return render_template('business_viewAffectedOutlet.html', userType=currentUserType,
																   locationDetails=json.loads(results))
