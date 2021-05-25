from ..entity.User import User
from ..entity.Alert import Alert

class HealthStaffUser_SendAlertPublicController:
	# Empty Constructor
	def __init__(self):
		pass

	def sendAlert(self, recipient, message, sender):
		"""
			Requests the alert entity to send a new alert
			Returns 
			0 - Sent Successfully
			1 - Invalid User
			2 - Error sending Alert
		"""

		# Verify NRIC
		user = User()

		# 1. Check if user exists
		if not user.verifyUserType(recipient, "Public"):
			return 1

		# Create alert object
		alert = Alert()

		# Return True if alert is sent successfully
		isSent = alert.newAlert(sender, "Public", recipient, message)
		
		# If sending is successful
		if isSent:
			return 0
		
		# If sending has met with an error
		else:
			return 2

