from ..entity.User import User

class User_UpdateContactController:
	def __init__(self):
		pass

	def getUserDetails(self, NRIC):
		""" 
		Returns a string array containing all the User Details

		"""
		return User().getFullUserData(NRIC)
		
	def updateMobile(self, NRIC, mobile):
		"""
		Updates the mobile number of the user.
		Returns True if successfully updated.
		Returns False if unsuccessful
		"""

		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		return user.updateMobile(mobile)