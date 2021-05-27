from ..entity.User import User
from ..entity.BusinessUser import BusinessUser
from ..entity.HealthStaffUser import HealthStaffUser
from ..entity.OrganisationUser import OrganisationUser
from ..entity.Business import Business
from ..entity.Organisation import Organisation

class OrganisationUser_CreateUserController:
	# Empty Constructor
	def __init__(self):
		pass

	def getBusinessNames(self):
		# Create business object
		business = Business()
		
		# Return array containing all business name
		businessIDArray = business.getAllBusinessID()
		businessNames = []
		for id in businessIDArray:
			businessTemp = Business(id)
			businessNames.append(businessTemp.getName())

		return businessNames

	def getOrganisationNames(self):
		# Create organisation object
		organisation = Organisation()

		# Return array containing all organisation name
		organisationIDArray = organisation.getAllOrganisationID()
		organisationNames = []
		for id in organisationIDArray:
			organisationTemp = Organisation(id)
			organisationNames.append(organisationTemp.getName())

		return organisationNames
	
	def isDuplicateNRIC(self, NRIC):
		# Create User Object
		user = User()

		# Check if user exists
		if user.verifyUser(NRIC):
			return True
		
		# If user does not exists
		return False
	
	def isDuplicateLicenseNo(self, licenseNo):
		# Create Health Staff User Object
		healthStaffUser = HealthStaffUser()
		return healthStaffUser.hasLicenseRecord(licenseNo)

	def getBusinessID(self, businessName):
		# Create business object
		business = Business()
		return business.getIDfromName(businessName)

	def getOrganisationID(self, organisationName):
		# Create organisation object
		organisation = Organisation()
		return organisation.getIDfromName(organisationName)

	def addNewPublicUser(self, NRIC, firstName, middleName,
						lastName, gender, mobile, password):
		# Create user entity object
		user = User()

		# Create a new user
		return user.addNewUser(NRIC, firstName, middleName,
								lastName, gender, mobile, password)
	
	def addNewHealthStaffUser(self, NRIC, firstName, middleName,
			 				lastName, gender, mobile, password, licenseNo):
		# Create HealthStaffUser entity object							 
		healthStaffUser = HealthStaffUser()

		# Create a new user
		return healthStaffUser.addNewUser(NRIC, firstName, middleName,
			lastName, gender, mobile, password, licenseNo)

	def addNewBusinessUser(self, NRIC, firstName, middleName,
							lastName, gender, mobile, password, businessID):
		# Create BusinessUser entity object	
		businessUser = BusinessUser()

		# Create a new user
		return businessUser.addNewUser(NRIC, firstName, middleName,
			lastName, gender, mobile, password, businessID)

	def addNewOrganisationUser(self, NRIC, firstName, middleName,
								lastName, gender, mobile, password, organisationID):
		# Create BusinessUser entity object	
		organisationUser = OrganisationUser()

		# Create a new user
		return organisationUser.addNewUser(NRIC, firstName, middleName,
			lastName, gender, mobile, password, organisationID)