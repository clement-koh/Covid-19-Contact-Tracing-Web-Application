from flask import redirect, session, flash

class User_LogoutUI:
	# Empty Constructor
	def __init__(self):
		pass

	def logout(self):
		"""
		Updates the session of the current user to logged off
		"""

		session['isAuthenticated'] = False
		session['user'] = None
		session['userType'] = None
	
	def redirectToLogin(self):
		"""
		Redirect to login page with the notification that 
		they have logged out successfully
		"""

		flash('Logged out successfully')
		return redirect('/login')

