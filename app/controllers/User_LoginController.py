from ..entity.User import User

class User_LoginController:
	# Empty Constructor
	def __init__(self):
		pass

	def validateLogin(self, NRIC, password):
		""" 
		Check if the login details provided by is a valid account 
		Returns True if validated else False
		"""

		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		# Verify if the NRIC and password is correct
		return user.verifyLoginDetails(NRIC, password)
		
	def validateAccountStatus(self, NRIC):
		""" 
		Check if the account for the user is active or suspended
		Returns True if account if active
		"""

		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		# Verify if the account is active
		return user.getAccountActive()

	def getAccountType(self, NRIC):
		"""
		Check if the account type of the user
		Returns a string of the account type
		"""

		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		# Get the type of account that is tied to the NRIC
		return user.getAccountType()

	