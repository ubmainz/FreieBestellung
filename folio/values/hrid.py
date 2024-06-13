#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

import re
from folio.exceptions import HRIDException

#
#
#

class HRID():
    def __init__(self):
        self.__pattern_1 = r'it[0-9]{11}$'
        self.__pattern_2 = r'[0-9X]{9,}-1$'

    def __call__(self, value: str):
        if re.fullmatch(self.__pattern_1, value) or \
           re.fullmatch(self.__pattern_2, value):
            return True
        else:
            return False

#
#
#

class HRIDValue(HRID):
    def __init__(self):
        super().__init__()

    def __call__(self, value: str):
        if super().__call__(value):
            return value
        else:
            raise HRIDException(value)
