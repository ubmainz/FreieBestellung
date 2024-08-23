#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

import requests, configparser, json

from folio.entities.user import User
from folio.entities.item import Item
from folio.entities.newitem import NewItem
from folio.entities.newrequest import NewRequest
from folio.entities.allowedservicepoints import AllowedServicePoints
from folio.entities.folioerror import FOLIOError
from folio.exceptions import NotFoundException, HTTPException, FOLIOErrorException, ConnectionException, ServicePointException

class Connection:

    def __init__(self, connection_ini, logger = None):

        cfp = configparser.ConfigParser(allow_no_value=True)

        self.__logger = logger

        try:
            file = open(connection_ini, "r")
            cfp.read_file(file)

            section = "connection"

            self.__url =       cfp[section]["okapi_url"]
            self.__login_url = cfp[section]["url_auth_login"]
            self.__tenant =    cfp[section]["tenant_id"]
            self.__user =      cfp[section]["username"]
            self.__pwd =       cfp[section]["password"]

        except FileNotFoundError as error:
            if self.__logger: self.__logger.debug(connection_ini + " konnte nicht gelesen werden! " + str(error))
            raise ConnectionException(FOLIOError("inifile.notfound", "Ini file not found").data) from error

        except PermissionError as error:
            if self.__logger: self.__logger.debug(connection_ini + " konnte nicht gelesen werden!" + str(error))
            raise ConnectionException(FOLIOError("inifile.permission", "Permission for ini file is missing").data) from error

        except KeyError as error:
            if self.__logger: self.__logger.debug("Die Config-Datei ist unvollständig! " + str(error))
            raise ConnectionException(FOLIOError("inifile.incomplete", "Incomplete ini file").data) from error

        except BaseException as error:
            if self.__logger: self.__logger.debug("Das Connection-Objekt konnte nicht initialisiert werden: " + str(error))
            raise ConnectionException(FOLIOError("error.unexpected", "An unexpected error appeared").data) from error

        finally:
            file.close()

        self.__okapi_token = ""

        payload = {
            'tenant': self.__tenant,
            'username': self.__user,
            'password': self.__pwd
        }

        headers = {
            'X-Okapi-Tenant': self.__tenant,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        if self.__logger: self.__logger.debug("POST " + self.__login_url)

        response = requests.post(self.__login_url, headers=headers, json=payload)
        self.__status_code = response.status_code  # HTTP 201 if a token was created!

        if self.__logger: self.__logger.debug("Response: " + str(self.__status_code) + "\nResponse Body: " + response.text)

        if self.__status_code == 201:
            data = json.loads(response.text)
            self.__okapi_token = data["okapiToken"]

        elif self.__status_code == 404:
            raise ConnectionException(FOLIOError("auth.notfound", str(response.text)).data)

        elif self.__status_code == 405:
            raise ConnectionException(FOLIOError("auth.notallowed", str(response.text)).data)

        elif self.__status_code == 422:
            data = json.loads(response.text)
            raise ConnectionException(data)

        else:
            raise ConnectionException({})

        self.__request_payload = { }
        self.__request_headers = { 'Authorization': 'Bearer ' + self.__okapi_token }
        self.__last_request_status_code = 0

    #
    #
    #

    def is_established(self):
        if self.__status_code == 201:
            return True
        else:
            return False

    #
    # Getter methods
    #

    @property
    def url(self):
        return self.__url
    
    @property
    def tenant(self):
        return self.__tenant
    
    @property
    def status_code(self):
        return self.__status_code
    
    @property
    def last_request_status_code(self):
        return self.__last_request_status_code

    @property
    def okapi_token(self):
        return self.__okapi_token

    #
    # requests
    #

    def get(self, endpoint):
        if self.__logger: self.__logger.debug("GET " + self.__url + endpoint)
        response = requests.get(self.__url + endpoint, headers=self.__request_headers, data=self.__request_payload)
        self.__last_request_status_code = response.status_code
        self.logResponse(response)
        return response

    def post(self, endpoint, body):
        if self.__logger: self.__logger.debug("POST " + self.__url + endpoint + "\nBody: " + body)
        response = requests.post(self.__url + endpoint, headers=self.__request_headers, data=body)
        self.__last_request_status_code = response.status_code
        self.logResponse(response)
        return response
    
    def delete(self, endpoint):
        if self.__logger: self.__logger.debug("DELETE " + self.__url + endpoint)
        response = requests.delete(self.__url + endpoint, headers=self.__request_headers, data=self.__request_payload)
        self.__last_request_status_code = response.status_code
        self.logResponse(response)
        return response

    #
    # logging
    #

    def logResponse(self, response):
        if self.__logger:
            logEntry = "Response: " + str(self.__last_request_status_code) + "\nResponse Body: " + response.text
            if self.__last_request_status_code == 403:
                self.__logger.error(logEntry)
            self.__logger.debug(logEntry)

    #
    # GET data methods
    #

    def getUserByBarcode(self, barcode):
        response = self.get('users?query=barcode=="' + str(barcode) + '"')

        if self.__last_request_status_code == 200:
            data = json.loads(response.text)
            if "users" in data and len(data['users']) > 0:
                return User(data['users'][0])
            else:
                raise NotFoundException("User", str(barcode))

        else:
            raise HTTPException(self.__last_request_status_code)

    #
    #
    #

    def getUserByExternalSystemId(self, externalSystemId):
        response = self.get('users?query=externalSystemId=="' + str(externalSystemId) + '"')

        if self.__last_request_status_code == 200:
            data = json.loads(response.text)
            if "users" in data and len(data['users']) > 0:
                return User(data['users'][0])
            else:
                raise NotFoundException("User", str(externalSystemId))

        else:
            raise HTTPException(self.__last_request_status_code)

    #
    #
    #

    def getItemByHRID(self, hrid):
        response = self.get('inventory/items?query=hrid=="' + str(hrid) + '"')

        if self.__last_request_status_code == 200:
            data = json.loads(response.text)
            if "items" in data and len(data['items']) > 0:
                return Item(data['items'][0])
            else:
                raise NotFoundException("Exemplar", str(hrid))

        elif self.__last_request_status_code == 404:
            raise NotFoundException("HRID", str(hrid))    

        else:
            raise HTTPException(self.__last_request_status_code)

    #
    #
    #

    def getItemByID(self, id):
        response = self.get("inventory/items/" + str(id))

        if self.__last_request_status_code == 200:
            return Item(json.loads(response.text))

        elif self.__last_request_status_code == 404:
            raise NotFoundException("Item", str(id))

        else:
            raise HTTPException(self.__last_request_status_code)

    #
    #
    #

    def getInstanceIdByItem(self, item):
        response = self.get("holdings-storage/holdings/" + str(item.holdingsRecordId))

        if self.__last_request_status_code == 200:
            data = json.loads(response.text)
            if "instanceId" in data:
                return data['instanceId']
            else:
                raise NotFoundException("Instance ID in Holding", str(item.holdingsRecordId))
        
        elif self.__last_request_status_code == 404:
            raise NotFoundException("Holding", str(item.holdingsRecordId))
        
        else:
            raise HTTPException(self.__last_request_status_code)

    #
    #
    #

    def getAllowedServicePoints(self, requesterId, itemId):
        response = self.get("circulation/requests/allowed-service-points?requesterId=" + str(requesterId) + "&itemId=" + str(itemId) + "&operation=create")

        if self.__last_request_status_code == 200:
            data = json.loads(response.text)
            if "Page" in data and len(data['Page']) > 0:
                return AllowedServicePoints(data['Page'])
            else:
                raise ServicePointException(requesterId, itemId)
        else:
            raise HTTPException(self.__last_request_status_code)

    #
    # POST data methods
    #

    def createItem(self, itemData):
        response = self.post("item-storage/items", itemData)

        if self.__last_request_status_code == 201:
            return NewItem(json.loads(response.text))

        elif self.__last_request_status_code == 422:
            raise FOLIOErrorException(json.loads(response.text))

        else:
            raise HTTPException(self.__last_request_status_code)

    #
    #
    #

    def createRequest(self, requestData):
        response = self.post("circulation/requests", requestData)

        if self.__last_request_status_code == 201:
            return NewRequest(json.loads(response.text))
                
        elif self.__last_request_status_code == 422:
            data = json.loads(response.text)
            """
            if a request with the same position already exists, increment position and try again:
            data e.g. =>
            { "errors": [ {
                            "message": "Cannot have more than one request with the same position in the queue",
                            "parameters": [],
                            "itemId": "8991c555-843b-483d-8f9a-f0ee8dcc32e8",
                            "position": 5
                          } ] } """
            
            if "errors" in data and len(data["errors"]) > 0 and \
                data["errors"][0]["message"] == "Cannot have more than one request with the same position in the queue":
                    newRequestData = json.loads(requestData)
                    newRequestData["position"] = int(data["errors"][0]["position"]) + 1
                    self.createRequest(json.dumps(newRequestData))
            else:
                raise FOLIOErrorException(data)

        else:
            raise HTTPException(self.__last_request_status_code)

    #
    # DELETE data methods
    #

    def deleteItem(self, id):
        self.delete("inventory/items/" + str(id))

        if self.__last_request_status_code == 204:
            return True

        elif self.__last_request_status_code == 404:
            raise NotFoundException("Item", str(id))

        else:
            raise HTTPException(self.__last_request_status_code)
