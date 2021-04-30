from ..entity.Alert import Alert

class BusinessUser_ViewAlertController:
	def __init__(self):
		pass

	def getAllAlerts(self, NRIC):
		"""
		Returns a string 2d array of alerts belonging to the user
		
		[][0] - id, 
		[][1] - sent by, 
		[][2] - sent on, 
		[][3] - alert type, 
		[][4] - recipient, 
		[][5] - message, 
		[][6] - read on, 
		[][7] - is read
		"""
		# Initialize alert entity
		alert = Alert()

		return alert.getUserAlerts(NRIC)