from ..entity.User import User

class HealthStaffUser_ViewPatientDetailsController:
	def __init__(self):
		pass

	def getPatientList(self):
		"""
			Returns an array of all patient's NRIC
		"""

		# Creates a user object
		user = User()

		# Returns a list of all NRIC of patients
		return user.getAllNRIC()

	def verifyPatient(self, NRIC):
		"""
			Returns True if patient exists
		"""
		# Creates a user object
		user = User(NRIC)

		# Returns True if patient exists
		if user.getNRIC() is None:
			return False
		return True

	def getPatientDetails(self, NRIC):
		""" Returns a list containing the following information.

		[0] - NRIC, 
		[1] - First Name, 
		[2] - Middle Name, 
		[3] - Last Name, 
		[4] - Gender, 
		[5] - Mobile Number, 
		"""

		# Creates a user object
		user = User(NRIC)
		
		# Returns all details in an array
		userInfo = []
		userInfo.append(NRIC)
		userInfo.append(user.getFirstName())
		userInfo.append(user.getMiddleName())
		userInfo.append(user.getLastName())
		userInfo.append(user.getGender())
		userInfo.append(user.getMobile())
		
		return userInfo