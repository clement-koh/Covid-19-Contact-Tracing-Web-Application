from ..entity.VaccinationStatus import VaccinationStatus
from ..entity.User import User
from datetime import datetime

class PublicUser_ViewVaccineCertificateController:
	def __init__(self):
		pass

	def getVaccinationDetails(self, NRIC):
		"""
		Returns a string array containing results from the database

		[0] Patient's full name
		[1] Patient's vaccination status
		[2] First shot date
		[3] Second shot date
		"""
		# Get the vaccination details of the user

		# Creates a User object
		user = User(NRIC)

		# Creates a VaccinationStatus object
		vaccinationStatus = VaccinationStatus(NRIC)

		# Empty list to contain the vaccination details
		vaccinationDetails = []
		
		fullUserDetails = user.getFullUserData(NRIC)
		fullVaccinationDetails = vaccinationStatus.getFullVaccinationData(NRIC)

		fullName = fullUserDetails[2] + " " + fullUserDetails[3] + " " + fullUserDetails[4]

		vaccinationDetails.append(fullName)
		vaccinationDetails.append(fullVaccinationDetails[1])
		vaccinationDetails.append(fullVaccinationDetails[2])
		vaccinationDetails.append(fullVaccinationDetails[3])
		
		if vaccinationDetails[2] is not None:
			vaccinationDetails[2] = datetime.strptime(vaccinationDetails[2], '%d/%m/%Y, %H:%M:%S')
			vaccinationDetails[2] = vaccinationDetails[2].strftime('%d %b %Y')
		
		if vaccinationDetails[3] is not None:
			vaccinationDetails[3] = datetime.strptime(vaccinationDetails[3], '%d/%m/%Y, %H:%M:%S')
			vaccinationDetails[3] = vaccinationDetails[3].strftime('%d %b %Y')

		return vaccinationDetails