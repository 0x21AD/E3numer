import requests
import json
import re
import sys 

def Sectrails(Domain):
    url = "https://api.securitytrails.com/v1/domain/"+Domain+"/subdomains?children_only=false&include_inactive=true"

    headers = {
        "accept": "application/json",
        "APIKEY": "PSIVR3dTsXWZdfEBXGpvWwaWjvyyAB3Q"
    }

    response = requests.get(url, headers=headers)
    jsondata=json.loads(response.text)
    data = jsondata["subdomains"]
    for domain in data:
        print(f"{domain}.{sys.argv[1]}")
Sectrails(sys.argv[1])
