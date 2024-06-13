#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from folio.entities.request import Request
import json

class NewRequest(Request):
    """This class is used to receive a new created request from FOLIO.
    It expands the Request class with an id, the service point some metadata and much
    more data provided by FOLIO during the creation process.
    """

    def __init__(self, request = {}):
        super().__init__(request)
        self.__id =                                      request["id"]                                         if "id"                    in request else ""
        self.__requestExpirationDate =                   request["requestExpirationDate"]                      if "requestExpirationDate" in request else ""
        self.__item_location_name =                      request["item"]["location"]["name"]                   if "item"                  in request and "location"             in request["item"] and "name"        in request["item"]["location"] else ""
        self.__item_location_libraryName =               request["item"]["location"]["libraryName"]            if "item"                  in request and "location"             in request["item"] and "libraryName" in request["item"]["location"] else ""
        self.__item_location_code =                      request["item"]["location"]["code"]                   if "item"                  in request and "location"             in request["item"] and "code"        in request["item"]["location"] else ""
        self.__item_chronology =                         request["item"]["chronology"]                         if "item"                  in request and "chronology"           in request["item"]               else ""
        self.__item_status =                             request["item"]["status"]                             if "item"                  in request and "status"               in request["item"]               else ""
        self.__item_callNumber =                         request["item"]["callNumber"]                         if "item"                  in request and "callNumber"           in request["item"]               else ""
        self.__item_callNumberComponents_callNumber =    request["item"]["callNumberComponents"]["callNumber"] if "item"                  in request and "callNumberComponents" in request["item"] and "callNumber" in request["item"]["callNumberComponents"] else ""
        self.__item_callNumberComponents_prefix =        request["item"]["callNumberComponents"]["prefix"]     if "item"                  in request and "callNumberComponents" in request["item"] and "prefix"     in request["item"]["callNumberComponents"] else ""
        self.__metadata_createdDate =                    request["metadata"]["createdDate"]                    if "metadata"              in request and "createdDate"          in request["metadata"]           else ""
        self.__metadata_createdByUserId =                request["metadata"]["createdByUserId"]                if "metadata"              in request and "createdByUserId"      in request["metadata"]           else ""
        self.__metadata_updatedDate =                    request["metadata"]["updatedDate"]                    if "metadata"              in request and "updatedDate"          in request["metadata"]           else ""
        self.__metadata_updatedByUserId =                request["metadata"]["updatedByUserId"]                if "metadata"              in request and "updatedByUserId"      in request["metadata"]           else ""
        self.__pickupServicePoint_name =                 request["pickupServicePoint"]["name"]                 if "pickupServicePoint"    in request and "name"                 in request["pickupServicePoint"] else ""
        self.__pickupServicePoint_code =                 request["pickupServicePoint"]["code"]                 if "pickupServicePoint"    in request and "code"                 in request["pickupServicePoint"] else ""
        self.__pickupServicePoint_discoveryDisplayName = request["pickupServicePoint"]["discoveryDisplayName"] if "pickupServicePoint"    in request and "discoveryDisplayName" in request["pickupServicePoint"] else ""
        self.__pickupServicePoint_description =          request["pickupServicePoint"]["description"]          if "pickupServicePoint"    in request and "description"          in request["pickupServicePoint"] else None
        self.__pickupServicePoint_shelvingLagTime =      request["pickupServicePoint"]["shelvingLagTime"]      if "pickupServicePoint"    in request and "shelvingLagTime"      in request["pickupServicePoint"] else 60
        self.__pickupServicePoint_pickupLocation =       request["pickupServicePoint"]["pickupLocation"]       if "pickupServicePoint"    in request and "pickupLocation"       in request["pickupServicePoint"] else True

    @property
    def data(self):
        return super().data | {
            "id": self.__id,
            "requestExpirationDate": self.__requestExpirationDate,
            "item" : {
                    "location" : {
                        "name" : self.__item_location_name,
                        "libraryName" : self.__item_location_libraryName,
                        "code" : self.__item_location_code
                    },
                    "chronology" : self.__item_chronology,
                    "status" : self.__item_status,
                    "callNumber" : self.__item_callNumber,
                    "callNumberComponents" : {
                        "callNumber" : self.__item_callNumberComponents_callNumber,
                        "prefix" : self.__item_callNumberComponents_prefix
                    },
            },
            "metadata": {
                "createdDate": self.__metadata_createdDate,
                "createdByUserId": self.__metadata_createdByUserId,
                "updatedDate": self.__metadata_updatedDate,
                "updatedByUserId": self.__metadata_updatedByUserId
            },
            "pickupServicePoint" : {
                "name" : self.__pickupServicePoint_name,
                "code" : self.__pickupServicePoint_code,
                "discoveryDisplayName" : self.__pickupServicePoint_discoveryDisplayName,
                "description" : self.__pickupServicePoint_description,
                "shelvingLagTime" : self.__pickupServicePoint_shelvingLagTime,
                "pickupLocation" : self.__pickupServicePoint_pickupLocation
            }
        }

    #
    # Operator overload
    #

    def __repr__(self):
        return "Class " + __name__ + ".NewRequest:\n" + json.dumps(self.data, indent=2)

    #
    # Getter methods
    #

    @property
    def id(self):
        return self.__id
    
    @property
    def requestExpirationDate(self):
        return self.__requestExpirationDate

    @property
    def item_location_name(self):
        return self.__item_location_name

    @property
    def item_location_libraryName(self):
        return self.__item_location_libraryName

    @property
    def item_location_code(self):
        return self.__item_location_code

    @property
    def item_chronology(self):
        return self.__item_chronology

    @property
    def item_status(self):
        return self.__item_status

    @property
    def item_callNumber(self):
        return self.__item_callNumber

    @property
    def item_callNumberComponents_callNumber(self):
        return self.__item_callNumberComponents_callNumber

    @property
    def item_callNumberComponents_prefix(self):
        return self.__item_callNumberComponents_prefix

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
    def pickupServicePoint_name(self):
        return self.__pickupServicePoint_name

    @property
    def pickupServicePoint_code(self):
        return self.__pickupServicePoint_code

    @property
    def pickupServicePoint_discoveryDisplayName(self):
        return self.__pickupServicePoint_discoveryDisplayName

    @property
    def pickupServicePoint_description(self):
        return self.__pickupServicePoint_description

    @property
    def pickupServicePoint_shelvingLagTime(self):
        return self.__pickupServicePoint_shelvingLagTime

    @property
    def pickupServicePoint_pickupLocation(self):
        return self.__pickupServicePoint_pickupLocation
