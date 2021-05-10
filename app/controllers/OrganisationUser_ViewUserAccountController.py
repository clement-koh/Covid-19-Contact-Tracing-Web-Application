from ..entity.User import User

class OrganisationUser_ViewUserAccountController:
	def __init__(self):
		pass

	def verifyUser(self, NRIC):
		"""
			Returns True if user exists
		"""
		# Creates a user object
		user = User(NRIC)

		# Returns True if patient exists
		if user.getNRIC() is None:
			return False
		return True

	def getUserDetails(self, NRIC):
		""" 
		Returns a string array containing the following information.

		[0] - NRIC, 
		[1] - First Name, 
		[2] - Middle Name, 
		[3] - Last Name, 
		[4] - Mobile Number, 
		[5] - Account Type, 
		[6] - Account Status, 
		"""
		# Local variable
		accountStatus = None

		# Creates a user object
		user = User(NRIC)
		
		# Returns all details in an array
		userInfo = []
		userInfo.append(NRIC)
		userInfo.append(user.getFirstName())
		userInfo.append(user.getMiddleName())
		userInfo.append(user.getLastName())
		userInfo.append(user.getMobile())
		userInfo.append(user.getAccountType())

		# Returns account status
		if user.getAccountActive():
			accountStatus = "Active"
		else:
			accountStatus = "Suspended"
		
		userInfo.append(accountStatus)
		
		return userInfo
