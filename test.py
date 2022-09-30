import requests
import os
import json
import sys 
import subprocess

def Sectrails(Domain):
    url = "https://api.securitytrails.com/v1/domain/"+Domain+"/subdomains?children_only=false&include_inactive=true"

    headers = {
        "accept": "application/json",
        "APIKEY": "I8ei5ZxqUZbY9EmR7YBQCw6NT7PDwwJX"
    }
    response = requests.get(url, headers=headers)
    jsondata=json.loads(response.text)
    data = jsondata["subdomains"]
    print("Printing all subdomains")
    for domain in data:
        print(f"{domain}.{sys.argv[1]}")
    print("\n")
    print("Printing the alive subdomains:\n")
    with open(os.devnull, 'w') as DEVNULL:
        for domain in data:
            subdomain = domain + "." + sys.argv[1]
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
                    os.system(f"echo {subdomain} >> alive.txt")
            except subprocess.CalledProcessError:
                is_up = False
    print("\n")
    
    print("Running Nuclei Scanner on the alive subdomains.\n")
    try:
        subprocess.run(["nuclei" , "-l" , "alive.txt" , "-o" , "nuclei.txt"])
    except:
        print("couldn't find nuclei in /usr/bin/nuclei")
    #subprocess.check_call(["/usr/bin/nuclei"] , )
    
   # print("Printing the dead subdomains:\n")
   # print("they might be alive can later...miracles are real :)\n")
   # for domain in data:
   #     subdomain = domain + "." + sys.argv[1]
   #     #print(subdomain)
   #     try:
   #         if(ping(subdomain, count=1)):
   #             pass
   #         else:
   #             print(f"{subdomain}")
   #     except:
   #         pass        
Sectrails(sys.argv[1])

