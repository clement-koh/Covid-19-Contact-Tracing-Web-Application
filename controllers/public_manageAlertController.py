from ..entities import User, Business, BusinessUser, Alert
from datetime import datetime
from flask import session
import json

class public_manageAlertController:
	@staticmethod
	def getAllAlerts():
		alerts = Alert.getUserAlert(session['user'])
		returned_alerts = []
		for alert in alerts:
			returned_alerts.append({
				'id': alert.id,
				'sent_by': alert.sent_by,
				'sent_on': alert.sent_on,
				'alert_type': alert.alert_type,
				'recipient_NRIC': alert.recipient_NRIC,
				'message': alert.message,
				'is_read': alert.is_read
			})
		return returned_alerts
    
	@staticmethod
	def markAsRead(alert_id):
		result = Alert.updateRecord(alert_id)
		if result:
			return (True, "Alert marked as read")
		return (False, "Failed to mark alert as read")