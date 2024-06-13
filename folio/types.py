#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

import re
import datetime

#
#
#

class EmptyString():
    def __call__(self, value: str):
        return value == ""

#
#
#

class DateTime():
    def __init__(self, checkToday = False):
        self.__pattern = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6}$'
        self.__checkToday = checkToday

    def __call__(self, value: str):
        if re.fullmatch(self.__pattern, value):
            date = value[:10].split("-")
            try:
                # The constructor of datetime.date raises a ValueError, if the date is unvalid.
                if self.__checkToday:
                    return datetime.date(int(date[0]), int(date[1]), int(date[2])) == \
                           datetime.date.today() # date is valid and it is today.
                else:
                    datetime.date(int(date[0]), int(date[1]), int(date[2]))
                    return True # date is valid, but it's not today.
            except ValueError:
                return False
        else:
            return False

#
#
#

class Today(DateTime):
    def __init__(self):
        super().__init__(True)

#
#
#

class UUID():

    def __init__(self):
        self.__pattern = r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'

    def __call__(self, value):
        return re.fullmatch(self.__pattern, value)

#
#
#

class FOLIOID():

    def __init__(self):
        self.__pattern = r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[1-5][a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$'

    def __call__(self, value):
        return re.fullmatch(self.__pattern, value)

#
#
#

class FOLIOItemStatus():

    def __init__(self):
        self.__status = [ "Aged to lost",
            "Available",
            "Awaiting pickup",
            "Awaiting delivery",
            "Checked out",
            "Claimed returned",
            "Declared lost",
            "In process",
            "In process (non-requestable)",
            "In transit",
            "Intellectual item",
            "Long missing",
            "Lost and paid",
            "Missing",
            "On order",
            "Paged",
            "Restricted",
            "Order closed",
            "Unavailable",
            "Unknown",
            "Withdrawn"
        ]

    def __call__(self, value :str):
        return value in self.__status

    @property
    def default(self):
        return "Available"

#
#
#

class FOLIORequestType():

    def __init__(self):
        self.__type = [
            "Hold",
            "Recall",
            "Page"
        ]

    def __call__(self, value :str):
        return value in self.__type

    @property
    def default(self):
        return "Page"

#
#
#

class FOLIORequestStatus():

    def __init__(self):
        self.__status = [
            "Open - Not yet filled",
            "Open - Awaiting pickup",
            "Open - In transit",
            "Open - Awaiting delivery",
            "Closed - Filled",
            "Closed - Cancelled",
            "Closed - Unfilled",
            "Closed - Pickup expired"
        ]

    def __call__(self, value :str):
        return value in self.__status

    @property
    def default(self):
        return "Open - Not yet filled"

#
#
#

class FOLIORequestLevel():

    def __init__(self):
        self.__level = [
            "Item",
            "Title"
        ]

    def __call__(self, value :str):
        return value in self.__level

    @property
    def default(self):
        return "Item"

#
#
#

class FOLIOFulfillmentPreference():

    def __init__(self):
        self.__preference = [
            "Hold Shelf",
            "Delivery"
        ]

    def __call__(self, value :str):
        return value in self.__preference

    @property
    def default(self):
        return "Hold Shelf"
