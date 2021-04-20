from entity import Person, BusinessUser, HealthStaffUser, OrganisationUser
from random import randrange, randint

#16 ^ 3  = 4096 names / accounts
firstName = ['Addison', 'Bowie', 'Carter', 'Drew', 'Eden', 'Finn', 'Gabriel', 'Hayden', 'Jamie', 'Jules', 'Ripley', 'Skylar', 'Ashton', 'Caelan', 'Flynn', 'Kaden']
middleName = ['Angel', 'Asa', 'Bay', 'Blue', 'Cameron', 'Gray', 'Lee', 'Quinn', 'Rue', 'Tate', 'Banks', 'Quince', 'Finley', 'Shea', 'Pace', 'James']
lastName = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Wilson', 'Taylor', 'Moore', 'White', 'Anderson', 'Rodriguez', 'Lopez', 'Walker']
gender = ['M', 'F']

businessID = range(1, 10)

publicUsers = []
businessUsers = []
healthUsers = []
organisationUsers = []


def populateDatabase():
    count = 0
    licenceNo = 10000000


    # Check Number of names
    print('Number of First Names: ' + str(len(firstName)))
    print('Number of Middle Names: ' + str(len(middleName)))
    print('Number of Last Names: ' + str(len(lastName)))

    # Check if any repeated
    fullnamelist = firstName + middleName + lastName
    print('Duplicate Names: ' + str(any(fullnamelist.count(x) > 1 for x in fullnamelist)))

    # Generate Users
    for x in firstName:
        for y in middleName:
            for z in lastName:
                count += 1

                # Generate NRIC
                NRIC = 'S'+ '{:04d}'.format(count)

                # Generate a random usertype
                type = randrange(4)
                mobile = randrange(90000000, 99999999)
                random_gender = randint(0,len(gender)-1)

                # Generate a public user
                if type == 0:
                    publicUsers.append(Person(NRIC, x, y, z, mobile, gender[random_gender]))

                # Generate a business user
                elif type == 1:
                    random_businessID = randint(0,len(businessID)-1)
                    businessUsers.append(BusinessUser(NRIC, x, y, z, mobile, gender[random_gender], businessID[random_businessID]))

                # Generate a health user
                elif type == 2:
                    licenceNo += 1
                    healthUsers.append(HealthStaffUser(NRIC, x, y, z, mobile, gender[random_gender], licenceNo))

                # Generate a organisation user
                else:
                    organisationUsers.append(OrganisationUser(NRIC, x, y, z, mobile, gender[random_gender], 1))

    print('Total unique names generated = ' + str(count))
    print(len(publicUsers))
    print(len(businessUsers))
    print(len(healthUsers))
    print(len(organisationUsers))

    

    

populateDatabase()