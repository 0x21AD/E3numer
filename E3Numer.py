#!/usr/bin/env python
from requests import get, RequestException
from os import system
from json import loads, JSONDecodeError
from sys import stdout, argv
from subprocess import run
from colorama import Fore, Style, Back

# API keys, add your api keysin API.py file
from API import wapplayzer_api_key, securityTrails_api_key

# color templates
ERROR = Back.RED + Fore.BLACK
ONGOING = Fore.YELLOW
DONE = Fore.GREEN + Back.LIGHTBLACK_EX
INPUT = Fore.LIGHTMAGENTA_EX
PHASE = Back.BLUE + Fore.WHITE
RESET = Style.RESET_ALL
IMPORTANT = Fore.CYAN

banner = """                                                                                
                     ($$$$$$$$$$$$$$$$Z^                                        
                    ^0$$$$$$$$$$$$$$$w;                                         
                    ~$$$$$$$$$$$$$$$#^                                          
                    `.      .t%$$$$b`                                           
         :}fpbka*q<         )B$$$$Q^                                            
      }8$$$$&#oox'         f$$$$$qI                                             
     I0B$8n^             .nB$$$$$$*z^                                           
     [M$8}               IrL$$$$$$$$W_                                          
    |$$$$$$$%x^              :Q@$$$$$pl  ,+++!.</}:i +++~" +++> ++++'"{)<. :)(>. 
  .u$$$hx[~l'                 ~W$$$$$a~  ld$$ad@$$B( ]$$$C C$$$| Y$$$pB$$$*L%$$$C^
 'U@$b!              '^      .vB$$$$$a<  Iq$$O" $$$L -$$$t J$$a~ u$$$l^Q$$W~,#$$w"
.xB$W+              "w$bJ{+}Yo$$$$$$@U'  Iq$$0^ $$$L -$$$[ J$$a~ u$$$; r$$W~ *$$w"
($$$oo$$$$B_        b$$$$$$$$$$$$$$@c    Iq$$0^ $$$L -$$$U C$$o~ u$$$I r$$W~ *$$q"
$$$$$BoZz?'         ~za@$$$$$$$$Bbf^     >k$$d! $$$a "0$$$88$$$/ O$$$} L$$8} #$$$i
^<;`.                  .`":;;;"`.        .^^^^.'^^^^  `,:'`^^^` ^^^^`  ^^^'. ^^^'

this tool reads your domain and pass it to this tool in purpose to automate recon
Subdomain Enum -> live subdomains -> gobuster subdomains -> nmap subdomains -> nuclei subdomain    
creators:       Zeyad Hassan (secYuri)    and     Ahmed Mamdouh (DeadDude) 
"""


# ----------------------------------------------Wapplayzer Integeration------------------------------------------------------
# this functions calls the API for the provided domain in the parameters, reads the json and print the results in a formated manner
def wapplayzer_report(Domain):
    print(PHASE + "Technology Detection Phase" + RESET)
    try:
        data = get("https://api.wappalyzer.com/v2/lookup/?urls=https://" + Domain,
                   headers={"x-api-key": wapplayzer_api_key})
        # format json and present results
        jsoned_data = loads(data.text)
        technologies = []
        versions = []
        result = []
        try:
            for one in jsoned_data[0]['technologies']:
                technologies.append(one['name'])
                try:
                    versions.append(one['versions'][0])
                except:
                    versions.append('unidentified')
        except RequestException:
            print(ERROR + "[!] WAPPALYZER REQUEST ERROR " + RESET)
        except JSONDecodeError:
            print(ERROR + "[!] WAPPALYZER RESPONSE ERROR " + RESET)
        except:
            print(ERROR + data.text + RESET)

        print(
            "----------------------------------------------------" + Domain + '----------------------------------------------------')
        for i in range(len(technologies) - 1):
            stdout.write("\t" + IMPORTANT + technologies[i] + "\t" + ONGOING + versions[i] + RESET + "\n")
            result.append([technologies[i], versions[i]])
    except:
        print(ERROR + "ERROR: COULND NOT ESTABLISH CONNECTION TO WAPPALYZER" + RESET)


# ----------------------------------------------SecTrails Integeration-------------------------------------------------------
# this function calls the security trails api for subdomain list of the apex domain
# read the json respones
# write them in alive.txt
# returns a list of the subdomains
def SecTrails(Domain):
    print(PHASE + " Subdomain Enumeration Phase " + RESET)
    url = "https://api.securitytrails.com/v1/domain/" + Domain + "/subdomains?children_only=false&include_inactive=true"

    headers = {
        "accept": "application/json",
        "APIKEY": securityTrails_api_key
    }
    response = get(url, headers=headers)
    jsondata = loads(response.text)
    data = jsondata["subdomains"]
    print(ONGOING + "Printing all subdomains" + RESET)
    for subdomain in data:
        print(f"{Fore.BLUE}\t{subdomain}.{Domain}" + RESET)
    print(ONGOING + "Printing the alive subdomains:" + RESET)
    """
    with open(devnull, 'w') as DEVNULL:
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
                    print( IMPORTANT + '\t' + subdomain)
                    system(f"echo https://{subdomain} >> alive.txt")
            except subprocess.CalledProcessError:
                is_up = False
                """
    print("\n")
    return data


# ----------------------------------------------Nuclei Integeration-------------------------------------------------------
# runs Nuclei for the alive subdomains that is saved in alive.txt
def Nuclei_Report():
    print(PHASE + "Vulnerability Scanning Phase" + RESET + "\n")
    try:
        run(["nuclei", "-l", "alive.txt", "-s", "low,medium,high,critical", "-o", "./NucleiReport.txt"])
    except:
        print(ERROR + "couldn't find nuclei in" + Fore.CYAN + " /usr/bin/nuclei" + Style.RESET_ALL)


# ----------------------------------------------Nmap automation-------------------------------------------------------
# runs nmap to scan the open ports of the provided domain and save the results in a file
def Nmap_Report(Domain):
    try:
        print(PHASE + "Service Scanning Phase" + RESET)
        print(f"{ONGOING}[+] Starting Nmap for {Fore.BLUE} {Domain} {Fore.MAGENTA}\n")
        system(f"nmap -sV -T4 {Domain} -o ./{Domain}/NmapReport.txt")
        print(RESET)
    except:
        print(ERROR + "Nmap could not run" + RESET)


# ----------------------------------------------wafw00f Integeration------------------------------------------------------
# checks if there is web applicatoin firewall (WAF)
def wafw00f_report(Domain):
    print(PHASE + "WAF Detection Phase" + RESET)
    try:
        system(f"wafw00f {Domain} -o ./{Domain}/WAF_Report.txt | grep 'is behind'")
        print('\n')
    # subprocess.check_call(["./bin/wafw00f", {Domain}, "-o", f"./{Domain}/WAF_Report.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("couldn't find wafw00f on /bin/")


# ----------------------------------------------gobuster Integeration------------------------------------------------------
# fuzz the directories of the provieded domain
def dirsearch(Domain):
    print(PHASE + "Directory Bruteforce Phase" + RESET)
    try:
        system(
            f"gobuster dir -q -u https://{Domain} --random-agent -w /usr/share/wordlists/dirb/common.txt --output='./{Domain}/Directories.txt'")
    except:
        print(
            "Couldn't conduct directory search, make sure you have gobuster and the common wordlist at /usr/share/wordlists/dirb/common.txt ")


# creates an html file that read all the outputs to be view from place
def create_Report(subdomain):
    with open(f"./{subdomain}/index.html", 'a') as f:
        content = "<html><head><title>Recon Report</title><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css' rel='stylesheet'><script src='https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js'></script><style>section{padding: 20px;}\niframe{color: green;background-color: white;}</style></head><body class='bg-dark text-bg-primary'><section class='row bg-dark text-bg-primary'><h1 class='center'>Report</h1><div class='col' id='nmap'><h1>Port Scan</h1><p class='container'><iframe style='color: green;background-color: white;' src='./NmapReport.txt' width='95%' height='800'></iframe></p></div><div class='col' id='dir'><h1>Busted Directories</h1><p class='container'><iframe style='color: green;background-color: white;' src='./Directories.txt' width='95%' height='800'></iframe></p></div><div class='col' id='waf'><h1>Detected WAF</h1><p class='container'><iframe style='color: green;background-color: white;' src='./WAF_Report.txt' width='95%' height='800'></iframe></p></div></section></body></html>"
        f.write(content)


if __name__ == "__main__":

    apexDomain = ""
    print(Fore.LIGHTGREEN_EX + banner + RESET)  # print banner
    apexDomain = argv[1] if len(argv) > 1 else input(INPUT + "Enter Apex Domain: ")

    while apexDomain == "":
        apexDomain = input(INPUT + "Enter Apex Domain: ")

    subdomains = SecTrails(apexDomain)
    for sub in subdomains:
        system("mkdir " + "./" + f'{sub}.{apexDomain}')  # create subdomain folder
        wafw00f_report(f'{sub}.{apexDomain}')
        wapplayzer_report(f'{sub}.{apexDomain}')
        Nmap_Report(f'{sub}.{apexDomain}')
        dirsearch(f'{sub}.{apexDomain}')
        create_Report(f'{sub}.{apexDomain}')
    Nuclei_Report()
