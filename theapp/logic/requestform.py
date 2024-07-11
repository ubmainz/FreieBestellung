#!/usr/bin/python3.9
#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

import uuid
from flask import Blueprint, request, current_app, render_template
from markupsafe import escape

from theapp.looknfeel import LookNFeel

from folio.connection import Connection

from folio.entities.user import User
from folio.entities.item import Item
from folio.entities.allowedservicepoints import AllowedServicePoints
from folio.entities.request import Request

from folio.values.externalsystemid import ExternalSystemID, ExternalSystemIDValue
from folio.values.barcode import Barcode, BarcodeValue
from folio.values.hrid import HRID, HRIDValue
from folio.values.uuid import UUIDValue, ItemIDValue, ServicePointIDValue 

from user.values.jahrgang import Jahrgang, JahrgangValue
from user.values.band import Band, BandValue
from user.values.seitenzahldatum import SeitenzahlDatum, SeitenzahlDatumValue

from folio.exceptions import ConnectionException, HTTPException, HRIDException, BarcodeException, UUIDException, \
                             ItemException, RequestException, ServicePointException,  \
                             FOLIOErrorException, InputException, NotFoundException, \
                             InstanceIDException, ItemIDException, ServicePointIDException, ExternalSystemIDException

requestform = Blueprint('requestform', __name__)

@requestform.route("/", methods=['GET'])
def create_form():

    look_n_feel = LookNFeel(request.args.get('looknfeel'))

    ex_sys_id_env   = current_app.config["EXTERNAL_SYSTEM_ID_ENV"]
    ex_sys_id_regex = current_app.config["EXTERNAL_SYSTEM_ID_REGEX"]
    connection_ini  = current_app.config["CONNECTION_INI"]
    logger          = current_app.logger

    try:
        log_entry = uuid.uuid4(); logger.debug("New Session: %s" % (log_entry))

        connection = Connection(connection_ini, logger)

        if connection.is_established():

            try:
                if current_app.debug:
                    # Debugging ohne IDM. User über GET Parameter 'externalSystemId' holen.
                    exSysId = ExternalSystemIDValue(ex_sys_id_regex)(request.args.get('exSysId', ''))
                else:
                    exSysId = ExternalSystemIDValue(ex_sys_id_regex)(request.environ.get(ex_sys_id_env))

                user = connection.getUserByExternalSystemId(exSysId)

                # Check if user has valid Barcode, if not we can't go on...
                barcode = BarcodeValue()(user.barcode)

                item = connection.getItemByHRID(HRIDValue()(request.args.get('hrid', '')))

                logger.info("Session: %s Step 1: UserID: %s Intellectual Item: %s" % (log_entry, user.id, item.id))

                return render_template(look_n_feel('item.html'), looknfeel=look_n_feel.look, session=log_entry, user=user.data, item=item.data, localisation=True)

            except ExternalSystemIDException as error:
                logger.error("Session: %s ExternalSystemIDException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="ExternalSystemId", error=error.data, localisation=True)

            except BarcodeException as error:
                logger.error("Session: %s BarcodeException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="Barcode", error=error.data, localisation=True)

            except HRIDException as error:
                logger.error("Session: %s HRIDException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="HRID", error=error.data, localisation=True)

            except NotFoundException as error:
                logger.error("Session: %s NotFoundException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="NotFound", error=error.data, localisation=True)

            except HTTPException as error:
                logger.error("Session: %s HTTPException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="HTTP", error=error.data, localisation=True)

            except BaseException as error:
                logger.error("Session: %s Something unexpected went wrong! %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="Base", localisation=True)

            finally:
                pass

    except ConnectionException as error:
        logger.error("Session: %s ConnectionException: %s" % (log_entry, str(error)))
        return render_template(look_n_feel('errors.html'), exception="Connection", localisation=True)

    except BaseException as error:
        logger.error("Session: %s Something unexpected went wrong! %s" % (log_entry, str(error)))
        return render_template(look_n_feel('errors.html'), exception="Base", localisation=True)

    finally:
        pass

#
#
#

@requestform.route("/", methods=['POST'])
def create_item():

    look_n_feel = LookNFeel(request.form.get('looknfeel'))

    connection_ini = current_app.config["CONNECTION_INI"]
    logger         = current_app.logger

    try:
        log_entry = UUIDValue()(request.form.get('session'))

        connection = Connection(connection_ini, logger)

        if connection.is_established():

            try:
                user = connection.getUserByBarcode(BarcodeValue()(request.form.get('barcode')))

                item = connection.getItemByID(ItemIDValue()(request.form.get('id')))

                if item.is_intellectual():

                    item.status_name = "Available"

                    item.yearCaption = ["FREIE BESTELLUNG"]

                    jahrgang =   JahrgangValue()       (request.form.get('jahrgang'))
                    band =       BandValue()           (request.form.get('band'))
                    seitenzahl = SeitenzahlDatumValue()(request.form.get('seitenzahl'))

                    item.chronology = jahrgang + " " + band + " " + seitenzahl

                    newItem = connection.createItem(item.creation_json)
                   
                    servicePoints = connection.getAllowedServicePoints(user.id, newItem.id)

                    logger.info("Session: %s Step 2: UserID: %s New Item: %s" % (log_entry, user.id, newItem.id))

                    return render_template(look_n_feel('servicepoints.html'), looknfeel=look_n_feel.look, session=log_entry, user=user.data, item=newItem.data, servicepoints=servicePoints.servicepoints)
                
                else:
                    raise ItemException(item.data)

            except InputException as error: # Der user hat ungültige Daten in das Formular eingetragen
                logger.error("Session: %s InputException: %s" % (log_entry, str(error)))

                errors = {}; values = {}

                if request.form.get('jahrgang'):
                    if Jahrgang()(request.form.get('jahrgang')):
                        values |= {"jahrgang":request.form.get('jahrgang')}
                    else:
                        errors |= {"jahrgang":escape(request.form.get('jahrgang'))}

                if request.form.get('band'):
                    if Band()(request.form.get('band')):
                        values |= {"band":request.form.get('band')}
                    else:
                        errors |= {"band":escape(request.form.get('band'))}

                if request.form.get('seitenzahl'):
                    if SeitenzahlDatum()(request.form.get('seitenzahl')):
                        values |= {"seitenzahl":request.form.get('seitenzahl')}
                    else:
                        errors |= {"seitenzahl":escape(request.form.get('seitenzahl'))}

                return render_template(look_n_feel('item.html'), looknfeel=look_n_feel.look, session=log_entry, user=user.data, item=item.data, errors=errors, values=values) 

            except ItemException as error:
                logger.error("Session: %s ItemException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="Item")

            except FOLIOErrorException as error:
                logger.error("Session: %s FOLIOErrorException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="FOLIOError", error=error.data)

            except HRIDException as error:
                logger.error("Session: %s HRIDException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="HRID", error=error.data)

            except BarcodeException as error:
                logger.error("Session: %s BarcodeException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="Barcode", error=error.data)

            except NotFoundException as error:
                logger.error("Session: %s NotFoundException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="NotFound", error=error.data)
            
            except ServicePointException as error:
                logger.error("Session: %s ServicePointException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="ServicePoint", error=error.data)

            except HTTPException as error:
                logger.error("Session: %s HTTPException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="HTTP", error=error.data)

            except BaseException as error:
                logger.error("Session: %s Something unexpected went wrong! %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="Base")

            finally:
                pass

    except ConnectionException as error:
        logger.error("Session: %s ConnectionException: %s" % (log_entry, str(error)))
        return render_template(look_n_feel('errors.html'), exception="Connection")
    
    except UUIDException as error:
        logger.error("Session: %s UUIDException: %s" % (log_entry, str(error)))
        return render_template(look_n_feel('errors.html'), exception="UUID", error=error.data, localisation=True)

    except BaseException as error:
        logger.error("Session: %s Something unexpected went wrong! %s" % (log_entry, str(error)))
        return render_template(look_n_feel('errors.html'), exception="Base")

    finally:
        pass

#
#
#

@requestform.route("/create", methods=['POST'])
def create_request():

    look_n_feel = LookNFeel(request.form.get('looknfeel'))

    connection_ini = current_app.config["CONNECTION_INI"]
    logger         = current_app.logger

    try:
        log_entry = UUIDValue()(request.form.get('session'))

        connection = Connection(connection_ini, logger)

        if connection.is_established():

            try:
                user = connection.getUserByBarcode(BarcodeValue()(request.form.get('barcode')))

                item = connection.getItemByID(ItemIDValue()(request.form.get('id')))

                newRequest = connection.createRequest(Request({
                                "instanceId": connection.getInstanceIdByItem(item),
                                "requesterId": user.id,
                                "requester": {
                                    "barcode": user.barcode,
                                    "lastName": user.personal_lastName,
                                    "firstName": user.personal_firstName
                                },
                                "instance": {
                                    "title": item.title
                                },
                                "holdingsRecordId": item.holdingsRecordId,
                                "itemId": item.id,
                                "pickupServicePointId": ServicePointIDValue()(request.form.get('servicePoint'))
                            }).creation_json)

                logger.info("Session: %s Step 3: UserID: %s New Item: %s RequestID: %s" % (log_entry, user.id, item.id, newRequest.id))

                return render_template(look_n_feel('request.html'), looknfeel=look_n_feel.look, session=log_entry, request=newRequest.data)

            except ServicePointIDException as error: # Der User hat keine Abholtheke ausgewählt => Formular nochmal anzeigen.

                servicePoints = connection.getAllowedServicePoints(user.id, item.id)

                return render_template(look_n_feel('servicepoints.html'), looknfeel=look_n_feel.look, session=log_entry, user=user.data, item=item.data, servicepoints=servicePoints.servicepoints, error=True)

            except ServicePointException as error: # Leere Liste! In FOLIO gibt es keine Abholtheken für die Kombination aus User und Item.
                                                   # D.h. das Item ist nicht ausleihbar. Dürfte eigentlich nicht auftreten. Wäre ein bibliothekarisches Problem.
                                                   # Bitte FOLIO richtig konfigurieren :)
                logger.error("Session: %s ServicePointException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="ServicePoint", error=error.data)
            
            except RequestException as error:
                logger.error("Session: %s RequestException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="Request")

            except InstanceIDException as error:
                logger.error("Session: %s InstanceIDException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="InstanceID", error=error.data)

            except ItemIDException as error:
                logger.error("Session: %s ItemIDException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="ItemId", error=error.data)

            except BarcodeException as error:
                logger.error("Session: %s BarcodeException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="Barcode", error=error.data)

            except NotFoundException as error:
                logger.error("Session: %s NotFoundException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="NotFound", error=error.data)

            except FOLIOErrorException as error:
                logger.error("Session: %s FOLIOErrorException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="FOLIOError", error=error.data)
            
            except HTTPException as error:
                logger.error("Session: %s HTTPException: %s" % (log_entry, str(error)))
                return render_template(look_n_feel('errors.html'), exception="HTTP", error=error.data)

            finally:
                pass

    except ConnectionException as error:
        logger.error("Session: %s ConnectionException: %s" % (log_entry, str(error)))
        return render_template(look_n_feel('errors.html'), exception="Connection")
    
    except UUIDException as error:
        logger.error("Session: %s UUIDException: %s" % (log_entry, str(error)))
        return render_template(look_n_feel('errors.html'), exception="UUID", error=error.data, localisation=True)

    except BaseException as error:
        logger.error("Session: %s Something unexpected went wrong! %s" % (log_entry, str(error)))
        return render_template(look_n_feel('errors.html'), exception="Base")

    finally:
        pass
