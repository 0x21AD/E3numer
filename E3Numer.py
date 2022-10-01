from attr import define
from jinja2 import is_undefined
import requests
import os
import json
import sys 
import subprocess
apexDomain=""

def main(Domain):
    #----------------------------------------------Wapplayzer------------------------------------------------------
    try:
        data = requests.get( "https://api.wappalyzer.com/v2/lookup/?urls=https://" + Domain , headers ={"x-api-key": "ddbOUg8jMv7WC2wbhuEyn4KnZsuXLfNI2QbZsndu"})
        # format json and present results
        jsoned_data = json.loads(data.text)
        technologies = []
        versions = []
        result = []
        try:
            for one in jsoned_data[0]['technologies']:
                technologies.append(one['name'])
                try:
                    versions.append(one['versions'][0])
                except: versions.append('unidentified')
        except:
                print("[!] wappalyzer request error")
        
        print("----------------------------------------------------" + Domain +'----------------------------------------------------')
        for i in range(len(technologies)-1):
            sys.stdout.write("\t" + technologies[i] + "\t" + versions[i] + "\n")
            result.append([technologies[i],versions[i]])
    except:
        print("couldn't connect to wappalyzer")
    #----------------------------------------------SecTrails Integeration-------------------------------------------------------
    url = "https://api.securitytrails.com/v1/domain/"+Domain+"/subdomains?children_only=false&include_inactive=true"

    headers = {
        "accept": "application/json",
        "APIKEY": "nEIBWK6dvQLYpIKPLj9uVonZZ2wb02HO"
    }
    response = requests.get(url, headers=headers)
    jsondata=json.loads(response.text)
    data = jsondata["subdomains"]
    print("Printing all subdomains")
    for subdomain in data:
        print(f"{subdomain}.{Domain}")
    print("\n")
    print("Printing the alive subdomains:\n")
    with open(os.devnull, 'w') as DEVNULL:
        for domain in data:
            subdomain = domain + "." + Domain
            #print(subdomain)
            try:
                subprocess.check_call(
                ['ping', '-c', '4', subdomain],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
                )
                is_up = True
                if is_up:
                    print(subdomain)
                    os.system(f"echo https://{subdomain} >> alive.txt")
            except subprocess.CalledProcessError:
                is_up = False
    print("\n")
    #----------------------------------------------Nuclei Integeration-------------------------------------------------------
    print("Running Nuclei Scanner on the alive subdomains.\n")
    try:
        subprocess.run(["nuclei" , "-l" , "alive.txt" , "-s" , "low,medium,high,critical" , "-o" , "nuclei.txt"]) 
    except:
        print("couldn't find nuclei in /usr/bin/nuclei")
    #----------------------------------------------Nmap automation-------------------------------------------------------
    f = open("alive.txt" ,"r")
    lines=f.read().split("\n")
    for line in lines:
        print(f"[+] Starting Nmap for {line}\n")
        newline = line.replace("https://","")
        os.system(f"nmap -A -T4 -Pn {newline} -o {newline}.nmap") 
        print(line[8:])
    f.close()

try:
    main(sys.argv[1])
except:
    while apexDomain=="":
        apexDomain= input("Enter Apex Domain: ")
    main(apexDomain)
        
