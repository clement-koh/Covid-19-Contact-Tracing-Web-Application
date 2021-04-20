# ------------------------------------
#       Entity for 4 User Groups
# ------------------------------------
# Entity for Person
class Person:
    # Constructor
    def __init__(self, NRIC, firstName, middleName, lastName, mobile, gender):
        self.NRIC = NRIC
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.mobile = mobile
        self.gender = gender

    def __repr__(self):
        message = "{} {} {}"
        return message.format(self.firstName, self.middleName, self.lastName)
    
    # Update function to update details
    def update(self, mobile):
        self.mobile = mobile
    


# Entity for BusinessUsers
class BusinessUser(Person):
    # Constructor
    def __init__(self, NRIC, firstName, middleName, lastName, mobile, gender, businessID):
        Person.__init__(self, NRIC, firstName, middleName, lastName, mobile,  gender)
        self.businessID = businessID
    
    # Update functions to update details and business
    def update(self, mobile, businessID):
        super.update(mobile)
        self.businessID = businessID

# Entity for HealthStaffs
class HealthStaffUser(Person):
    # Constructor
    def __init__(self, NRIC, firstName, middleName, lastName, mobile, gender, LicenceNo):
        Person.__init__(self, NRIC, firstName, middleName, lastName, mobile,  gender)
        self.LicenceNo = LicenceNo

    # Uses person update function as Licence Number unlikely to change

class OrganisationUser(Person):
    # Constructor
    def __init__(self, NRIC, firstName, middleName, lastName, mobile, gender, organisationID):
        Person.__init__(self, NRIC, firstName, middleName, lastName, mobile,  gender)
        self.organisationID = organisationID
    
    # Update functions to update details and business
    def update(self, mobile, organisationID):
        super.update(mobile)
        self.organisationID = organisationID

# -----------------------------------------
#       Entity for Priviledged Users
# ------------------------------------------
# Base class for all priviledged users
class Admin:
    # Constructor
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Update password
    def update(self, password):
        self.password = password

# Entity for Business Administrator
class BusinessAdmin(Admin):
    # Constructor
    def __init__(self, username, password, businessID):
        admin.__init__(username, password)
        self.businessID = businessID

# Entity for Health Administrator
class HealthAdmin(Admin):
    # Constructor
    def __init__(self, username, password):
        admin.__init__(username, password)


# Entity for Organisation Administrator
class OrganisationAdmin(Admin):
    # Constructor
    def __init__(self, username, password, organisationID):
        admin.__init__(username, password)
        self.organisationID = organisationID