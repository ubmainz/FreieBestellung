#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from folio.exceptions import FOLIOIDException
from folio.types import FOLIOID

#
#
#

class FOLIOIDValue(FOLIOID):
    def __init__(self):
        super().__init__()

    def __call__(self, value: str):
        if super().__call__(value):
            return value
        else:
            raise FOLIOIDException(value)
