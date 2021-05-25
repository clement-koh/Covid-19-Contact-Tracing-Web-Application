from ..entity.User import User
from ..entity.Alert import Alert

class HealthStaffUser_SendAlertPublicController:
	# Empty Constructor
	def __init__(self):
		pass

	def sendAlert(self, recipient, message, sender):
		"""
			Requests the alert entity to send a new alert
			Returns True is sent successfully
		"""
		# Private variable
		validationCode = 0

		# Verify NRIC
		user = User(recipient)

		if user.getNRIC() is None or user.getAccountType() != "Public":
			validationCode = -1
			return validationCode

		# Create alert object
		alert = Alert()

		# Return True if alert is sent successfully
		isSent = alert.newAlert(sender, "Public", recipient, message)
		if isSent == True:
			return validationCode
		else:
			validationCode = -2
			return validationCode

