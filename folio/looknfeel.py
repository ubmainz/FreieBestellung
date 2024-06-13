#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

class LookNFeel():
    """The LookNFeel class is used to switch the layout of the request form.
    RAW is pure HTML without any style (css) information, but the error indication: inline style "color:red".
    It just contains "name" attributes to make the markup work with the request-form script.
    So do whatever you want to with this HTML.
    """

    looks = [
        "HDS2",
        "OPAC",
        "RAW"
    ]

    separator = "/"

    def __init__(self, look :str):
        if look in LookNFeel.looks:
            self.__look = look 
        else:
            self.__look = self.default

    def __call__(self, site :str):
        return self.__look + LookNFeel.separator + site

    @property
    def look(self):
        return self.__look

    @property
    def default(self):
        return "HDS2"
