#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from folio.entities.item import Item
from folio.exceptions import ItemException
import json

class NewItem(Item):
    """This class is used to receive and indicate a new item after creation in FOLIO.
    It actually implements no further functionality, but can be used to do so.
    """

    def __init__(self, item = {}):
        super().__init__(item)
    
    def check_required(self):
        return super().check_required() # and  \
            # place further field comparsion here, if needed

    @property
    def data(self):
        return super().data | {
            # add further fields here
        }

    @property
    def creation_data(self):
        if self.check_required():
            return super().creation_data | {
                # add further fields here
            }
        else:
            raise ItemException(self.data)

    #
    # Operator overload
    #

    def __repr__(self):
        return "Class " + __name__ + ".NewItem:\n" + json.dumps(self.data, indent=2)
