#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from folio.types import UUID, FOLIOItemStatus
from folio.exceptions import ItemException
import json

class FOLIOItem():
    """The base class for FOLIO items.
    This class provides all required(!) fields and functions for an FOLIO item.
    Inherit all other FOLIO item classes from this class!

    required: {
        "status": { 
            "name": Enum => FOLIOItemStatus
        }
        "holdingsRecordId": UUID
        "materialTypeId": UUID
        "permanentLoanTypeId": UUID
    }
    """

    def __init__(self, item = {}):
        self.__status_name =            item["status"]["name"]            if "status"            in item and "name" in item["status"] and FOLIOItemStatus()(item["status"]["name"]) else FOLIOItemStatus().default
        self.__status_date =            item["status"]["date"]            if "status"            in item and "date" in item["status"] else ""
        self.__holdingsRecordId =       item["holdingsRecordId"]          if "holdingsRecordId"  in item else ""
        self.__materialType_id =        item["materialType"]["id"]        if "materialType"      in item and "id"   in item["materialType"] else ""
        self.__materialType_name =      item["materialType"]["name"]      if "materialType"      in item and "name" in item["materialType"] else ""
        self.__permanentLoanType_id =   item["permanentLoanType"]["id"]   if "permanentLoanType" in item and "id"   in item["permanentLoanType"] else ""
        self.__permanentLoanType_name = item["permanentLoanType"]["name"] if "permanentLoanType" in item and "name" in item["permanentLoanType"] else ""

    def check_required(self):
        return FOLIOItemStatus()(self.__status_name) and \
               UUID()(self.__holdingsRecordId) and \
               UUID()(self.__materialType_id) and \
               UUID()(self.__permanentLoanType_id)

    @property
    def data(self):
        return {
            "status": {
                "name": self.__status_name,
                "date": self.__status_date
            },
            "holdingsRecordId": self.__holdingsRecordId,
            "materialType": {
                "id": self.__materialType_id,
                "name": self.__materialType_name
            },
            "permanentLoanType": {
                "id": self.__permanentLoanType_id,
                "name": self.__permanentLoanType_name
            }
        }

    @property
    def json(self):
        return json.dumps(self.data)

    @property
    def creation_data(self):
        if self.check_required():
            return {
                "status": {
                    "name": self.__status_name
                },
                "holdingsRecordId": self.__holdingsRecordId,
                "materialTypeId": self.__materialType_id,
                "permanentLoanTypeId": self.__permanentLoanType_id
            }
        else:
            raise ItemException(self.data)

    @property
    def creation_json(self):
        return json.dumps(self.creation_data)

    #
    # Operator overload
    #

    def __str__(self):
        return json.dumps(self.data, indent=2)

    def __repr__(self):
        return "Class " + __name__ + ".FOLIOItem:\n" + json.dumps(self.data, indent=2)

    def __hash__(self):
        return hash(self.__status_name, self.__status_date, self.__holdingsRecordId, self.__materialType_id, self.__permanentLoanType_id)

    #
    # Getter methods
    #

    @property
    def status_name(self):
        return self.__status_name

    @property
    def status_date(self):
        return self.__status_date

    @property
    def holdingsRecordId(self):
        return self.__holdingsRecordId

    @property
    def materialType_id(self):
        return self.__materialType_id
    
    @property
    def materialType_name(self):
        return self.__materialType_name

    @property
    def permanentLoanType_id(self):
        return self.__permanentLoanType_id

    @property
    def permanentLoanType_name(self):
        return self.__permanentLoanType_name

    #
    # Setter methods
    #

    @status_name.setter
    def status_name(self, value):
        self.__status_name = value

    @holdingsRecordId.setter
    def holdingsRecordId(self, value):
        self.__holdingsRecordId = value

    @materialType_id.setter
    def materialType_id(self, value):
        self.__materialType_id = value

    @permanentLoanType_id.setter
    def permanentLoanType_id(self, value):
        self.__permanentLoanType_id = value
