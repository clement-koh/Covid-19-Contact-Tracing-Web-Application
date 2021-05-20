from flask import session, flash, redirect, render_template
from ..controllers.OrganisationUser_ViewVaccinationStatusReportController import OrganisationUser_ViewVaccinationStatusReportController

class OrganisationUser_ViewVaccinationStatusReportUI:
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

        controller = OrganisationUser_ViewVaccinationStatusReportController()
        vaccinationStatusData = controller.getVaccinationStatusData()

        # Render the page
        return render_template('organisationUser_viewVaccinationStatusReport.html', userType=userType,
                                                                                    vaccinationStatusData=vaccinationStatusData)