from ..entity.User import User

class User_ChangePasswordController:
	# Empty Constructor
	def __init__(self):
		pass

	def validatePassword(self, NRIC, password):
		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		# Verify if the password is correct
		return user.verifyPassword(password)

	def updatePassword(self, NRIC, password):
		"""
		Updates the mobile number of the user.
		Returns True if successfully updated.
		Returns False if unsuccessful
		"""

		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		# Update the password of the user
		return user.updatePassword(password)