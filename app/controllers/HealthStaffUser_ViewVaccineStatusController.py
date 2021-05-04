from ..entity.User import User
from ..entity.VaccinationStatus import VaccinationStatus

class HealthStaffUser_ViewVaccineStatusController:
	def __init__(self):
		pass

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
	
	def getPatientVaccineStatusDetails(self, NRIC):
		""" 
		Returns a string array containing the following information.

		[0] - NRIC, 
		[1] - First Name, 
		[2] - Middle Name, 
		[3] - Last Name, 
		[4] - Gender, 
		[5] - FirstShotDate, 
		[6] - SecondShotDate,
		[7] - VaccinationStatus,
		"""

		# Creates a user object
		user = User(NRIC)

		# Creates a VaccinationStatus object
		vaccineStatus = VaccinationStatus(NRIC)
		
		# Returns all details in an array
		userInfo = []
		userInfo.append(NRIC)
		userInfo.append(user.getFirstName())
		userInfo.append(user.getMiddleName())
		userInfo.append(user.getLastName())
		userInfo.append(user.getGender())
		userInfo.append(vaccineStatus.getFirstShotDate())
		userInfo.append(vaccineStatus.getSecondShotDate())
		userInfo.append(vaccineStatus.getVaccinationStatus())
		
		return userInfo