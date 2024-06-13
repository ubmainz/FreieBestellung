#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from folio.exceptions import UUIDException, ItemIDException, ServicePointIDException
from folio.types import UUID

#
#
#

class UUIDValue(UUID):
    def __init__(self):
        super().__init__()

    def __call__(self, value: str):
        if super().__call__(value):
            return value
        else:
            raise UUIDException(value)

#
#
#

class ItemIDValue(UUID):
    def __init__(self):
        super().__init__()

    def __call__(self, value: str):
        if super().__call__(value):
            return value
        else:
            raise ItemIDException(value)

#
#
#

class ServicePointIDValue(UUID):
    def __init__(self):
        super().__init__()

    def __call__(self, value):
        if value == None:
            raise ServicePointIDException(value)
        elif super().__call__(value):
            return value
        else:
            raise ServicePointIDException(value)
