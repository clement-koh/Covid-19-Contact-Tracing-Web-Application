from ..entity.User import User

class User_UpdateContactController:
	def __init__(self):
		pass

	def getUserFirstName(self, NRIC):
		"""
		Returns a string containing 
		the first name of the person tied to this NRIC No.
		"""

		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		return user.getFirstName()

	def getUserMiddleName(self, NRIC):
		"""
		Returns a string containing 
		the middle name of the person tied to this NRIC No.
		"""

		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		return user.getMiddleName()

	def getUserLastName(self, NRIC):
		"""
		Returns a string containing 
		the Last name of the person tied to this NRIC No.
		"""

		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		return user.getLastName()

	def getUserMobile(self, NRIC):
		"""
		Returns an int of 
		the mobile number of the person tied to this NRIC No.
		"""

		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		return user.getMobile()

	def updateMobile(self, NRIC, mobile):
		"""
		Updates the mobile number of the user.
		Returns True if successfully updated.
		Returns False if unsuccessful
		"""

		# Create a user object containing details of the NRIC owner
		user = User(NRIC)

		return user.updateMobile(mobile)