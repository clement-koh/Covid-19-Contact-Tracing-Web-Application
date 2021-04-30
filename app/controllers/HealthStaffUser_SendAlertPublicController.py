from ..entity.User import User
from ..entity.Alert import Alert

class HealthStaffUser_SendAlertPublicController:
	# Empty Constructor
	def __init__(self):
		pass

	def verifyNRIC(self, NRIC):
		"""
			Returns True if the NRIC provided is a valid user
		"""
		# Create User Object
		user = User(NRIC)

		if user.getNRIC() is None:
			return False
		return True

	def sendAlert(self, recipient, message, sender):
		"""
			Requests the alert entity to send a new alert
			Returns True is sent successfully
		"""
		# Create alert object
		alert = Alert()

		# Return True if alert is sent successfuly
		return alert.newAlert(sender, "Public", recipient, message)

