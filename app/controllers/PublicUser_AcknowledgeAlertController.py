from ..entity.Alert import Alert

class PublicUser_AcknowledgeAlertController:
	# Empty Constructor
	def __init__(self):
		pass

	def markAlertAsRead(self, id):
		"""
		Returns True is alert is successfully mark as read
		"""
		alert = Alert()

		return alert.markAsRead(id)