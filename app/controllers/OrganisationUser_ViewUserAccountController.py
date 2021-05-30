from ..entity.User import User

class OrganisationUser_ViewUserAccountController:
	def __init__(self):
		pass

	def verifyUser(self, NRIC):
		"""
			Returns True if user exists
		"""
		#Create a User Object
		user = User()

		return user.verifyUser(NRIC)

	def getUserDetails(self, NRIC):
		""" 
		Returns a string array containing all the User Details

		"""
		#Create a User Object
		user = User()

		return user.getFullUserData(NRIC)
