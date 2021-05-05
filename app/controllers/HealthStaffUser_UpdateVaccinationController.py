from ..entity.VaccinationStatus import VaccinationStatus

class HealthStaffUser_UpdateVaccinationController:
	def __init__(self):
		pass


	def updateVaccinationStatus(self, NRIC, vaccination_Status, dateOfFirstShot, dateOfSecondShot):
		"""
		Updates the Vaccination Status of the patient.
		Returns True if successfully updated.
		Returns False if unsuccessful
		"""

		# Create a VaccinationStatus object containing details of the NRIC owner
		vaccinationstatus = VaccinationStatus(NRIC)

		return vaccinationstatus.updateVaccinationStatus(NRIC, vaccination_Status, dateOfFirstShot, dateOfSecondShot)