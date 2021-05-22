from ..entity.VaccinationStatus import VaccinationStatus

class OrganisationUser_GenerateVaccinationStatusReportController:
    def __init__(self):
        pass

    def getVaccinationStatusData(self):
        """
        Returns an integer array containing the following:

        [0] - Total number of records in the vaccination status table,
        [1] - Number of people who are fully vaccinated,
        [2] - Number of people who have taken the first dose,
        [3] - Number of people who are eligible but not vaccinated,
        [4] - Number of people who are not eligible for vaccination
        """

        vaccinationStatus = VaccinationStatus()
        
        return vaccinationStatus.getVaccinationStatusData()
