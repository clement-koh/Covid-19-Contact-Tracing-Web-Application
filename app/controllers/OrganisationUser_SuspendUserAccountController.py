from ..entity.User import User

class OrganisationUser_SuspendUserAccountController:
	# Empty constructor
	def __init__(self):
		pass


	def updateAccountStatus(self, NRIC):
		"""
		Updates the Account Status of the user.
		Returns True if successfully updated.
		Returns False if unsuccessful
		"""		
		
		# Create a AccountStatus object containing details of the NRIC owner
		user = User(NRIC)

		# Toggles the account active status for the user
		return user.updateAccountActive()