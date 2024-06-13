#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

import re
from folio.exceptions import InputException

#
#
#

class Band():
    def __init__(self):
        self.__pattern = r'[0-9a-zA-ZäüöÄÜÖß ./-]{0,40}$'

    def __call__(self, value):
        if re.fullmatch(self.__pattern, value):
            return True
        else:
            return False

#
#
#

class BandValue(Band):
    def __init__(self):
        super().__init__()

    def __call__(self, value):
        if super().__call__(value):
            return value
        else:
            raise InputException(value)
