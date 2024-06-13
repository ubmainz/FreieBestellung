#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from folio.entities.foliorequest import FOLIORequest
from folio.exceptions import RequestException
from folio.values.barcode import Barcode
from folio.types import EmptyString, Today
import json

class Request(FOLIORequest):
    """The Request class extends the FOLIORequest class with data to generate a JSON string 
    for creation of a new request (Bestandsanfrage/Ausleihe) in FOLIO.
    The result of that creation process will be saved in the class NewRequest.
    """

    def __init__(self, request = {}):
        super().__init__(request)
        self.__requester_barcode =                request["requester"]["barcode"]            if "requester"            in request and  "barcode"          in request["requester"] else ""
        self.__requester_lastname =               request["requester"]["lastName"]           if "requester"            in request and  "lastName"         in request["requester"] else "" 
        self.__requester_firstname =              request["requester"]["firstName"]          if "requester"            in request and  "firstName"        in request["requester"] else ""
        self.__instance_title =                   request["instance"]["title"]               if "instance"             in request and  "title"            in request["instance"] else ""
        self.__instance_identifiers =             request["instance"]["identifiers"]         if "instance"             in request and  "identifiers"      in request["instance"] else []
        self.__instance_contributorNames =        request["instance"]["contributorNames"]    if "instance"             in request and  "contributorNames" in request["instance"] else []
        self.__instance_publication =             request["instance"]["publication"]         if "instance"             in request and  "publication"      in request["instance"] else []
        self.__holdingsRecordId =                 request["holdingsRecordId"]                if "holdingsRecordId"     in request else ""
        self.__itemId =                           request["itemId"]                          if "itemId"               in request else ""
        self.__position =                         request["position"]                        if "position"             in request else 1
        self.__pickupServicePointId =             request["pickupServicePointId"]            if "pickupServicePointId" in request else ""
        self.__searchindex_pickupServicePointId = request["searchIndex"]["pickupServicePointName"] if "searchIndex"    in request and  "pickupServicePointName" in request["searchIndex"] else ""

    def check_required(self):
        return super().check_required() and not \
            EmptyString()(self.__instance_title) and \
            Barcode()(self.__requester_barcode)  and \
            Today()(super().requestDate) # and \
            # place further field comparsion here, if needed

    @property
    def data(self):
        return super().data | {
            "requester": {
                "barcode": self.__requester_barcode,
                "lastName": self.__requester_lastname,
                "firstName": self.__requester_firstname
            },
            "instance": {
                "title": self.__instance_title,
                "identifiers": self.__instance_identifiers,
                "contributorNames": self.__instance_contributorNames,
                "publication": self.__instance_publication,
            },
            "holdingsRecordId": self.__holdingsRecordId,
            "itemId": self.__itemId,
            "position": self.__position,
            "pickupServicePointId": self.__pickupServicePointId,
            "searchIndex": {
                "pickupServicePointName": self.__searchindex_pickupServicePointId
            }
        }

    @property
    def creation_data(self):
        if self.check_required():
            return super().creation_data | {
                "requester": {
                    "barcode": self.__requester_barcode,
                    "lastName": self.__requester_lastname,
                    "firstName": self.__requester_firstname
                },
                "instance": {
                    "title": self.__instance_title,
                    "identifiers": []
                },
                "holdingsRecordId": self.__holdingsRecordId,
                "itemId": self.__itemId,
                "position": self.__position,
                "pickupServicePointId": self.__pickupServicePointId
            }
        else:
            raise RequestException(self.data)

    #
    # Operator overload
    #

    def __repr__(self):
        return "Class " + __name__ + ".Request:\n" + json.dumps(self.data, indent=2)

    #
    # Getter methods
    #

    @property
    def requester_barcode(self):
        return self.__requester_barcode

    @property
    def requester_lastname(self):
        return self.__requester_lastname

    @property
    def requester_firstname(self):
        return self.__requester_firstname

    @property
    def instance_title(self):
        return self.__instance_title

    @property
    def instance_identifiers(self):
        return self.__instance_identifiers
    
    @property
    def instance_contributorNames(self):
        return self.__instance_contributorNames
    
    @property
    def instance_publication(self):
        return self.__instance_publication

    @property
    def holdingsRecordId(self):
        return self.__holdingsRecordId

    @property
    def itemId(self):
        return self.__itemId

    @property
    def position(self):
        return self.__position

    @property
    def pickupServicePointId(self):
        return self.__pickupServicePointId

    @property
    def searchindex_pickupServicePointId(self):
        return self.__searchindex_pickupServicePointId

    #
    # Setter methods
    #

    @requester_barcode.setter
    def requester_barcode(self, value):
        self.__requester_barcode = value

    @requester_lastname.setter
    def requester_lastname(self, value):
        self.__requester_lastname = value

    @requester_firstname.setter
    def requester_firstname(self, value):
        self.__requester_firstname = value

    @instance_title.setter
    def instance_title(self, value):
        self.__instance_title = value

    @instance_identifiers.setter
    def instance_identifiers(self, value):
        self.__instance_identifiers = value

    @holdingsRecordId.setter
    def holdingsRecordId(self, value):
        self.__holdingsRecordId = value

    @itemId.setter
    def itemId(self, value):
        self.__itemId = value

    @position.setter
    def position(self, value):
        self.__position = value

    @pickupServicePointId.setter
    def pickupServicePointId(self, value):
        self.__pickupServicePointId = value

    @searchindex_pickupServicePointId.setter
    def searchindex_pickupServicePointId(self, value):
        self.__searchindex_pickupServicePointId = value
