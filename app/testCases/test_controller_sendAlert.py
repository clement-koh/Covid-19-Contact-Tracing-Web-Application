from ..controllers.HealthStaffUser_SendAlertPublicController import HealthStaffUser_SendAlertPublicController
from flask import Flask, session, render_template, redirect
import os

import unittest

class testCases_HealthStaffUser_SendAlertPublicController(unittest.TestCase):
	def setUp(self):
		# Create boundary object
		self.controller = HealthStaffUser_SendAlertPublicController()

	def test_verifyNRIC_acceptsPublicNRIC(self):
		result = self.controller.verifyNRIC("S0999")
		self.assertTrue(result, "Public user's NRIC provided, expected True but returned False")
	
	def test_verifyNRIC_rejectsHealthStaffUserNRIC(self):
		result = self.controller.verifyNRIC("S1999")
		self.assertFalse(result, "Health Staff user's NRIC provided, expected False but returned True")

	def test_verifyNRIC_rejectsBusinessUserNRIC(self):
		result = self.controller.verifyNRIC("S2999")
		self.assertFalse(result, "Business user's NRIC provided, expected False but returned True")

	def test_verifyNRIC_rejectsOrganisationUserNRIC(self):
		result = self.controller.verifyNRIC("S3999")
		self.assertFalse(result, "Organisation user's NRIC provided, expected False but returned True")
	
	def test_verifyNRIC_rejectsInvalidNRIC(self):
		result = self.controller.verifyNRIC("invalidNRIC")
		self.assertFalse(result, "Invalid NRIC provided, expected False but returned True")

	def test_verifyNRIC_rejectsBlankNRIC(self):
		result = self.controller.verifyNRIC("")
		self.assertFalse(result, "Blank NRIC provided, expected False but returned True")

	def test_sendAlert_acceptCorrectValues(self):
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case with correct values", "S1999")
		self.assertTrue(result, "Correct values provided, expected True but returned False")

	def test_sendAlert_rejectBlankRecipient(self):
		result = self.controller.sendAlert("", "Message from CONTROLLER test case without recipient NRIC", "S1999")
		self.assertFalse(result, "Invalid NRIC provided, expected False but returned True")

	def test_sendAlert_rejectInvalidRecipient(self):
		result = self.controller.sendAlert("invalidNRIC", "Message from CONTROLLER test case with incorrect NRIC", "S1999")
		self.assertFalse(result, "Invalid NRIC provided, expected False but returned True")

	def test_sendAlert_rejectBlankMessage(self):
		result = self.controller.sendAlert("S0999", "", "S1999")
		self.assertFalse(result, "No alert message provided, expected False but returned True")

	def test_sendAlert_rejectBlankSender(self):
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case without sender NRIC", "")
		self.assertFalse(result, "No sender NRIC provided, expected False but returned True")

	def test_sendAlert_rejectInvalidSender(self):
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case with invalid NRIC", "InvalidNRIC")
		self.assertFalse(result, "Invalid NRIC provided, expected False but returned True")

	def test_sendAlert_rejectPublicUserAsSender(self):
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case by sent by public user", "S0999")
		self.assertFalse(result, "Public User's NRIC provided as sender, expected False but returned True")

	def test_sendAlert_rejectBusinessUserAsSender(self):
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case by sent by business user", "S2999")
		self.assertFalse(result, "Business User's NRIC provided as sender, expected False but returned True")
	
	def test_sendAlert_rejectOrganisationUserAsSender(self):
		result = self.controller.sendAlert("S0999", "Message from CONTROLLER test case by sent by organisation user", "S3999")
		self.assertFalse(result, "Organisation User's NRIC provided as sender, expected False but returned True")

if __name__ == '__main__':
	unittest.main(verbosity=2)