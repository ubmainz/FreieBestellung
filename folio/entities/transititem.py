#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from folio.entities.item import Item
from folio.exceptions import ItemException
import json

class TransitItem(Item):
    """The class TransitItem expands the Item class with further fields to receive an Item
    from FOLIO that is in transition mode.
    """

    def __init__(self, item = {}):
        super().__init__(item)
        self.__inTransitDestinationServicePointId, = item["inTransitDestinationServicePointId"] if "inTransitDestinationServicePointId" in item else ""
        self.__lastCheckIn_servicePointId =          item["lastCheckIn"]["servicePointId"]      if "lastCheckIn"                        in item and "servicePointId"   in item["lastCheckIn"] else ""
        self.__lastCheckIn_staffMemberId =           item["lastCheckIn"]["staffMemberId"]       if "lastCheckIn"                        in item and "staffMemberId"    in item["lastCheckIn"] else ""
        self.__lastCheckIn_dateTime =                item["lastCheckIn"]["dateTime"]            if "lastCheckIn"                        in item and "dateTime"         in item["lastCheckIn"] else ""

    def check_required(self):
        return super().check_required() # and \
            # place further fields here, if necessary

    @property
    def data(self):
        return super().data | {
            "inTransitDestinationServicePointId": self.__inTransitDestinationServicePointId,
            "lastCheckIn": {
                "servicePointId": self.__lastCheckIn_servicePointId,
                "staffMemberId": self.__lastCheckIn_staffMemberId,
                "dateTime": self.__lastCheckIn_dateTime
            }
        }

    @property
    def creation_data(self):
        if self.check_required():
            return super().creation_data | {
                "inTransitDestinationServicePointId": self.__inTransitDestinationServicePointId,
                "lastCheckIn": {
                    "servicePointId": self.__lastCheckIn_servicePointId,
                    "staffMemberId": self.__lastCheckIn_staffMemberId,
                    "dateTime": self.__lastCheckIn_dateTime
                }
            }
        else:
            raise ItemException(self.data)

    #
    # Operator overload
    #

    def __repr__(self):
        return "Class " + __name__ + ".TransitItem:\n" + json.dumps(self.data, indent=2)

    #
    # Getter methods
    #

    @property
    def inTransitDestinationServicePointId(self):
        return self.__inTransitDestinationServicePointId

    @property
    def lastCheckIn_servicePointId(self):
        return self.__lastCheckIn_servicePointId

    @property
    def lastCheckIn_staffMemberId(self):
        return self.__lastCheckIn_staffMemberId

    @property
    def lastCheckIn_dateTime(self):
        return self.__lastCheckIn_dateTime

    #
    # Setter methods
    #

    @inTransitDestinationServicePointId.setter
    def inTransitDestinationServicePointId(self, value):
        self.__inTransitDestinationServicePointId = value

    @lastCheckIn_servicePointId.setter
    def lastCheckIn_servicePointId(self, value):
        self.__lastCheckIn_servicePointId = value

    @lastCheckIn_staffMemberId.setter
    def lastCheckIn_staffMemberId(self, value):
        self.__lastCheckIn_staffMemberId = value

    @lastCheckIn_dateTime.setter
    def lastCheckIn_dateTime(self, value):
        self.__lastCheckIn_dateTime = value
