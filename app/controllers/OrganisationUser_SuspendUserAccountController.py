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

		# Create a AccountStatus object containing details of the NRIC owner
		AccountActiveStatus = User(NRIC)

		# Returns True if account is active return false if not.
		if AccountActiveStatus.getAccountActive():
			AccountStatus = True
		else:
			AccountStatus = False

		return AccountActiveStatus.updateAccountStatus(NRIC, AccountStatus)