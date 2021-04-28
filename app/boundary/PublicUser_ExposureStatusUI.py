from flask import session
from ..controllers.PublicUser_ExposureStatusController import PublicUser_ExposureStatusController

class PublicUser_ExposureStatusUI:
	# Empty Constructor
	def __init__(self):
		pass

	def getExposureStatus(self):
		"""
		Returns None if the user type is not a public user

		Else Returns the color code "Red", "Yellow", "Green" based
		on his exposure status
		"""

		# Return None if usertype is not Public as other usertype
		# does not have access to this functionality
		if session['userType'] != 'Public':
			return None
		
		else:
			controller = PublicUser_ExposureStatusController()
			return controller.getExposureStatus(session['user'])