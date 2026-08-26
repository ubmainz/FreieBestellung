#
# @author    Matthias Genzmehr
# @copyright 2026 Universitätsbibliothek Mainz
# @version   1.1
#

import sys, logging

from logging import FileHandler, Formatter

from folio.connection import Connection

from folio.values.uuid import ItemIDValue
from folio.values.filename import FileName

from folio.exceptions import ArgumentException, \
                             ItemIDException, \
                             HTTPException, \
                             ConnectionException, \
                             NotFoundException

def main():

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

            FOLIO = Connection("connection.ini")

            if FOLIO.is_established():

                request = FOLIO.getOpenRequestByItemId(id)

                if request is None:

                    item = FOLIO.getItemByID(id)

                    if item.status_name == "Available":

                        if item.barcode == "":

                            if FOLIO.deleteItem(id):
                                logEntry = f"Das Item mit der ID {id} wurde gelöscht!"
                                logger.info(logEntry)
                                print(logEntry)

                        else:
                            logEntry = f"Das Item mit der ID {id} kann nicht gelöscht werden. Es wurde bereits ein Barcode vergeben: {item.barcode}."
                            logger.info(logEntry)
                            print(logEntry)

                    else:
                        logEntry = f"Das Item mit der ID {id} konnte nicht gelöscht werden. Item Status: {item.status_name}."
                        logger.info(logEntry)
                        print(logEntry)

                else:
                    logEntry = f"Das Item mit der ID {id} konnte nicht gelöscht werden. Es liegt eine offene Bestandsanfrage vor."
                    logger.info(logEntry)
                    print(logEntry)

        except ItemIDException as error:
            logEntry = f"ItemIDException: {error}"
            logger.error(logEntry)
            print(logEntry)

        except NotFoundException as error:
            logEntry = f"NotFoundException: {error}"
            logger.error(logEntry)
            print(logEntry)

        except HTTPException as error:
            logEntry = f"HTTPException: {error}"
            logger.error(logEntry)
            print(logEntry)

        except ConnectionException as error:
            logEntry = f"ConnectionException: {error}"
            logger.error(logEntry)
            print(logEntry)

        except BaseException as error:
            logEntry = f"Something unexpected went wrong! {error}"
            logger.error(logEntry)
            print(logEntry)

        finally:
            pass

    except ArgumentException as error:
        print(f"ArgumentException: {error}")

    finally:
        pass

if __name__ == "__main__":
    main()
