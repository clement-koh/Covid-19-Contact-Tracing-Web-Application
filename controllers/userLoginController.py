from ..entities import User, BusinessUser, HealthStaffUser, OrganisationUser
from functools import wraps
from flask import session, redirect

# Controller used to manage user login functions
class userLoginController:
    # Returns true/false to show success/failure of login
    # Provide with
    @classmethod
    def login(cls, username, password):
        # Check if user exists
        username = username.upper()
        if User.verifyUser(username, password):
            # Check if user account is active
            if User.getAccountStatus(username):
                session['authenticated'] = True
                session['user'] = username
                session['userType'] = cls.__getUserType(username)
                return (True,)

            # If user account is suspended
            return (False, "Account has been suspended")
        
        # If user does not exsit
        return (False, "Username or password is incorrect")

    # Logs the current user out
    @staticmethod
    def logout():
        session['authenticated'] = False
        session['user'] = None
        session['userType'] = None

    # Check the account type of the user
    @staticmethod
    def __getUserType(username):
        if BusinessUser.verifyUser(username):
            return 'Business'
        elif HealthStaffUser.verifyUser(username):
            return 'Health Staff'
        elif OrganisationUser.verifyUser(username):
            return 'Organisation'
        return "Public"
    
    # Check if the user is currently logged in
    @staticmethod
    def isAuthenticated():
        try:
            return session['authenticated']
        except:
            session['authenticated'] = False
            return session['authenticated']

    # Get the type of user that is currently logged in
    @staticmethod
    def getUserType():
        return session['userType']

    # Makes a page unaccessable to those who are not logged in
    # Redirect to login page if user is not logged in
    @staticmethod
    def loginRequired(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if userLoginController.isAuthenticated():
                print("User authenticated")
                print(session['userType'])
                return function()
            else:
                print("User not authenticated")
                return redirect('/login')
        
        return decorated_function