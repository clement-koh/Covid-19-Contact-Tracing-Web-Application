from ..entity.Alert import Alert

import unittest

class testCases_HealthStaffUser_SendAlertPublicEntity(unittest.TestCase):
	def setUp(self):
		# Create boundary object
		self.alert = Alert()

	# ----------------------------------------------------
	#		Test Empty Constructor & Accessor Method
	# ----------------------------------------------------

	def test_Alert_getIDIsNone(self):
		result = self.alert.getID()
		self.assertIsNone(result, "Empty Alert object should have no ID, but a value was returned")

	def test_Alert_getSentByIsNone(self):
		result = self.alert.getSentBy()
		self.assertIsNone(result, "Empty Alert object should have no sender, but a value was returned")

	def test_Alert_getSentOnIsNone(self):
		result = self.alert.getSentOn()
		self.assertIsNone(result, "Empty Alert object should have no sent timing, but a value was returned")
	
	def test_Alert_getAlertTypeIsNone(self):
		result = self.alert.getAlertType()
		self.assertIsNone(result, "Empty Alert object should have no alert type, but a value was returned")
	
	def test_Alert_getRecipientIsNone(self):
		result = self.alert.getRecipient()
		self.assertIsNone(result, "Empty Alert object should have no recipient, but a value was returned")
	
	def test_Alert_getMessageIsNone(self):
		result = self.alert.getMessage()
		self.assertIsNone(result, "Empty Alert object should have no message, but a value was returned")

	def test_Alert_getReadOnIsNone(self):
		result = self.alert.getReadOn()
		self.assertIsNone(result, "Empty Alert object should have no read timing, but a value was returned")

	def test_Alert_getIsReadIsNone(self):
		result = self.alert.getIsRead()
		self.assertIsNone(result, "Empty Alert object should not be read, but a value was returned")

	# ----------------------------------------------------
	#					Test newAlert method
	# ----------------------------------------------------

	# Test with correct values
	def test_newAlert_acceptsCorrectValue(self):
		errorMsg = "Correct values provided, expected True but returned False"
		result = self.alert.newAlert("S1999", "Entity Test Case", "S0999", "Message from ENTITY test case with correct values")
		self.assertTrue(result, errorMsg)

	# Test with incorrect SENTBY values
	def test_newAlert_rejectsBlankSender(self):
		errorMsg = "No sender provided, expected False but returned True"
		result = self.alert.newAlert("", "Entity Test Case", "S0999", "Message from ENTITY test case with incorrect values")
		self.assertFalse(result, errorMsg)

	def test_newAlert_rejectsInvalidSender(self):
		errorMsg = "Invalid sender provided, expected False but returned True"
		result = self.alert.newAlert("InvalidUser", "Entity Test Case", "S0999", "Message from ENTITY test case with incorrect values")
		self.assertFalse(result, errorMsg)
	
	def test_newAlert_rejectsPublicUserAsSender(self):
		errorMsg = "Public user's NRIC provided as sender, expected False but returned True"
		result = self.alert.newAlert("S0999", " Entity Test Case", "S0999", "Message from ENTITY test case with incorrect values")
		self.assertFalse(result, errorMsg)

	def test_newAlert_rejectsBusinessUserAsSender(self):
		errorMsg = "Business user's NRIC provided as sender, expected False but returned True"
		result = self.alert.newAlert("S2999", " EntityTest Case", "S0999", "Message from ENTITY test case with incorrect values")
		self.assertFalse(result, errorMsg)
	
	def test_newAlert_rejectsOrganisationUserAsSender(self):
		errorMsg = "Organisation user's NRIC provided as sender, expected False but returned True"
		result = self.alert.newAlert("S3999", "Entity Test Case", "S0999", "Message from ENTITY test case with incorrect values")
		self.assertFalse(result, errorMsg)

	# Test with incorrect ALERTTYPE values
	def test_newAlert_rejectsBlankAlertType(self):
		errorMsg = "Alert type is empty, expected False but returned True"
		result = self.alert.newAlert("S1999", "", "S0999", "Message from ENTITY test case with incorrect values")
		self.assertFalse(result, errorMsg)

	# Test with incorrect RECIPIENT values
	def test_newAlert_rejectsBlankRecipient(self):
		errorMsg = "Recipient is empty, expected False but returned True"
		result = self.alert.newAlert("S1999", "Entity Test Case", "", "Message from ENTITY test case with incorrect values")
		self.assertFalse(result, errorMsg)
	
	def test_newAlert_rejectsInvalidRecipient(self):
		errorMsg = "Recipient was provided with a invalid value, expected False but returned True"
		result = self.alert.newAlert("S1999", "Entity Test Case", "InvalidUser", "Message from ENTITY test case with incorrect values")
		self.assertFalse(result, errorMsg)

	# Test with incorrect MESSAGE values
	def test_newAlert_rejectsBlankMessage(self):
		errorMsg = "No message is provided for the alert, expected False but returned True"
		result = self.alert.newAlert("S1999", "Entity Test Case", "S0999", "")
		self.assertFalse(result, errorMsg)

if __name__ == '__main__':
	unittest.main(verbosity=2)