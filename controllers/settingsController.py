from ..entities import User, Business, BusinessUser, Alert
from datetime import datetime
from flask import session

class settingsController:
    @staticmethod
    def updatePassword(currentpassword,password):

        #check if NRIC Exist
        if ((not User.hasRecord(NRIC = session['user']))):

            
            # if not Valid NRIC
            flashMessage = 'NRIC ({}) does not exist'.format(NRIC)
            return (False, flashMessage)
        
        print('NRIC Exist')
        currentpasswords = User.checkpasswords(NRIC = session['user'])
        
        #check current password
        if (currentpassword != currentpasswords):

            # if not Valid current password
            flashMessage = 'Error, current password not match'
            return (False, flashMessage)

        else:
      
            # update password record to database
            result = User.updatePassword(NRIC = session['user'], password = password)

            # If addition is successful
            if result is not None:
                flashMessage = 'Your Password has been updated successfully'
                return (True, flashMessage)

            flashMessage = 'Error generating Updating Password. Please check value entered'
            return (False, flashMessage)
            
   