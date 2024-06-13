#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

import re
from folio.exceptions import BarcodeException

#
#
#

class Barcode():
    def __init__(self):
        self.__pattern = r'[0-9]{12}$'

    def __call__(self, value: str):
        if re.fullmatch(self.__pattern, value):
            return True
        else:
            return False

#
#
#

class BarcodeValue(Barcode):
    def __init__(self):
        super().__init__()

    def __call__(self, value: str):
        if super().__call__(value):
            return value
        else:
            raise BarcodeException(value)
