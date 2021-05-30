from ..controllers.HealthStaffUser_SendAlertPublicController import HealthStaffUser_SendAlertPublicController

import unittest

class testCases_HealthStaffUser_SendAlertPublicController(unittest.TestCase):
	def setUp(self):
		# Create boundary object
		self.controller = HealthStaffUser_SendAlertPublicController()

	# ----------------------------------------------------
	#					Test verifyNRIC method
	# ----------------------------------------------------

	# # Test with correct value
	# def test_verifyNRIC_acceptsPublicNRIC(self):
	# 	errorMsg = "Public user's NRIC provided, expected True but returned False"
	# 	result = self.controller.verifyNRIC("S0999")
	# 	self.assertTrue(result, errorMsg)
	
	# # Test with incorrect value
	# def test_verifyNRIC_rejectsHealthStaffUserNRIC(self):
	# 	errorMsg = "Health Staff user's NRIC provided, expected False but returned True"
	# 	result = self.controller.verifyNRIC("S1999")
	# 	self.assertFalse(result, errorMsg)

	# def test_verifyNRIC_rejectsBusinessUserNRIC(self):
	# 	errorMsg = "Business user's NRIC provided, expected False but returned True"
	# 	result = self.controller.verifyNRIC("S2999")
	# 	self.assertFalse(result, errorMsg)

	# def test_verifyNRIC_rejectsOrganisationUserNRIC(self):
	# 	errorMsg = "Organisation user's NRIC provided, expected False but returned True"
	# 	result = self.controller.verifyNRIC("S3999")
	# 	self.assertFalse(result, errorMsg)
	
	# def test_verifyNRIC_rejectsInvalidNRIC(self):
	# 	errorMsg = "Invalid NRIC provided, expected False but returned True"
	# 	result = self.controller.verifyNRIC("invalidNRIC")
	# 	self.assertFalse(result, errorMsg)

	# def test_verifyNRIC_rejectsBlankNRIC(self):
	# 	errorMsg = "Blank NRIC provided, expected False but returned True"
	# 	result = self.controller.verifyNRIC("")
	# 	self.assertFalse(result, errorMsg)

	# ----------------------------------------------------
	#					Test sendAlert method
	# ----------------------------------------------------

	# Test with correct value
	def test_sendAlert_acceptCorrectValues(self):
		errorMsg = "Correct values provided, expected return value of 0 was not received"
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case with correct values", "S1999")
		self.assertEqual(result, 0, errorMsg)

	# Test with incorrect RECIPIENT values
	def test_sendAlert_rejectBlankRecipient(self):
		errorMsg = "No recipient provided, expected return value of 1 was not received"
		result = self.controller.sendAlert("", "Message from CONTROLLER test case without recipient NRIC", "S1999")
		self.assertEqual(result, 1, errorMsg)

	def test_sendAlert_rejectInvalidRecipient(self):
		errorMsg = "Invalid NRIC provided, expected return value of 1 was not received"
		result = self.controller.sendAlert("invalidNRIC", "Message from CONTROLLER test case with incorrect NRIC", "S1999")
		self.assertEqual(result, 1, errorMsg)

	def test_sendAlert_rejectBusinessRecipient(self):
		errorMsg = "Business User's NRIC provided as recipient, expected return value of 1 was not received"
		result = self.controller.sendAlert("S2999", "Message from CONTROLLER test case with business user's NRIC as recipient", "S1999")
		self.assertEqual(result, 1, errorMsg)
	
	def test_sendAlert_rejectHealthStaffRecipient(self):
		errorMsg = "Health Staff User's NRIC provided as recipient, expected return value of 1 was not received"
		result = self.controller.sendAlert("S1999", "Message from CONTROLLER test case with health staff user's NRIC as recipient", "S1999")
		self.assertEqual(result, 1, errorMsg)

	def test_sendAlert_rejectOrganisationRecipient(self):
		errorMsg = "Organisation User's NRIC provided as recipient, expected return value of 1 was not received"
		result = self.controller.sendAlert("S1999", "Message from CONTROLLER test case with organisation user's NRIC as recipient", "S1999")
		self.assertEqual(result, 1, errorMsg)
	

	# Test with incorrect MESSAGE values
	def test_sendAlert_rejectBlankMessage(self):
		errorMsg = "No alert message provided, expected return value of 2 was not received"
		result = self.controller.sendAlert("S0999", "", "S1999")
		self.assertEqual(result, 2, errorMsg)

	# Test with incorrect SENDER values
	def test_sendAlert_rejectBlankSender(self):
		errorMsg = "No sender NRIC provided, expected return value of 2 was not received"
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case without sender NRIC", "")
		self.assertEqual(result, 2, errorMsg)

	def test_sendAlert_rejectInvalidSender(self):
		errorMsg = "Invalid NRIC provided, expected return value of 2 was not received"
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case with invalid NRIC", "InvalidNRIC")
		self.assertEqual(result, 2, errorMsg)

	def test_sendAlert_rejectPublicUserAsSender(self):
		errorMsg = "Public User's NRIC provided as sender, expected return value of 2 was not received"
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case by sent by public user", "S0999")
		self.assertEqual(result, 2, errorMsg)

	def test_sendAlert_rejectBusinessUserAsSender(self):
		errorMsg = "Business User's NRIC provided as sender, expected return value of 2 was not received"
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case by sent by business user", "S2999")
		self.assertEqual(result, 2, errorMsg)
	
	def test_sendAlert_rejectOrganisationUserAsSender(self):
		errorMsg = "Organisation User's NRIC provided as sender, expected return value of 2 was not received"
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case by sent by organisation user", "S3999")
		self.assertEqual(result, 2, errorMsg)

if __name__ == '__main__':
	unittest.main(verbosity=2)