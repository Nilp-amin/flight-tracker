import requests
import sys
import json

from opensky_api import OpenSkyApi
from bs4 import BeautifulSoup

class Aircraft(object):
    commerical_call_ids = {
        "VOZ": "Virgin Australia",
        "JST": "Jet Star",
        "QJE": "Qantas Link"
    }
    def __init__(self, ads_b_data:dict):
        self.data = ads_b_data
        self.is_commercial = Aircraft.is_commercial_aircraft(self.data["callsign"])

    def look_up_info(self)->None:
        if self.is_commercial:
            print(f"Requesting endpoint at https://flightaware.com/live/flight/{self.data['callsign']}")
            req = requests.get(f"https://flightaware.com/live/flight/{self.data['callsign']}")
            print(f"Obtained response status code {req.status_code}")

            # Parse HTML
            soup = BeautifulSoup(req.content, "lxml")
            print(soup.find("meta", {"name": "aircrafttype"})["content"])
        else:
            # Make API call
            print(f"Requesting endpoint at https://www.casa.gov.au/search-centre/aircraft-register/{callsign}")
            req = requests.get(f"https://www.casa.gov.au/search-centre/aircraft-register/{callsign}")
            print(f"Obtained response status code {req.status_code}")

            # Parse HTML
            soup = BeautifulSoup(req.content, "lxml")
            print(soup.find_all("div", {"class": "field__label"})[0])
            for child in soup.find_all("div", {"class": "field__item"})[0].children:
                print(child.string)

    @staticmethod
    def is_commercial_aircraft(call_id:str)->bool:
        identifier = call_id[0:3]
        return identifier in Aircraft.commerical_call_ids.keys()

"""*1 *2
   *3 *4
"""
toowoomba_bbox = (-27.82065042845486, -27.33918011669274, 151.67275413394034, 152.1955775316677)
brisbane_bbox = (-27.925491172556544, -27.256274952594293, 152.7001978337609, 153.54413678561804)
australia_bbox = (-43.49442965153107, -8.7358402011794, 107.0424980296446, 161.324777867652) 

if __name__ == "__main__":
    # init data
    with open("api_details.json") as f:
        api_keys = json.load(f)
        opensky_api_keys = api_keys["openskyapi"]

    # aircraft ADS-B data
    api = OpenSkyApi(username=opensky_api_keys["username"], password=opensky_api_keys["password"])
    s = api.get_states(bbox=australia_bbox)
    for states in s.states:
        print(states)

    # satellite images (NASA: GIBS)
    if len(sys.argv):
        callsign = sys.argv[1]
        print(f"Requesting endpoint at https://www.casa.gov.au/search-centre/aircraft-register/{callsign}")
        req = requests.get(f"https://www.casa.gov.au/search-centre/aircraft-register/{callsign}")
        print(f"Obtained response status code {req.status_code}")

        # Parse HTML
        soup = BeautifulSoup(req.content, "lxml")
        print(soup.find_all("div", {"class": "field__label"})[0])
        for child in soup.find_all("div", {"class": "field__item"})[0].children:
            print(child.string)

        """
        tree = html.fromstring(req.content)
        items = tree.xpath('//div[@class="field__item"]/text()')
        print(items)
        """