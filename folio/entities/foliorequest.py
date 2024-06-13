#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from folio.types import DateTime, UUID, FOLIOID, FOLIORequestType, FOLIORequestStatus, FOLIORequestLevel, FOLIOFulfillmentPreference
from folio.exceptions import RequestException
import datetime
import json

class FOLIORequest():
    """The base class for FOLIO requests (Bestandsanfragen/Ausleihe).
    This class provides all required(!) fields and functions for an FOLIO request.
    Inherit all other FOLIO request classes from this class!

    required: {
        "instanceId", FOLIOID()
        "requesterId", UUID()
        "requestType", Enum => FOLIORequestType()
        "requestLevel", Enum => FOLIORequestLevel()
        "requestDate", String (date-time)
        "fulfillmentPreference", Enum => FOLIOFulfillmentPreference()
        "status" Enum => FOLIORequestStatus()
    }
    """

    def __init__(self, request = {}):
        self.__instanceId =             request["instanceId"]            if "instanceId"            in request else ""
        self.__requesterId =            request["requesterId"]           if "requesterId"           in request else ""
        self.__requestType =            request["requestType"]           if "requestType"           in request and FOLIORequestType()(request["requestType"])   else FOLIORequestType().default
        self.__requestLevel =           request["requestLevel"]          if "requestLevel"          in request and FOLIORequestLevel()(request["requestLevel"]) else FOLIORequestLevel().default
        self.__requestDate =            request["requestDate"]           if "requestDate"           in request and DateTime()(request["requestDate"])           else datetime.datetime.now().isoformat()
        self.__fulfillmentPreference =  request["fulfillmentPreference"] if "fulfillmentPreference" in request and FOLIOFulfillmentPreference()(request["fulfillmentPreference"]) else FOLIOFulfillmentPreference().default
        self.__status =                 request["status"]                if "status"                in request and FOLIORequestStatus()(request["status"])      else FOLIORequestStatus().default

    def check_required(self):
        return FOLIOID()(self.__instanceId) and \
               UUID()(self.__requesterId) and \
               FOLIORequestType()(self.__requestType) and \
               FOLIORequestLevel()(self.__requestLevel) and \
               DateTime()(self.__requestDate) and \
               FOLIOFulfillmentPreference()(self.__fulfillmentPreference) and \
               FOLIORequestStatus()(self.__status)

    @property
    def data(self):
        return {
            "instanceId": self.__instanceId,
            "requesterId": self.__requesterId,
            "requestType": self.__requestType,
            "requestLevel": self.__requestLevel,
            "requestDate": self.__requestDate,
            "fulfillmentPreference": self.__fulfillmentPreference,
            "status": self.__status
        }

    @property
    def json(self):
        return json.dumps(self.data)

    @property
    def creation_data(self):
        if self.check_required():
            return {
                "instanceId": self.__instanceId,
                "requesterId": self.__requesterId,
                "requestType": self.__requestType,
                "requestLevel": self.__requestLevel,
                "requestDate": self.__requestDate + "+01:00",
                "fulfillmentPreference": self.__fulfillmentPreference,
                "status": self.__status
            }
        else:
            raise RequestException(self.data)

    @property
    def creation_json(self):
        return json.dumps(self.creation_data)

    #
    # Operator overload
    #

    def __str__(self):
        return json.dumps(self.data, indent=2)

    def __repr__(self):
        return "Class " + __name__ + ".FOLIORequest:\n" + json.dumps(self.data, indent=2)

    def __hash__(self):
        return hash(self.__status, self.__instanceId, self.__requesterId, self.__requestType, self.__requestLevel, self.__requestDate)

    #
    # Getter methods
    #

    @property
    def instanceId(self):
        return self.__instanceId

    @property
    def requesterId(self):
        return self.__requesterId

    @property
    def requestType(self):
        return self.__requestType
    
    @property
    def requestLevel(self):
        return self.__requestLevel

    @property
    def requestDate(self):
        return self.__requestDate

    @property
    def fulfillmentPreference(self):
        return self.__fulfillmentPreference

    @property
    def status(self):
        return self.__status

    #
    # Setter methods
    #

    @instanceId.setter
    def instanceId(self, value):
        self.__instanceId = value

    @requesterId.setter
    def requesterId(self, value):
        self.__requesterId = value

    @requestType.setter
    def requestType(self, value):
        self.__requestType = value

    @requestLevel.setter
    def requestLevel(self, value):
        self.__requestLevel = value

    @requestDate.setter
    def requestDate(self, value):
        self.__requestDate = value

    @fulfillmentPreference.setter
    def fulfillmentPreference(self, value):
        self.__fulfillmentPreference = value

    @status.setter
    def status(self, value):
        self.__status = value
