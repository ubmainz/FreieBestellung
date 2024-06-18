#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

import re
from folio.exceptions import ExternalSystemIDException

#
# 
#

class ExternalSystemID():
    def __init__(self, pattern :str):
        self.__pattern = pattern

    def __call__(self, value: str):
        if self.__pattern == None:
            return True

        if re.fullmatch(self.__pattern, value):
            return True
        else:
            return False

#
# 
#

class ExternalSystemIDValue(ExternalSystemID):
    def __init__(self, pattern : str):
        super().__init__(pattern)

    def __call__(self, value: str):
        if super().__call__(value):
            return value
        else:
            raise ExternalSystemIDException(value)
