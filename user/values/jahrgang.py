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

class Jahrgang():
    def __init__(self):
        self.__pattern = r'[1-2]{1}[0-9]{3}$'

    def __call__(self, value):
        if re.fullmatch(self.__pattern, value):
            return True
        else:
            return False

#
#
#

class JahrgangValue(Jahrgang):
    def __init__(self):
        super().__init__()

    def __call__(self, value):
        if super().__call__(value):
            return value
        else:
            raise InputException(value)
