#!/usr/bin/python3.9
#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

import sys
import logging
from logging import FileHandler, Formatter

from folio.connection import Connection
from folio.values.uuid import ItemIDValue
from folio.values.filename import FileName
from folio.exceptions import ArgumentException, ItemIDException, HTTPException, ConnectionException, NotFoundException

try:
    if len(sys.argv) < 2: raise ArgumentException("Das Script benötigt eine ItemID als Argument!")

    if len(sys.argv) >= 3 and FileName()(sys.argv[2]) :
        logFileName = sys.argv[2]
    else:
        logFileName = "remove.log"

    logger = logging.Logger("RemoveItem")
    logger.setLevel(logging.INFO)

    handler = FileHandler(logFileName)
    handler.setLevel(logging.INFO)
    handler.setFormatter(Formatter("{asctime} {levelname}: {message}", "%Y-%m-%d %H:%M:%S", style="{"))

    logger.addHandler(handler)

    try:
        id = ItemIDValue()(sys.argv[1])

        connection = Connection("connection.ini")

        if connection.is_established():
            if connection.deleteItem(id):
                logEntry = "Das Item mit der ID %s wurde gelöscht!" % (id)
                logger.info(logEntry)
                print(logEntry)

    except ItemIDException as error:
        logEntry = "ItemIDException: " + str(error)
        logger.error(logEntry)
        print(logEntry)

    except NotFoundException as error:
        logEntry = "NotFoundException: " + str(error)
        logger.error(logEntry)
        print(logEntry)

    except HTTPException as error:
        logEntry = "HTTPException: " + str(error)
        logger.error(logEntry)
        print(logEntry)

    except ConnectionException as error:
        logEntry = "ConnectionException: " + str(error)
        logger.error(logEntry)
        print(logEntry)

    except BaseException as error:
        logEntry = "Something unexpected went wrong! " + str(error)
        logger.error(logEntry)
        print(logEntry)

    finally:
        pass

except ArgumentException as error:
    print("ArgumentException: " + str(error))

finally:
    pass
