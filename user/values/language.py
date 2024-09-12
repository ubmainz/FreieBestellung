#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

#
#
#

class Language():
    def __init__(self):
        self.__languages = ["de", "en"]

    def __call__(self, value):
        if value in self.__languages:
            return True
        else:
            return False

#
#
#

class LanguageValue(Language):
    def __init__(self):
        super().__init__()

    def __call__(self, value):
        if value == None:
            return 'de'
        elif super().__call__(value):
            return value
        else:
            return 'de' 
