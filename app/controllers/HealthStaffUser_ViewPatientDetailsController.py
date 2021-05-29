from ..entity.User import User

class HealthStaffUser_ViewPatientDetailsController:
	def __init__(self):
		pass

	def verifyPatient(self, NRIC):
		"""
			Returns True if patient exists
		"""
		#Create a User Object
		user = User()

		return user.verifyUser(NRIC)

	def getPatientDetails(self, NRIC):
		""" 
		Returns a string array containing all the User Details

		"""
		#Create a User Object
		user = User()
		
		return user.getFullUserData(NRIC)