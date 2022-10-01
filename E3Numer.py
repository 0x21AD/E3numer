import requests
import os
import json
import sys 
import subprocess
import colorama

apexDomain=""

# constants
wapplayzer_api_key = "ddbOUg8jMv7WC2wbhuEyn4KnZsuXLfNI2QbZsndu"
securityTrails_api_key =  "1QIJWVHfK0UtBOiDuINEOoOOEkFXXXD1"

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
                                                                                
"""




def main(Domain):
    #----------------------------------------------Wapplayzer------------------------------------------------------
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
        except requests.JSONDecodeError:
            print(ERROR + "[!] WAPPALYZER RESPONSE ERROR " + RESET)
        except:
            print(ERROR + "UNKNOWN ERROR" + RESET)

        print("----------------------------------------------------" + Domain +'----------------------------------------------------')
        for i in range(len(technologies)-1):
            sys.stdout.write("\t" + IMPORTANT + technologies[i] + "\t" + ONGOING + versions[i] + RESET + "\n")
            result.append([technologies[i],versions[i]])
    except:
        print(ERROR + "ERROR: COULND NOT ESTABLISH CONNECTION TO WAPPALYZER" + RESET)
    
    #----------------------------------------------SecTrails Integeration-------------------------------------------------------
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
    print("\n")
    
    #----------------------------------------------Nuclei Integeration-------------------------------------------------------
    print(PHASE +"Vulnerability Scanning Phase" + RESET + "\n")
    try:
        subprocess.run(["nuclei" , "-l" , "alive.txt" , "-s" , "low,medium,high,critical" , "-o" , "nuclei.txt"]) 
    except:
        print(ERROR + "couldn't find nuclei in" + colorama.Fore.CYAN + " /usr/bin/nuclei" + colorama.Style.RESET_ALL)
    
    #----------------------------------------------Nmap automation-------------------------------------------------------
    print(PHASE + "Service Scanning Phase")
    f = open("alive.txt" ,"r")
    lines=f.read().split("\n")
    for line in lines:
        print(f"{ONGOING}[+] Starting Nmap for {colorama.Fore.BLUE} {line} {RESET}\n")
        newline = line.replace("https://","")
        os.system(f"nmap -A -T4 -Pn {newline} -o {newline}.nmap") 
    f.close()

print(colorama.Fore.LIGHTGREEN_EX + banner + RESET)

try:
    main(sys.argv[1])
    quit()
except IndexError:
    while apexDomain=="":
        apexDomain= input(INPUT + "Enter Apex Domain: ") ##############
    main(apexDomain)
    quit()
except: quit()