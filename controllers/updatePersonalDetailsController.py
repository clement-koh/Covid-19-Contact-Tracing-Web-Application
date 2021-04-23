from ..entities import User, Business, BusinessUser, Alert
from datetime import datetime
from flask import session


class updatePersonalDetailsController:
    @staticmethod
    def updateRecord(mobile):

        #check if NRIC Exist
        if ((not User.hasRecord(NRIC = session['user']))):

            
            # if not Valid NRIC
            flashMessage = 'NRIC ({}) does not exist'.format(NRIC)
            return (False, flashMessage)
        
        print('NRIC Exist')

      
        # update record to database
        result = User.updateRecord(NRIC = session['user'], mobile = mobile)

        # If addition is successful
        if result is not None:
            flashMessage = 'Your Personal info has been updated successfully'
            return (True, flashMessage)

        flashMessage = 'Error generating Updating Personal Record. Please check value entered'
        return (False, flashMessage)
        
    # get first name
    @staticmethod
    def getFirstName():
        result = User.getFirstName(NRIC = session['user'])
        return result

    # get last name
    @staticmethod
    def getLastName():
        result = User.getLastName(NRIC = session['user'])
        return result

    # get mobile
    @staticmethod
    def getMobile():
        result = User.getMobile(NRIC = session['user'])
        return result