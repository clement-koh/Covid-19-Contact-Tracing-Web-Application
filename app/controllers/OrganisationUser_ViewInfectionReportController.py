from ..entity.InfectedPeople import InfectedPeople

class OrganisationUser_ViewInfectionReportController:
	# Empty Constructor
	def __init__(self):
		self.INFECTION_TIME = 14  #No of days to be considered as infected

	def get2WeekInfectionCount(self):
		"""
		Returns the daily infection count for the past 2 weeks in an array
		Latest date being [13]
		"""
		
		# Create entity object	
		infectedPeople = InfectedPeople()

		# Create an array to store the result
		result = []

		# Gets the number of infected people the last 14 days (include today)
		for i in reversed(range(14)):
			result.append(len(infectedPeople.getInfectedPeople(i, self.INFECTION_TIME)))

		return result
		



