#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from markupsafe import escape
import json

###
# Exception handling for API communication
###

#
# Connection Errors
#

class ConnectionException(Exception):
    def __init__(self, error):
        super().__init__(error)

    def __str__(self):
        return "Anmeldung am Bibliothekssystem fehlgeschlagen. (Fehler: " + json.dumps(self.args[0]) + "):"

#
# All unhandled HTTP Errors
#

class HTTPException(Exception):
    def __init__(self, error_code):
        super().__init__(error_code)

    def __str__(self):
        return "Es gibt ein Problem mit der Verbindung zu FOLIO: HTTP " + str(self.args[0])

    @property
    def data(self):
        return {"status_code":self.args[0]}

#
# Error messages from FOLIO
#

class FOLIOErrorException(Exception):
    def __init__(self, error):
        super().__init__()
        self.__error = error; self.__error_message = ''; self.__error_code = 'NO_CODE'
        if "errors" in error and len(error["errors"]) > 0:
            if "message" in error["errors"][0]:
                self.__error_message = error["errors"][0]["message"]
            if "code" in error["errors"][0]:
                self.__error_code = error["errors"][0]["code"]

    def __str__(self):
        return "FOLIO hat eine Fehlermeldung gesendet:\nError: " + str(self.__error)

    @property
    def data(self):
        return {
            "code":self.__error_code,
            "message":self.__error_message
        }

#
# ServicePoint list is empty
#

class ServicePointException(Exception):

    def __init__(self, requesterId, itemId):
        super().__init__(requesterId, itemId)

    def __str__(self):
        return "Es konnte keine Zieltheke zugeordnet werden: Requester: " + str(self.args[0]) + " Item: " + str(self.args[1])

    @property
    def data(self):
        return {
            "requesterId":self.args[0],
            "itemId":self.args[1]
        }

#
# Not Found
# This is not(!) HTTP 404
# It indicates that there is no result for an object search in FOLIO
# e.g. an empty list of something
#

class NotFoundException(Exception):

    def __init__(self, type, id):
        super().__init__(type, id)

    def __str__(self):
        return "Das folgende Objekt wurde im Bibliothekssystem nicht gefunden: " + str(self.args[0]) + ": " + str(self.args[1])

    @property
    def data(self):
        return {
            "type":self.args[0],
            "id":self.args[1]
        }

###
# Exception handling for Values
###

#
# Script Argument
#

class ArgumentException(Exception):
    def __init__(self, error):
        super().__init__(error)

    def __str__(self):
        return "Die Script Argumente sind fehlerhaft."

#
# UUID
#

class UUIDException(Exception):

    def __init__(self, uuid):
        super().__init__(uuid)

    def __str__(self):
        return "Die UUID ist nicht gültig: " + str(self.args[0])

    @property
    def data(self):
        return {"uuid":self.args[0]}

#
# FOLIOID
#

class FOLIOIDException(Exception):

    def __init__(self, folioId):
        super().__init__(folioId)

    def __str__(self):
        return "Die FOLIOID ist nicht gültig: " + str(self.args[0])

    @property
    def data(self):
        return {"folioId":self.args[0]}
#
# HRID (input field => escape output)
#

class HRIDException(Exception):

    def __init__(self, hrid):
        super().__init__(hrid)

    def __str__(self):
        return "Die HRID ist nicht gültig: " + str(escape(self.args[0]))

    @property
    def data(self):
        return {"hrid":escape(self.args[0])}

#
# InstanceID
#

class InstanceIDException(Exception):

    def __init__(self, instanceId):
        super().__init__(instanceId)

    def __str__(self):
        return "Die InstanceID ist nicht gültig: " + str(self.args[0])

    @property
    def data(self):
        return {"instanceId":self.args[0]}

#
# ItemID (input field => escape output)
#

class ItemIDException(Exception):

    def __init__(self, itemId):
        super().__init__(itemId)

    def __str__(self):
        return "Die ItemID ist nicht gültig: " + str(escape(self.args[0]))

    @property
    def data(self):
        return {"itemId":escape(self.args[0])}

#
# ServicePointID (input field => escape output)
#

class ServicePointIDException(Exception):

    def __init__(self, servicePointId):
        super().__init__(servicePointId)

    def __str__(self):
        return "Die ServicePointId ist nicht gültig: " + str(escape(self.args[0]))

    @property
    def data(self):
        return {"servicePointId":escape(self.args[0])}
    
#
# ExternalSystemID
#

class ExternalSystemIDException(Exception):

    def __init__(self, externalSystemId):
        super().__init__(externalSystemId)

    def __str__(self):
        return "Die externe System ID ist nicht gültig: " + str(self.args[0])

    @property
    def data(self):
        return {"externalSystemId":self.args[0]}

#
# Environment variable not set
#

class EnvironmentException(Exception):

    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return "Die Umgebungsvariable " + str(self.args[0] + "ist nicht gesetzt.")

    @property
    def data(self):
        return {"envName":self.args[0]}

#
# Barcode
#

class BarcodeException(Exception):

    def __init__(self, barcode):
        super().__init__(barcode)

    def __str__(self):
        return "Der User Barcode ist nicht gültig: " + str(self.args[0])

    @property
    def data(self):
        return {"barcode":self.args[0]}

#
# Input fields (input field => escape output)
#

class InputException(Exception):

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return "Nicht alle Input Felder des Formulars sind gültig: " + escape(self.args[0])
    
    @property
    def data(self):
        return {"input":escape(self.args[0])}

###
# Exception handling for folio.entities
###

#
# FOLIOItem
#

from folio.types import UUID, FOLIOItemStatus

class ItemException(Exception):

    def __init__(self, item):
        super().__init__(item)

    def __str__(self):
        error = "Nicht alle erforderlichen Felder des Items sind gültig:\n"
        if not FOLIOItemStatus()(self.args[0]["status"]["name"]):
            error += "Ungültiger Status: " + self.args[0]["status"]["name"] + "\n"
        if not UUID()(self.args[0]["holdingsRecordId"]):
            error += "Ungültiges Format: holdingsRecordId: " + self.args[0]["holdingsRecordId"] + "\n"
        if not UUID()(self.args[0]["materialType"]["id"]):
            error += "Ungültiges Format: materialType: " + self.args[0]["materialType"]["id"] + "\n"
        if not UUID()(self.args[0]["permanentLoanType"]["id"]):
            error += "Ungültiges Format: permanentLoanType: " + self.args[0]["permanentLoanType"]["id"] + "\n"
        return error

#
# FOLIORequest
#

from folio.types import EmptyString, DateTime, Today, FOLIOID, FOLIORequestType, FOLIORequestLevel, FOLIORequestStatus, FOLIOFulfillmentPreference
from folio.values.barcode import Barcode

class RequestException(Exception):

    def __init__(self, request):
        super().__init__(request)

    def __str__(self):
        error = "Nicht alle erforderlichen Felder des Requests sind gültig:\n"
        if not FOLIOID()(self.args[0]["instanceId"]):
            error += "Ungültiges Format: " + self.args[0]["instanceId"] + "\n"
        if not UUID()(self.args[0]["requesterId"]):
            error += "Ungültiges Format: requesterId: " + self.args[0]["requesterId"] + "\n"
        if     EmptyString()(self.args[0]["instance"]["title"]):
            error += "Ungültiges Format: instance_title: Darf nicht leer sein.\n"
        if not Barcode()(self.args[0]["requester"]["barcode"]):
            error += "Ungültiges Format: requester_barcode: " + self.args[0]["requester"]["barcode"] + "\n"
        if not FOLIORequestType()(self.args[0]["requestType"]):
            error += "Ungültiges Format: requestType: " + self.args[0]["requestType"] + "\n"
        if not FOLIORequestLevel()(self.args[0]["requestLevel"]):
            error += "Ungültiges Format: requestLevel: " + self.args[0]["requestLevel"] + "\n"
        if not DateTime()(self.args[0]["requestDate"]):
            error += "Ungültiges Datum: requestDate: " + self.args[0]["requestDate"] + "\n"
        if not Today()(self.args[0]["requestDate"]):
            error += "Datum ist nicht heute: requestDate: " + self.args[0]["requestDate"] + "\n"
        if not FOLIOFulfillmentPreference()(self.args[0]["fulfillmentPreference"]):
            error += "Ungültiges Format: fulfillmentPreference: " + self.args[0]["fulfillmentPreference"] + "\n"
        if not FOLIORequestStatus()(self.args[0]["status"]):
            error += "Ungültiges Format: status: " + self.args[0]["status"] + "\n"
        return error
