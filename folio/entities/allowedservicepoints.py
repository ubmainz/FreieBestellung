#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

class AllowedServicePoints():
    """ This class holds a list of allowed service points (Abholtheken) e.g.:
    {"Page": [
        {
            "id": "8bf6f209-2b0d-425f-bbe2-a2323a694f1d",
            "name": "BB PHIL HFM"
        },
        {
            "id": "c200929e-444e-46a8-b7ac-961a83167dfe",
            "name": "BB UM Zahnklinik"
        }
    ]}
    """

    def __init__(self, servicepoints):
        self.__servicepoints = servicepoints

    @property
    def servicepoints(self):    
        return self.__servicepoints
