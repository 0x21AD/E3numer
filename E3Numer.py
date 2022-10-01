import requests
import os
import json
import sys 
import subprocess
import colorama

apexDomain=""

# constants
wapplayzer_api_key = "sMSUWa5StM9OWbeDWsWj4259lZ1rTUDW5gciwdAn"
securityTrails_api_key =  "nEIBWK6dvQLYpIKPLj9uVonZZ2wb02HO"

ERROR = colorama.Back.RED + colorama.Fore.BLACK
ONGOING = colorama.Fore.YELLOW
DONE = colorama.Fore.GREEN + colorama.Back.LIGHTBLACK_EX
INPUT = colorama.Fore.LIGHTMAGENTA_EX
PHASE = colorama.Back.BLUE + colorama.Fore.WHITE
RESET = colorama.Style.RESET_ALL
IMPORTANT = colorama.Fore.CYAN


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

#----------------------------------------------Wapplayzer Integeration------------------------------------------------------

def wapplayzer_report(Domain):
    print(PHASE + "Technology Detection Phase" + RESET)
    try:
        data = requests.get( "https://api.wappalyzer.com/v2/lookup/?urls=https://" + Domain , headers ={"x-api-key": wapplayzer_api_key})
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
        except requests.RequestException:
            print(ERROR + "[!] WAPPALYZER REQUEST ERROR " + RESET)
        except json.JSONDecodeError:
            print(ERROR + "[!] WAPPALYZER RESPONSE ERROR " + RESET)
        except:
            print(ERROR + data.text + RESET)

        print("----------------------------------------------------" + Domain +'----------------------------------------------------')
        for i in range(len(technologies)-1):
            sys.stdout.write("\t" + IMPORTANT + technologies[i] + "\t" + ONGOING + versions[i] + RESET + "\n")
            result.append([technologies[i],versions[i]])
    except:
        print(ERROR + "ERROR: COULND NOT ESTABLISH CONNECTION TO WAPPALYZER" + RESET)


#----------------------------------------------SecTrails Integeration-------------------------------------------------------

def SecTrails(Domain):
    print(PHASE + " Subdomain Enumeration Phase " + RESET)
    url = "https://api.securitytrails.com/v1/domain/"+Domain+"/subdomains?children_only=false&include_inactive=true"

    headers = {
        "accept": "application/json",
        "APIKEY": securityTrails_api_key
    }
    response = requests.get(url, headers=headers)
    jsondata=json.loads(response.text)
    data = jsondata["subdomains"]
    print(ONGOING + "Printing all subdomains" + RESET)
    for subdomain in data:
        print(f"{colorama.Fore.BLUE}\t{subdomain}.{Domain}" + RESET)
    print(ONGOING + "Printing the alive subdomains:" + RESET)
    """
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
                    print( IMPORTANT + '\t' + subdomain)
                    os.system(f"echo https://{subdomain} >> alive.txt")
            except subprocess.CalledProcessError:
                is_up = False
                """
    print("\n")
    return data
    

#----------------------------------------------Nuclei Integeration-------------------------------------------------------

def Nuclei_Report():
    print(PHASE +"Vulnerability Scanning Phase" + RESET + "\n")
    try:
        subprocess.run(["nuclei" , "-l" , "alive.txt" , "-s" , "low,medium,high,critical" , "-o" , "./NucleiReport.txt"]) 
    except:
        print(ERROR + "couldn't find nuclei in" + colorama.Fore.CYAN + " /usr/bin/nuclei" + colorama.Style.RESET_ALL)

#----------------------------------------------Nmap automation-------------------------------------------------------

def Nmap_Report(Domain):
    try:
        print(PHASE + "Service Scanning Phase"+ RESET)
        print(f"{ONGOING}[+] Starting Nmap for {colorama.Fore.BLUE} {Domain} {colorama.Fore.MAGENTA}\n")
        os.system(f"nmap -sV -T4 {Domain} -o ./{Domain}/NmapReport.txt")
        print(RESET)
    except:
        print(ERROR + "Nmap could not run"+ RESET)

#----------------------------------------------wafw00f Integeration------------------------------------------------------

def wafw00f_report(Domain):
    print(PHASE + "WAF Detection Phase" + RESET)
    try:
        os.system(f"wafw00f {Domain} -o ./{Domain}/WAF_Report.txt | grep 'is behind'")
        print('\n')
       # subprocess.check_call(["./bin/wafw00f", {Domain}, "-o", f"./{Domain}/WAF_Report.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("couldn't find wafw00f on /bin/")

#----------------------------------------------dirsearch Integeration------------------------------------------------------

def dirsearch(Domain):
    print(PHASE + "Directory Bruteforce Phase" + RESET)
    try:
        os.system(f"gobuster dir -q --url https://{Domain} --random-agent --wordlist /usr/share/wordlists/dirb/common.txt --output='./{Domain}/Directories.txt'")
    except:
        print("Couldn't conduct directory search, make sure you have gobuster and the common wordlist at /usr/share/wordlists/dirb/common.txt ")


def create_Report(subdomain):
    f= open(f"./{subdomain}/index.html", 'a')
    content = "<html><head><title>Recon Report</title><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.cs' rel='stylesheet'><script src='https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.j'></script><style>section{padding: 20px;}\niframe{color: green;background-color: white;}</style></head><body class='bg-dark text-bg-primary'><section class='row bg-dark text-bg-primary'><h1 class='center'>Report</h1><div class='col' id='nmap'><h1>Port Scan</h1><p class='container'><iframe style='color: green;background-color: white;' src='./NmapReport.txt' width='95%' height='800'></iframe></p></div><div class='col' id='dir'><h1>Busted Directories</h1><p class='container'><iframe style='color: green;background-color: white;' src='./Directories.txt' width='95%' height='800'></iframe></p></div><div class='col' id='waf'><h1>Detected WAF</h1><p class='container'><iframe style='color: green;background-color: white;' src='./WAF_Report.txt' width='95%' height='800'></iframe></p></div></section></body></html>"
    f.write(content)
    f.close()
    
if __name__ == "__main__":
    def main():
        apexDomain = ""
        print(colorama.Fore.LIGHTGREEN_EX + banner + RESET)
        try:
            subdomains = SecTrails(sys.argv[1])
            for sub in subdomains:
                os.system("mkdir " + "./" + sub + "." + sys.argv[1])
                wafw00f_report(sub + "." +sys.argv[1])
                wapplayzer_report(sub + "." + sys.argv[1])
                Nmap_Report(sub + "." + sys.argv[1])
                dirsearch(sub + "." + sys.argv[1])
                create_Report(sub + "." + sys.argv[1])
            Nuclei_Report()

        except:
            while apexDomain == "":
                apexDomain= input(INPUT + "Enter Apex Domain: ") 
            subdomains = SecTrails(apexDomain)
            for sub in subdomains:
                os.system("mkdir " + "./" + sub + "." + apexDomain)    # create subdomain file
                wafw00f_report(sub + "." + apexDomain)      
                wapplayzer_report(sub + "." + apexDomain)
                Nmap_Report(sub + "." + apexDomain)
                dirsearch(sub + "." + apexDomain)
                create_Report(sub + "." + apexDomain)
            Nuclei_Report()            
    main()

# run plz