from flask import session, flash, redirect, render_template
from ..controllers.OrganisationUser_GenerateVaccinationStatusReportController import OrganisationUser_GenerateVaccinationStatusReportController

class OrganisationUser_GenerateVaccinationStatusReportUI:
    def __init__(self):
        pass

    def displayPage(self):
        """
        Display the page to view the vaccination status report
        """

        # Check that the user is authorised to access the page
        userType = session['userType'] 
        if userType!= "Organisation":
            flash("Unauthorised to access this content", 'error')
            return redirect('/')

        controller = OrganisationUser_GenerateVaccinationStatusReportController()
        vaccinationStatusData = controller.getVaccinationStatusData()

        # Render the page
        return render_template('organisationUser_generateVaccinationStatusReport.html', userType=userType,
                                                                                    	vaccinationStatusData=vaccinationStatusData)