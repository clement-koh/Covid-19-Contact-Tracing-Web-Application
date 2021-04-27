from flask import render_template, session

class User_OverviewUI:
	# Empty Constructor
	def __init__(self):
		pass

	def displayPage(self, healthStatus=None):
		return render_template('overview.html', userType = session['userType'],
												healthStatus = healthStatus)