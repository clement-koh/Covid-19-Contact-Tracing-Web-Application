from ..dbConfig import dbConnect, dbDisconnect
from datetime import datetime

class Alert:
	def __init__(self, id=None):
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# If the id is provided, fill the object with details from database
		hasResult = False
		if id is not None:
			# Select from database and populate instance variables
			result = db.execute("""SELECT id, sent_by, sent_on, alert_type,
								   recipient_NRIC, message, read_on, is_read
								   FROM alert
								   WHERE id = (?)""", (id,)).fetchone()
			
			# Populate private instance variables with value or None 
			if result is not None:
				hasResult = True
				self.__id = result[0]
				self.__sentBy = result[1]
				self.__sentOn = result[2]
				self.__alertType = result[3]
				self.__recipient = result[4]
				self.__message = result[5]
				self.__readOn = result[6]
				self.__isRead = bool(result[7])
		
		# If no result
		if not hasResult:
				self.__id = None
				self.__sentBy = None
				self.__sentOn = None
				self.__alertType = None
				self.__recipient = None
				self.__message = None
				self.__readOn = None
				self.__isRead = None
		
		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Methods
	def getID(self):
		return self.__id
	
	def getSentBy(self):
		return self.__sentBy

	def getSentOn(self):
		return self.__sentOn
	
	def getAlertType(self):
		return self.__alertType

	def getRecipient(self):
		return self.__recipient

	def getMessage(self):
		return self.__message

	def getReadOn(self):
		return self.__readOn

	def getIsRead(self):
		return self.__isRead
	
	# Other Methods
	def newAlert(self, sentBy, alertType, recipient, message):
		""" 
		Adds a new alert into the database
		Returns true if successfully added to database
		"""
		
		# Perform checks on values
		if (sentBy is None or len(str(sentBy.strip())) == 0) or \
			(alertType is None or len(str(alertType).strip()) == 0) or \
			(recipient is None or len(str(recipient).strip()) == 0) or \
			(message is None or len(str(message).strip()) == 0):
			return False

		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		hasError = False
		# Update the account status for the user
		try:
			db.execute("""INSERT INTO alert(sent_by, alert_type, recipient_NRIC, message, sent_on)
						  VALUES((?), (?), (?), (?), (?))""",
						  (sentBy, alertType, recipient, message, datetime.now()))
		except:
			hasError = True

		# Commit the update to the database
		connection.commit()

		# Disconnect from database
		dbDisconnect(connection)

		return not hasError

	def getUserAlerts(self, NRIC):
		"""
		Returns a 2d array of alerts belonging to the user
		
		[][0] - id, 
		[][1] - sent by, 
		[][2] - sent on, 
		[][3] - alert type, 
		[][4] - recipient, 
		[][5] - message, 
		[][6] - read on, 
		[][7] - is read
		"""
		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Select User from database and populate instance variables
		results = db.execute("""SELECT id, sent_by, sent_on, alert_type,
									   recipient_NRIC, message, read_on,
									   is_read 
								FROM alert
								WHERE recipient_NRIC = (?)
								ORDER BY sent_on DESC""", (NRIC,)).fetchall()

		# Disconnect from database
		dbDisconnect(connection)

		# Return search results
		return results

	def markAsRead(self, alertID):
		""" 
		Updates the read status and read timing of the alert 
		Returns True if updated successfully
		Returns False if update failed
		"""

		self.__isRead = True
		self.__readOn = datetime.now()

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Update the read timing and read status for the alert
		db.execute("""UPDATE alert
					  SET read_on = (?),
					  	  is_read = (?)
					  WHERE id = (?)""", (self.__readOn, self.__isRead, alertID))

		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)
		
		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			return True
		
		# If no rows has been updated
		return False