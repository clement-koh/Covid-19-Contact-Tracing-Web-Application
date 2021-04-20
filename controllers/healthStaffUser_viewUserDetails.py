from ..entities import User

class healthStaffUser_viewUserDetails:
	@staticmethod
	def getUserSearchDetails():
		# Get search result
		results = User.getAllUser()

		# Format the result
		adjustedResult = []
		for result in results:
			adjustedResult.append(result.NRIC)
		return adjustedResult
	
	@staticmethod
	def getUserDetails(NRIC):
		# Get search result
		result = User.getUser(NRIC)

		# Invalid option entered
		if result is None:
			return None

		# Format the result
		adjustedResult = []
		adjustedResult.append({"NRIC": result.NRIC,"firstName": result.firstName, "middleName": result.middleName,
								"lastName" : result.lastName,"gender": result.gender,"mobile": result.mobile})

		# Return adjusted result
		return adjustedResult