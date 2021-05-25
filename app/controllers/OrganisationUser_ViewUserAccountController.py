from ..entity.User import User

class OrganisationUser_ViewUserAccountController:
	def __init__(self):
		pass

	def verifyUser(self, NRIC):
		"""
			Returns True if user exists
		"""

		return User().verifyUser(NRIC)

	def getUserDetails(self, NRIC):
		""" 
		Returns a string array containing all the User Details

		"""
		
		return User().getFullUserData(NRIC)
