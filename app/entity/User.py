from ..dbConfig import dbConnect, dbDisconnect

class User:
	# Constructor for user
	def __init__(self, NRIC=None):
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		# If the NRIC is provided, fill the object with details from database
		hasResult = False
		if NRIC is not None:
			# Select User from database and populate instance variables
			result = db.execute("""SELECT NRIC, password, firstName,
										middleName, lastName, mobile, gender,
										accountActive, accountType
								FROM user 
								WHERE NRIC = (?)""", (NRIC,)).fetchone()

			# If a result is returned, populate object with data
			if result is not None:
				hasResult = True
				# Initialise instance variables for this object
				self.__NRIC = NRIC
				self.__password = result[1]
				self.__firstName = result[2]
				self.__middleName = result[3]
				self.__lastName = result[4]
				self.__mobile = result[5]
				self.__gender = result[6]
				self.__accountActive = result[7]
				self.__accountType = result[8]
		
		if not hasResult:
			self.__NRIC = None
			self.__password = None
			self.__firstName = None
			self.__middleName = None
			self.__lastName = None
			self.__mobile = None
			self.__gender = None
			self.__accountActive = None
			self.__accountType = None

		# Disconnect from database
		dbDisconnect(connection)

	# Accessor Methods
	def getNRIC(self):
		"""Returns the NRIC of the user"""
		return self.__NRIC

	def getPassword(self):
		"""Returns the Password of the user"""
		return self.__password

	def getFirstName(self):
		"""Returns the first name of the user"""
		return self.__firstName
	
	def getMiddleName(self):
		"""Returns the middle name of the user"""
		return self.__middleName

	def getLastName(self):
		"""Returns the last name of the user"""
		return self.__lastName

	def getMobile(self):
		"""Returns the mobile number of the user"""
		return self.__mobile
	
	def getGender(self):
		"""Returns the gender of the user"""
		return self.__gender
	
	def getAccountActive(self):
		"""Returns True if account is active"""
		return bool(self.__accountActive)
	
	def getAccountType(self):
		"""Returns the accountType of the user"""
		return self.__accountType

	# Mutator Methods
	def updatePassword(self, old_pw, new_pw):
		""" 
		Updates the password of the user. 
		Returns True if updated successfully
		Returns False if update failed
		"""

		#if old password is NOT equal to database return false
		if old_pw != self.__password:
			return False
		
		else:
			# Update the object's recorded password"
			self.__password = new_pw
			# Open connection to database
			connection = dbConnect()
			db = connection.cursor()

			# Update the password for the user
			db.execute("""UPDATE user
						SET password = (?)
						WHERE NRIC = (?)""", (new_pw, self.__NRIC))
			
			# Commit the update to the database
			connection.commit()
			
			# Close the connection to the database
			dbDisconnect(connection)
			
			# Check if any rows have been updated successfully
			if db.rowcount != 0:
				return True
			
			# If no rows has been updated
			return False	

	def updateMobile(self, mobile):
		""" 
		Updates the mobile number of the user
		Returns True if updated successfully
		Returns False if update failed
		"""

		# Update the object's recorded mobile number"
		self.__mobile = mobile

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Update the mobile number for the user
		db.execute("""UPDATE user
					  SET mobile = (?)
					  WHERE NRIC = (?)""", (mobile, self.__NRIC))

		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)
		
		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			return True
		
		# If no rows has been updated
		return False

	def updateAccountActive(self):
		"""
		Updates account status of the user.
		Returns True if updated successfully
		Returns False if update failed
		"""

		# Update the object's recorded account status"
		self.__accountActive = not self.__accountActive

		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Update the account status for the user
		db.execute("""UPDATE user
					  SET accountActive = (?)
					  WHERE NRIC = (?)""", (self.__accountActive, self.__NRIC))

		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)
		
		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			return True
		
		# If no rows has been updated
		return False
	
	# Other Methods
	def verifyUser(self,NRIC):
		""" 
		Verify the user against retrieved data from database
		Returns True if verified successfully
		Returns False if verification does not match
		"""
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()

		
		hasResult = False
		if NRIC is not None:
			# Select User from database
			result = db.execute("""SELECT NRIC, password, firstName,
										middleName, lastName, mobile, gender,
										accountActive, accountType
								FROM user 
								WHERE NRIC = (?)""", (NRIC,)).fetchone()

			
			if result is not None:
				hasResult = True

		# Disconnect from database
		dbDisconnect(connection)

		return hasResult

	def verifyLoginDetails(self, NRIC, password):
		""" 
		Verify the login details against retrieved data from database
		Returns True if verified successfully
		Returns False if verification does not match
		"""
		if self.__NRIC == NRIC and self.__password == password:
			return True
		return False

	def verifyPassword(self, password):
		""" 
		Verify the password against retrieved data from database
		Returns True if verified successfully
		Returns False if verification does not match
		"""
		return self.__password == password

	def getFullUserData(self,NRIC):
		""" 
		Returns a string array containing the following information.

		[0] - NRIC,
		[1] - Password, 
		[2] - First Name, 
		[3] - Middle Name, 
		[4] - Last Name, 
		[5] - Mobile Number, 
		[6] - Gender,
		[7] - AccountActive, 
		[8] - AccountType

		"""

		# Connect to database
		connection = dbConnect()
		db = connection.cursor()


		# Select User from database
		results = db.execute("""SELECT NRIC, password, firstName,
								middleName, lastName, mobile, gender,
								accountActive, accountType
								FROM user 
								WHERE NRIC = (?)""", (NRIC,)).fetchone()


		userInfo = []
		userInfo.append(results[0])
		userInfo.append(results[1])
		userInfo.append(results[2])
		userInfo.append(results[3])
		userInfo.append(results[4])
		userInfo.append(results[5])
		userInfo.append(results[6])

		# Local variable
		accountStatus = None
		
		# Returns account status
		if results[7]:
			accountStatus = "Active"
		else:
			accountStatus = "Suspended"
		
		userInfo.append(accountStatus)
		userInfo.append(results[8])

		# Disconnect from database
		dbDisconnect(connection)

		return userInfo
		
	def verifyUserType(self, NRIC, userType):
		# Connect to database
		connection = dbConnect()
		db = connection.cursor()


		# Select User from database
		results = db.execute("""SELECT accountType
								FROM user 
								WHERE NRIC = (?)""", (NRIC,)).fetchone()
		
		# Disconnect from database
		dbDisconnect(connection)

		if results is None or userType != results[0]:
			return False
		else:
			return True
	
		

	def addNewUser(self, NRIC, firstName, middleName,
					lastName, gender, mobile, password,
					accountType='Public'):
		"""
		Returns True if record is successfully added to database
		"""
		
		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()
		
		# insert new user record
		db.execute("""INSERT INTO user(
							NRIC, password, firstName,
							middleName, lastName, mobile, gender,
							accountActive, accountType
						)
						VALUES((?), (?), (?), (?), (?), (?), (?), (?), (?))""",
						(NRIC, password, firstName, middleName, lastName, mobile,
						gender, True, accountType))
		
		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)

		# Check if any rows have been updated successfully
		if db.rowcount != 0:
			print("Added new User")
			return True
		
		# If no rows has been updated
		return False
		
	def updateExistingUser(self, firstName, middleName, lastName,
							gender, mobile, password):
		"""
		Updates the details of an existing user
		Returns True if record is successfully updated in the database
		"""
		# Open connection to database
		connection = dbConnect()
		db = connection.cursor()

		# Update existing user record
		db.execute("""UPDATE user
						SET firstName = (?), middleName = (?), lastName = (?),
						gender = (?), mobile = (?), password = (?)
						WHERE NRIC = (?)""", (firstName, middleName, lastName,
												gender, mobile, password, self.__NRIC))
		
		# Commit the update to the database
		connection.commit()

		# Close the connection to the database
		dbDisconnect(connection)

		# Check if any row has been updated successfully
		if db.rowcount != 0:
			print("Updated existing User")
			return True
		
		# If no row has been updated
		return False

