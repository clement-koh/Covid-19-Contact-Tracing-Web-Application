from ..entities import User, Business, BusinessUser, Alert, Location
from datetime import datetime
from flask import session

class healthStaffUser_SendAlertController:
    @staticmethod
    def getUserSearchDetails():
        # Get search result
        results = User.getAllUser()

        # Format the result
        adjustedResult = []
        for result in results:
            adjustedResult.append(result.NRIC)
        return adjustedResult

    @staticmethod
    def getBusinessSearchDetails():
        # Get search result
        results = Business.getAllBusiness()

        # Format the result
        adjustedResult = []
        for result in results:
            adjustedResult.append(result.name)
        return adjustedResult

    @staticmethod
    def newAlert(category, recipient, message):
        # Check if recipient exists
        if ((category == 'public' and not User.hasRecord(recipient)) or 
            (category == 'business' and Business.getID(recipient) is None)):
            # if addition is unsuccessful
            flashMessage = 'Recipient ({}) does not exist'.format(recipient)
            return (False, flashMessage)
        
        print('Recipient Exist')

        if category == 'public':
            # Add record to database
            result = Alert.addRecord(sent_by=session['user'],
                                     alert_type='public',
                                     recipient_NRIC=recipient,
                                     message=message)

            # If addition is successful
            if result is not None:
                flashMessage = """Your alert message has been successfully 
                                  delivered to {}!""".format(recipient)
                return (True, flashMessage)

            flashMessage = 'Error generating alert. Please check value entered'
            return (False, flashMessage)

        if category == 'business':
            count = 0
            alert_type = 'Business: {}'.format(recipient)
            
            # Get all business users
            businessUser = BusinessUser.getUsers(recipient)

            for user in businessUser:
                result = Alert.addRecord(sent_by=session['user'],
                                         alert_type=alert_type,
                                         recipient_NRIC=user.NRIC,
                                         message=message)
                count += 1
            
            flashMessage = """Your alert message has been successfully 
                              delivered to {} users in {}!""".format(count, recipient)
            return (True, flashMessage)

        # Invalid Option
        return(False, 'Invalid Option Detected')