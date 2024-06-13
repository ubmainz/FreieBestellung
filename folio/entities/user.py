#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

import json

class User():
    """This class represents an user in FOLIO.
    It is not fully implemented yet. There are much more attributes for an user in FOLIO, 
    which are not used in most cases.
    """

    def __init__(self, user = {}):
        self.__username =                        user["username"]                           if "username"     in user else ""
        self.__id =                              user["id"]                                 if "id"           in user else ""
        self.__barcode =                         user["barcode"]                            if "barcode"      in user else ""
        self.__active =                          user["active"]                             if "active"       in user else True
        self.__patronGroup =                     user["patronGroup"]                        if "patronGroup"  in user else ""
        self.__departments =                     user["departments"]                        if "departments"  in user else []
        self.__proxyFor =                        user["proxyFor"]                           if "proxyFor"     in user else []
        self.__personal_lastName =               user["personal"]["lastName"]               if "personal"     in user and "lastName"               in user["personal"] else ""
        self.__personal_firstName =              user["personal"]["firstName"]              if "personal"     in user and "firstName"              in user["personal"] else ""
        self.__personal_email =                  user["personal"]["email"]                  if "personal"     in user and "email"                  in user["personal"] else ""
        self.__personal_addresses =              user["personal"]["addresses"]              if "personal"     in user and "addresses"              in user["personal"] else []
        self.__personal_preferredContactTypeId = user["personal"]["preferredContactTypeId"] if "personal"     in user and "preferredContactTypeId" in user["personal"] else ""
        self.__createdDate =                     user["createdDate"]                        if "createdDate"  in user else ""
        self.__updatedDate =                     user["updatedDate"]                        if "updatedDate"  in user else ""
        self.__metadata_createdDate =            user["metadata"]["createdDate"]            if "metadata"     in user and "createdDate"            in user["metadata"] else ""
        self.__metadata_createdByUserId =        user["metadata"]["createdByUserId"]        if "metadata"     in user and "createdByUserId"        in user["metadata"] else ""
        self.__metadata_updatedDate =            user["metadata"]["updatedDate"]            if "metadata"     in user and "updatedDate"            in user["metadata"] else ""
        self.__metadata_updatedByUserId =        user["metadata"]["updatedByUserId"]        if "metadata"     in user and "updatedByUserId"        in user["metadata"] else ""
        self.__customFields =                    user["customFields"]                       if "customFields" in user else {}

    @property
    def data(self):
        return {
            "username": self.__username,
            "id": self.__id,
            "barcode": self.__barcode,
            "active": self.__active,
            "patronGroup": self.__patronGroup,
            "departments": self.__departments,
            "proxyFor": self.__proxyFor,
            "personal": {
                "lastName": self.__personal_lastName,
                "firstName": self.__personal_firstName,
                "email": self.__personal_email,
                "addresses": self.__personal_addresses,
                "preferredContactTypeId": self.__personal_preferredContactTypeId
            },
            "createdDate": self.__createdDate,
            "updatedDate": self.__updatedDate,
            "metadata": {
                "createdDate": self.__metadata_createdDate,
                "createdByUserId": self.__metadata_createdByUserId,
                "updatedDate": self.__metadata_updatedDate,
                "updatedByUserId": self.__metadata_updatedByUserId
            },
            "customFields": self.__customFields
        }

    @property
    def json(self):
        return json.dumps(self.data)

    #
    # Operator overload
    #

    def __repr__(self):
        return "Class " + __name__ + ".User:\n" + json.dumps(self.data, indent=2)

    def __hash__(self):
        return hash(self.__id, self.__barcode, self.__personal_email)

    #
    # Getter methods
    #

    @property
    def username(self):
        return self.__username

    @property
    def id(self):
        return self.__id

    @property
    def barcode(self):
        return self.__barcode

    @property
    def active(self):
        return self.__active

    @property
    def patronGroup(self):
        return self.__patronGroup

    @property
    def departments(self):
        return self.__departments

    @property
    def proxyFor(self):
        return self.__proxyFor

    @property
    def personal_lastName(self):
        return self.__personal_lastName

    @property
    def personal_firstName(self):
        return self.__personal_firstName

    @property
    def personal_email(self):
        return self.__personal_email

    @property
    def personal_addresses(self):
        return self.__personal_addresses

    @property
    def personal_preferredContactTypeId(self):
        return self.__personal_preferredContactTypeId

    @property
    def createdDate(self):
        return self.__createdDate

    @property
    def updatedDate(self):
        return self.__updatedDate

    @property
    def metadata_createdDate(self):
        return self.__metadata_createdDate

    @property
    def metadata_createdByUserId(self):
        return self.__metadata_createdByUserId

    @property
    def metadata_updatedDate(self):
        return self.__metadata_updatedDate

    @property
    def metadata_updatedByUserId(self):
        return self.__metadata_updatedByUserId

    @property
    def customFields(self):
        return self.__customFields
    
    #
    # Setter methods
    #

    @username.setter
    def username(self, value):
        self.__username = value

    @id.setter
    def id(self, value):
        self.__id = value

    @barcode.setter
    def barcode(self, value):
        self.__barcode = value

    @active.setter
    def active(self, value):
        self.__active = value

    @patronGroup.setter
    def patronGroup(self, value):
        self.__patronGroup = value

    @departments.setter
    def departments(self, value):
        self.__departments = value

    @proxyFor.setter
    def proxyFor(self, value):
        self.__proxyFor = value

    @personal_lastName.setter
    def personal_lastName(self, value):
        self.__personal_lastName = value

    @personal_firstName.setter
    def personal_firstName(self, value):
        self.__personal_firstName = value

    @personal_email.setter
    def personal_email(self, value):
        self.__personal_email = value

    @personal_addresses.setter
    def personal_addresses(self, value):
        self.__personal_addresses = value

    @personal_preferredContactTypeId.setter
    def personal_preferredContactTypeId(self, value):
        self.__personal_preferredContactTypeId = value

    @customFields.setter
    def customFields(self, value):
        self.__customFields = value
