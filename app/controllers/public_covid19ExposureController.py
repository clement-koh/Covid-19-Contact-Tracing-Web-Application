from flask import session

class public_covid19ExposureController:
	@staticmethod
	def getCovid19ExposureStatus():
		NRIC = session['user'];