#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

import json

class FOLIOError():
    """This class represents an error in the format normally send from FOLIO as JSON string
    """

    def __init__(self, code, message:str, parameters=[]):
        self._message = message
        self._type = "error"
        self._code = code
        self._parameters = parameters

    @property
    def data(self):
        return {
            "errors": [{
                "message": self._message,
                "type": self._type,
                "code": self._code,
                "parameters": self._parameters
            }]
        }

    @property
    def json(self):
        return json.dumps(self.data)

    #
    # Operator overload
    #

    def __str__(self):
        return json.dumps(self.data, indent=2)

    def __repr__(self):
        return "Class " + __name__ + ".FOLIOError:\n" + json.dumps(self.data, indent=2)

    def __hash__(self):
        return hash(self._code, self._type, self._message)

    #
    # Getter methods
    #

    @property
    def message(self):
        return self._message

    @property
    def type(self):
        return self._type

    @property
    def code(self):
        return self._code

    @property
    def parameters(self):
        return self._parameters
