import requests
import sys

from bs4 import BeautifulSoup

if len(sys.argv):
    url = sys.argv[1]
    response = requests.get(url)
    print(response.status_code)
    print(response.headers)

    soup = BeautifulSoup(response.content, "lxml")
    print(soup.find("meta", {"name": "aircrafttype"})["content"])
    # div -> data-type="enroute"