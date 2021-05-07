from ..entity.VaccinationStatus import VaccinationStatus
from ..entity.User import User

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

        # Creates a User object
        user = User(NRIC)

        # Creates a VaccinationStatus object
        vaccinationStatus = VaccinationStatus(NRIC)

        # Empty list to contain the vaccination details
        vaccinationDetails = []
        
        fullName = user.getFirstName() + " " + user.getMiddleName() + " " + user.getLastName()

        vaccinationDetails.append(fullName)
        vaccinationDetails.append(vaccinationStatus.getVaccinationStatus())
        vaccinationDetails.append(vaccinationStatus.getFirstShotDate())
        vaccinationDetails.append(vaccinationStatus.getSecondShotDate())

        return vaccinationDetails