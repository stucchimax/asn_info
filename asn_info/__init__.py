
import os
import requests

from dotenv import load_dotenv 

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
        total=8,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )

load_dotenv()

class Asns:
    def __init__(self):
        
        self.asns = {}

    def load_asn_data(self, add_manrs_data = False):

        url = "https://ftp.ripe.net/ripe/asnames/asn.txt"

        q = requests.Session()

        p = q.get(url, timeout=20)

        for line in p.iter_lines():
            split_line = line.decode().split(", ")
            
            try:
                country = split_line[1]
                split_line.pop(1)
            except:
                country = "ZZ"

            as_details = split_line[0].split()

            asn = int(as_details[0])
            
            as_details.pop(0)
            
            try:
                as_name = ' '.join(as_details)
            except:
                as_name = "None/Reserved"

            self.asns[asn] = {"country": country, "as_name": as_name}
        
        if add_manrs_data == True:
            self.manrs_data = True
            self.load_manrs_asn_data()
        else:
            self.manrs_data = False

    def load_manrs_asn_data(self):

        url = "https://api.manrs.org/asns/info"

        headers = {
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(os.getenv("MANRS_API_KEY"))
                }
        q = requests.Session()

        p = q.get(url, timeout=20, headers=headers)

        manrs_asns = p.json()
        
        for asn in manrs_asns['asns']:
            if asn['number'] in self.asns:
                self.asns[asn['number']]['manrs'] = asn['manrs']


    def get_as_name(self, asn):
        if asn in self.asns:
            return(self.asns[asn]["as_name"])
        else:
            return("Name not available")

    def get_as_country(self, asn):
        if asn in self.asns:
            return(self.asns[asn]["country"])
        else:
            return("ZZ")

    def is_manrs_participant(self, asn):
        if self.manrs_data == True:
            if asn in self.asns:
                return(self.asns[asn]["manrs"])
            else:
                return(False)
        else:
            return("No MANRS Data available")

