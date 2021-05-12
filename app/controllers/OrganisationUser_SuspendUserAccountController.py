from ..entity.User import User

class OrganisationUser_SuspendUserAccountController:
	# Empty constructor
	def __init__(self):
		pass


	def updateAccountStatus(self, NRIC, AccountStatus):
		"""
		Updates the Account Status of the user.
		Returns True if successfully updated.
		Returns False if unsuccessful
		"""

		# Returns account status to database value 
		if AccountStatus == "Active":
			AccountStatus = "1"
		else:
			AccountStatus = "0"
		
		
		

		# Create a AccountStatus object containing details of the NRIC owner
		AccountActiveStatus = User(NRIC)

		return AccountActiveStatus.updateAccountStatus(NRIC, AccountStatus)