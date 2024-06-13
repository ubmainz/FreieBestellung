#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from folio.entities.folioitem import FOLIOItem
from folio.exceptions import ItemException
from folio.types import EmptyString
import json

class Item(FOLIOItem):
    """This class represents an Item in FOLIO.
    It is derived from FOLIOItem and is the most used entity in this request-form script.
    It is used to receive an Item from FOLIO, manipulate the data and create the JSON string for a new Item.
    """

    def __init__(self, item = {}):
        super().__init__(item)
        self.__id =                          item["id"]                             if "id"                          in item else ""
        self.__version =                     item["_version"]                       if "_version"                    in item else ""
        self.__administrativeNotes =         item["administrativeNotes"]            if "administrativeNotes"         in item else []
        self.__title =                       item["title"]                          if "title"                       in item else ""
        self.__callNumber =                  item["callNumber"]                     if "callNumber"                  in item else ""
        self.__hrid =                        item["hrid"]                           if "hrid"                        in item else ""
        self.__contributorNames =            item["contributorNames"]               if "contributorNames"            in item else []
        self.__formerIds =                   item["formerIds"]                      if "formerIds"                   in item else []
        self.__discoverySuppress =           item["discoverySuppress"]              if "discoverySuppress"           in item else False
        self.__barcode =                     item["barcode"]                        if "barcode"                     in item else ""
        self.__chronology =                  item["chronology"]                     if "chronology"                  in item else ""
        self.__itemLevelCallNumber =         item["itemLevelCallNumber"]            if "itemLevelCallNumber"         in item else ""
        self.__notes =                       item["notes"]                          if "notes"                       in item else []
        self.__circulationNotes =            item["circulationNotes"]               if "circulationNotes"            in item else []
        self.__accessionNumber =             item["accessionNumber"]                if "accessionNumber"             in item else ""
        self.__tags_tagList =                item["tags"]["tagList"]                if "tags"                        in item and "tagList"          in item["tags"] else []
        self.__yearCaption =                 item["yearCaption"]                    if "yearCaption"                 in item else []
        self.__electronicAccess =            item["electronicAccess"]               if "electronicAccess"            in item else []
        self.__statisticalCodeIds =          item["statisticalCodeIds"]             if "statisticalCodeIds"          in item else []
        self.__purchaseOrderLineIdentifier = item["purchaseOrderLineIdentifier"]    if "purchaseOrderLineIdentifier" in item else None
        self.__metadata_createdDate =        item["metadata"]["createdDate"]        if "metadata"                    in item and "createdDate"      in item["metadata"] else ""
        self.__metadata_createdByUserId =    item["metadata"]["createdByUserId"]    if "metadata"                    in item and "createdByUserId"  in item["metadata"] else ""
        self.__metadata_updatedDate =        item["metadata"]["updatedDate"]        if "metadata"                    in item and "updatedDate"      in item["metadata"] else ""
        self.__metadata_updatedByUserId =    item["metadata"]["updatedByUserId"]    if "metadata"                    in item and "updatedByUserId"  in item["metadata"] else ""
        self.__effCNComponents_callNumber =  item["effectiveCallNumberComponents"]["callNumber"] if "effectiveCallNumberComponents" in item and "callNumber" in item["effectiveCallNumberComponents"] else ""
        self.__effCNComponents_prefix =      item["effectiveCallNumberComponents"]["prefix"]     if "effectiveCallNumberComponents" in item and "prefix"     in item["effectiveCallNumberComponents"] else None
        self.__effCNComponents_suffix =      item["effectiveCallNumberComponents"]["suffix"]     if "effectiveCallNumberComponents" in item and "suffix"     in item["effectiveCallNumberComponents"] else None
        self.__effCNComponents_typeId =      item["effectiveCallNumberComponents"]["typeId"]     if "effectiveCallNumberComponents" in item and "typeId"     in item["effectiveCallNumberComponents"] else None
        self.__effectiveShelvingOrder =      item["effectiveShelvingOrder"]         if "effectiveShelvingOrder"      in item else ""
        self.__isBoundWith =                 item["isBoundWith"]                    if "isBoundWith"                 in item else False
        self.__effectiveLocation_id =        item["effectiveLocation"]["id"]        if "effectiveLocation"           in item and "id"               in item["effectiveLocation"] else ""
        self.__effectiveLocation_name =      item["effectiveLocation"]["name"]      if "effectiveLocation"           in item and "name"             in item["effectiveLocation"] else ""

    def check_required(self):
        return super().check_required() and not \
            EmptyString()(self.__chronology)

    def is_intellectual(self):
        return super().status_name == "Intellectual item" and \
               self.__effectiveLocation_name != "Dummy"

    @property
    def data(self):
        return super().data | {
            "id": self.__id,
            "_version": self.__version,
            "administrativeNotes": self.__administrativeNotes,
            "title": self.__title,
            "callNumber": self.__callNumber,
            "hrid": self.__hrid,
            "contributorNames": self.__contributorNames,
            "formerIds": self.__formerIds,
            "discoverySuppress": self.__discoverySuppress,
            "barcode": self.__barcode,
            "chronology": self.__chronology,
            "itemLevelCallNumber": self.__itemLevelCallNumber,
            "notes": self.__notes,
            "circulationNotes": self.__circulationNotes,
            "accessionNumber": self.__accessionNumber,
            "tags": {
                "tagList": self.__tags_tagList
            },
            "yearCaption": self.__yearCaption,
            "electronicAccess": self.__electronicAccess,
            "statisticalCodeIds": self.__statisticalCodeIds,
            "purchaseOrderLineIdentifier": self.__purchaseOrderLineIdentifier,
            "metadata": {
                "createdDate": self.__metadata_createdDate,
                "createdByUserId": self.__metadata_createdByUserId,
                "updatedDate": self.__metadata_updatedDate,
                "updatedByUserId": self.__metadata_updatedByUserId
            },
            "effectiveCallNumberComponents": {
                "callNumber": self.__effCNComponents_callNumber,
                "prefix": self.__effCNComponents_prefix,
                "suffix": self.__effCNComponents_suffix,
                "typeId": self.__effCNComponents_typeId
            },
            "effectiveShelvingOrder": self.__effectiveShelvingOrder,
            "isBoundWith": self.__isBoundWith,
            "effectiveLocation": {
                "id": self.__effectiveLocation_id,
                "name": self.__effectiveLocation_name
            }
        }
    
    @property
    def creation_data(self):
        if self.check_required():
            return super().creation_data | {
                "_version": self.__version,
                "administrativeNotes": self.__administrativeNotes,
                "formerIds": self.__formerIds,
                "discoverySuppress": self.__discoverySuppress,
                "chronology": self.__chronology,
                "itemLevelCallNumber": self.__itemLevelCallNumber,
                "notes": self.__notes,
                "circulationNotes": self.__circulationNotes,
                "accessionNumber": self.__accessionNumber,
                "tags": {
                    "tagList": self.__tags_tagList
                },
                "yearCaption": self.__yearCaption,
                "electronicAccess": self.__electronicAccess,
                "statisticalCodeIds": self.__statisticalCodeIds,
                "purchaseOrderLineIdentifier": self.__purchaseOrderLineIdentifier,
                "effectiveCallNumberComponents": {
                    "callNumber": self.__effCNComponents_callNumber,
                    "prefix": self.__effCNComponents_prefix,
                    "suffix": self.__effCNComponents_suffix,
                    "typeId": self.__effCNComponents_typeId
                },
                "effectiveShelvingOrder": self.__effectiveShelvingOrder
            }
        else:
            raise ItemException(self.data)

    #
    # Operator overload
    #

    def __repr__(self):
        return "Class " + __name__ + ".Item:\n" + json.dumps(self.data, indent=2)

    def __hash__(self):
        return hash(self.__id, self.__version, self.__hrid, self.__holdingsRecordId)

    #
    # Getter methods
    #

    @property
    def id(self):
        return self.__id

    @property
    def version(self):
        return self.__version

    @property
    def administrativeNotes(self):
        return self.__administrativeNotes

    @property
    def title(self):
        return self.__title

    @property
    def callNumber(self):
        return self.__callNumber

    @property
    def hrid(self):
        return self.__hrid

    @property
    def contributorNames(self):
        return self.__contributorNames

    @property
    def formerIds(self):
        return self.__formerIds

    @property
    def discoverySuppress(self):
        return self.__discoverySuppress
    
    @property
    def barcode(self):
        return self.__barcode
    
    @property
    def chronology(self):
        return self.__chronology

    @property
    def itemLevelCallNumber(self):
        return self.__itemLevelCallNumber

    @property
    def notes(self):
        return self.__notes

    @property
    def circulationNotes(self):
        return self.__circulationNotes
    
    @property
    def accessionNumber(self):
        return self.__accessionNumber

    @property
    def tags_tagList(self):
        return self.__tags_tagList

    @property
    def yearCaption(self):
        return self.__yearCaption

    @property
    def electronicAccess(self):
        return self.__electronicAccess

    @property
    def statisticalCodeIds(self):
        return self.__statisticalCodeIds

    @property
    def purchaseOrderLineIdentifier(self):
        return self.__purchaseOrderLineIdentifier

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
    def effectiveCallNumberComponents_callNumber(self):
        return self.__effCNComponents_callNumber

    @property
    def effectiveCallNumberComponents_prefix(self):
        return self.__effCNComponents_prefix

    @property
    def effectiveCallNumberComponents_suffix(self):
        return self.__effCNComponents_suffix

    @property
    def effectiveCallNumberComponents_typeId(self):
        return self.__effCNComponents_typeId

    @property
    def effectiveShelvingOrder(self):
        return self.__effectiveShelvingOrder

    @property
    def isBoundWith(self):
        return self.__isBoundWith

    @property
    def effectiveLocation_id(self):
        return self.__effectiveLocation_id

    @property
    def effectiveLocation_name(self):
        return self.__effectiveLocation_name

    #
    # Setter methods
    #

    @version.setter
    def version(self, value):
        self.__version = value

    @administrativeNotes.setter
    def administrativeNotes(self, value):
        self.__administrativeNotes = value

    @formerIds.setter
    def formerIds(self, value):
        self.__formerIds = value

    @discoverySuppress.setter
    def discoverySuppress(self, value):
        self.__discoverySuppress = value

    @barcode.setter
    def barcode(self, value):
        self.__barcode = value

    @chronology.setter
    def chronology(self, value):
        self.__chronology = value

    @itemLevelCallNumber.setter
    def itemLevelCallNumber(self, value):
        self.__itemLevelCallNumber = value

    @notes.setter
    def notes(self, value):
        self.__notes = value

    @circulationNotes.setter
    def circulationNotes(self, value):
        self.__circulationNotes = value

    @accessionNumber.setter
    def accessionNumber(self, value):
        self.__accessionNumber = value

    @tags_tagList.setter
    def tags_tagList(self, value):
        self.__tags_tagList = value

    @yearCaption.setter
    def yearCaption(self, value):
        self.__yearCaption = value

    @electronicAccess.setter
    def electronicAccess(self, value):
        self.__electronicAccess = value

    @statisticalCodeIds.setter
    def statisticalCodeIds(self, value):
        self.__statisticalCodeIds = value

    @purchaseOrderLineIdentifier.setter
    def purchaseOrderLineIdentifier(self, value):
        self.__purchaseOrderLineIdentifier = value

    @effectiveCallNumberComponents_callNumber.setter
    def effectiveCallNumberComponents_callNumber(self, value):
        self.__effCNComponents_callNumber = value

    @effectiveCallNumberComponents_prefix.setter
    def effectiveCallNumberComponents_prefix(self, value):
        self.__effCNComponents_prefix = value

    @effectiveCallNumberComponents_suffix.setter
    def effectiveCallNumberComponents_suffix(self, value):
        self.__effCNComponents_suffix = value

    @effectiveCallNumberComponents_typeId.setter
    def effectiveCallNumberComponents_typeId(self, value):
        self.__effCNComponents_typeId = value

    @effectiveShelvingOrder.setter
    def effectiveShelvingOrder(self, value):
        self.__effectiveShelvingOrder = value

    @isBoundWith.setter
    def isBoundWith(self, value):
        self.__isBoundWith = value

    @effectiveLocation_id.setter
    def effectiveLocation_id(self, value):
        self.__effectiveLocation_id = value

    @effectiveLocation_name.setter
    def effectiveLocation_name(self, value):
        self.__effectiveLocation_name = value
