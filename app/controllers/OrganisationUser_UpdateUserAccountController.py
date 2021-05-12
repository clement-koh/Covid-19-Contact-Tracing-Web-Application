from ..entity.User import User
from ..entity.BusinessUser import BusinessUser
from ..entity.HealthStaffUser import HealthStaffUser
from ..entity.OrganisationUser import OrganisationUser
from ..entity.Business import Business
from ..entity.Organisation import Organisation

class OrganisationUser_UpdateUserAccountController:
    # Empty constructor
    def __init__(self):
        pass

    def getBusinessID(self, businessName):
        # Create a Business object
        business = Business()
        return business.getIDfromName(businessName)
        
    def getBusinessNames(self):
        # Create a Business object
        business = Business()

        # Return an array containing all business names
        businessIDArray = business.getAllBusinessID()
        businessNames = []
        for id in businessIDArray:
            businessObj = Business(id)
            businessNames.append(businessObj.getName())

        return businessNames

    def isDuplicateLicenseNo(self, licenseNo):
        # Create a HealthStaffUser object
        healthStaffUser = HealthStaffUser()
        return healthStaffUser.hasLicenseRecord(licenseNo)

    def getOrganisationID(self, organisationName):
        # Create an Organisation object
        organisation = Organisation()
        return organisation.getIDfromName(organisationName)
        
    def getOrganisationNames(self):
        # Create an Organisation object
        organisation = Organisation()

        # Return an array containing all organisation names
        organisationIDArray = organisation.getAllOrganisationID()
        organisationNames = []
        for id in organisationIDArray:
            organisationObj = Organisation(id)
            organisationNames.append(organisationObj.getName())

        return organisationNames

    def getUserDetails(self, NRIC):
        # Local variables
        businessName = ""
        licenseNo = ""
        organisationName = ""

        # Create a User object
        user = User(NRIC)
        
        if user.getAccountType() == 'Business':
            businessUser = BusinessUser(NRIC)
            businessID = businessUser.getBusinessID()
            business = Business(businessID)
            businessName = business.getName()

        if user.getAccountType() == 'Health Staff':
            healthStaffUser = HealthStaffUser(NRIC)
            licenseNo = healthStaffUser.getLicenseNo()

        if user.getAccountType() == 'Organisation':
            organisationUser = OrganisationUser(NRIC)
            id = organisationUser.getOrganisationID()
            organisation = Organisation(id)
            organisationName = organisation.getName()
        
        userInfo = []
        
        userInfo.append(user.getAccountType())
        userInfo.append(user.getNRIC())
        userInfo.append(user.getFirstName())
        userInfo.append(user.getMiddleName())
        userInfo.append(user.getLastName())
        userInfo.append(user.getGender())
        userInfo.append(user.getMobile())
        userInfo.append(user.getPassword())
        userInfo.append(businessName)
        userInfo.append(licenseNo)
        userInfo.append(organisationName)

        return userInfo

    def updatePublicUser(self, NRIC, firstName, middleName,
                         lastName, gender, mobile, password):
        # Create a User object
        user = User(NRIC)

        # Update the user
        return user.updateExistingUser(firstName, middleName, lastName,
                                        gender, mobile, password)

    def updateBusinessUser(self, NRIC, firstName, middleName, lastName,
                            gender, mobile, password, businessName):
        # Create a BusinessUser object
        businessUser = BusinessUser(NRIC)

        # Create a Business object
        business = Business()
        businessID = business.getIDfromName(businessName)

        # Update the business uer
        return businessUser.updateExistingUser(firstName, middleName, lastName,
                                                gender, mobile, password, businessID)

    def updateHealthStaffUser(self, NRIC, firstName, middleName, lastName,
                              gender, mobile, password, licenseNo):
        # Create a HealthStaffUser object
        healthStaffUser = HealthStaffUser(NRIC)

        # Update the health staff user
        return healthStaffUser.updateExistingUser(firstName, middleName, lastName,
                                                  gender, mobile, password, licenseNo)

    def updateOrganisationUser(self, NRIC, firstName, middleName, lastName,
                                gender, mobile, password, organisationID):
        # Create a OrganisationUser object
        organisationUser = OrganisationUser(NRIC)

        # Update the organisation user
        return organisationUser.updateExistingUser(firstName, middleName, lastName,
                                                    gender, mobile, password, organisationID)