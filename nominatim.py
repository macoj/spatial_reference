__author__ = 'marcos'
import re
import json
import urllib2


class Nominatim():
    def __init__(self):
        pass

    @staticmethod
    def nominatim_get_bounding_box_of(street=None, city=None, county=None, state=None,
                                      postalcode=None, country=None, polygon=True):
        assert street or city or county or state or postalcode or country, "input we weed"
        parameters = ['street', 'city', 'county', 'state', 'postalcode', 'country']
        input_parameters = [street, city, county, state, postalcode, country]
        url_input = [parameters[i] + "=" + str(re.sub(" ", "+", input_parameters[i]))
                     for i in range(len(parameters)) if input_parameters[i] is not None]
        url_input = "http://nominatim.openstreetmap.org/search?" + "&".join(url_input) + "&format=json"
        url_open = urllib2.urlopen(url_input)
        result = json.load(url_open)
        if polygon:
            if len(result) > 0:
                bb = map(float, result[0]['boundingbox'])
                result = bb[:4]
        return result