from ..entity.User import User

class HealthStaffUser_ViewPatientDetailsController:
	def __init__(self):
		pass

	def verifyPatient(self, NRIC):
		"""
			Returns True if patient exists
		"""
		# Creates a user object
		user = User()
		return user.verifyUser(NRIC)

	def getPatientDetails(self, NRIC):
		""" 
		Returns a string array containing all the User Details

		"""
		return User().getFullUserData(NRIC)