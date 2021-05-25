from ..entity.User import User
from ..entity.VaccinationStatus import VaccinationStatus

class HealthStaffUser_ViewVaccineStatusController:
	def __init__(self):
		pass

	def verifyPatient(self, NRIC):
		"""
			Returns True if patient exists
		"""
		return User().verifyUser(NRIC)

		
	
	def getPatientVaccineStatusDetails(self, NRIC):
		""" 
		Returns a string array containing the following information.

		[0] - NRIC,
		[1] - First Name, 
		[2] - Middle Name, 
		[3] - Last Name, 
		[4] - Gender, 
		[5] - dateOfFirstShot, 
		[6] - dateOfSecondShot
		[7] - vaccinationStatus
		"""

		# Creates a user object
		user = User()

		userData = user.getFullUserData(NRIC)

		# Creates a VaccinationStatus object
		vaccineStatus = VaccinationStatus()

		
		vaccinationstatus = vaccineStatus.getFullVaccinationData(NRIC)

		
		
		# Returns all details in an array
		userInfo = []
		userInfo.append(userData[0])
		userInfo.append(userData[2])
		userInfo.append(userData[3])
		userInfo.append(userData[4])
		userInfo.append(userData[6])
		
		userInfo.append(vaccinationstatus[2])
		userInfo.append(vaccinationstatus[3])
		userInfo.append(vaccinationstatus[1])


		print(userInfo)

		return userInfo