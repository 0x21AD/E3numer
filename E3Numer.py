import requests
import os
import json
import sys
import subprocess
import colorama
from random import choice
import validators

apexDomain=""

# API keys, add your api keys her
wapplayzer_api_key = "sMSUWa5StM9OWbeDWsWj4259lZ1rTUDW5gciwdAn" # REMOVE BEFORE PUBLISHING
securityTrails_api_key =  "PjZjxGoqfRo1zqL6drUqaj3bESlEQUdg"	# REMOVE BEFORE PUBLISHING

# color templates
ERROR     = colorama.Fore.BLACK  + colorama.Back.RED
ONGOING   = colorama.Fore.YELLOW + colorama.Back.BLACK
DONE      = colorama.Fore.GREEN  + colorama.Back.BLACK
INPUT     = colorama.Fore.WHITE  + colorama.Back.BLACK
PHASE     = colorama.Fore.BLUE   + colorama.Back.BLACK
IMPORTANT = colorama.Fore.CYAN   + colorama.Back.BLACK
RESET     = colorama.Style.RESET_ALL


banner = ["""
       ____                           
      |___ \                          
  ___   __) | _ __   _   _  _ __ ___  
 / _ \ |__ < | '_ \ | | | || '_ ` _ \ 
|  __/ ___) || | | || |_| || | | | | |
 \___||____/ |_| |_| \__,_||_| |_| |_|

""",
"""
 _______  ______   _                 _______ 
(  ____ \/ ___  \ ( (    /||\     /|(       )
| (    \/\/   \  \|  \  ( || )   ( || () () |
| (__       ___) /|   \ | || |   | || || || |
|  __)     (___ ( | (\ \) || |   | || |(_)| |
| (            ) \| | \   || |   | || |   | |
| (____/\/\___/  /| )  \  || (___) || )   ( |
(_______/\______/ |/    )_)(_______)|/     \|

""",
"""
             ____                                   
   ____     F___ J    _ ___     _    _    _ _____   
  F __ J    `-__| L  J '__ J   J |  | L  J '_  _ `, 
 | _____J    |__  (  | |__| |  | |  | |  | |_||_| | 
 F L___--..-____] J  F L  J J  F L__J J  F L LJ J J 
J\______/FJ\______/FJ__L  J__LJ\____,__LJ__L LJ J__L
 J______F  J______F |__L  J__| J____,__F|__L LJ J__|

"""
]
statment = IMPORTANT + """
this tool reads your domain and pass it to these tools in purpose to automate recon
creators: 	Zeyad Hassan (secYuri), Ahmed Mamdouh (DeadDude)
""" + RESET




#----------------------------------------------Wapplayzer Integeration------------------------------------------------------
# this functions calls the API for the provided domain in the parameters, reads the json and print the results in a formated manner
def wapplayzer_report(Domain):
	print(PHASE + "Technology Detection Phase " + ONGOING  + " " + Domain + RESET)
	try:
		data = requests.get( "https://api.wappalyzer.com/v2/lookup/?urls=https://" + Domain , headers ={"x-api-key": wapplayzer_api_key})
        # format json and present results
		jsoned_data = json.loads(data.text)
		technologies = []
		versions = []
		result = []
		# list extracted data in arrays
		try:
			for one in jsoned_data[0]['technologies']:
				technologies.append(one['name'])
				try: versions.append(one['versions'][0])
				except IndexError: versions.append('unidentified')
		
		except requests.RequestException:
			print(ERROR + "[!] WAPPALYZER REQUEST ERROR " + RESET)
		
		except json.JSONDecodeError:
			print(ERROR + "[!] WAPPALYZER RESPONSE ERROR " + RESET)
		
		except:
			print(ERROR + data.text + RESET)
		# print results to the user
		for i in range(len(technologies)-1):
			sys.stdout.write("\t" + IMPORTANT + technologies[i] + "\t" + ONGOING + versions[i] + RESET + "\n")
			result.append([technologies[i],versions[i]])
	
	except:
		print(ERROR + "ERROR: COULND NOT ESTABLISH PROPER CONNECTION WITH WAPPALYZER" + RESET)




#----------------------------------------------SecTrails Integeration-------------------------------------------------------
# this function calls the security trails api for subdomain list of the apex domain
def SecTrails(Domain):
	print(PHASE + "Subdomain Enumeration Phase " + RESET)
	# creating the request
	url = "https://api.securitytrails.com/v1/domain/"+Domain+"/subdomains?children_only=false&include_inactive=true"
	headers = {
		"accept": "application/json",
		"APIKEY": securityTrails_api_key
	}
	# calling the API
	try:
		response = requests.get(url, headers=headers)
		
		# formating the requested data
		jsondata=json.loads(response.text)
		data = jsondata["subdomains"]
		print(ONGOING + "[~] Listing subdomains" + RESET)

		for subdomain in data:
			print(f"\t{subdomain}.{Domain}" + RESET)
		print(ONGOING + "\n[~] Listing live subdomains:" + RESET)

		with open(os.devnull, 'w') as DEVNULL:
			for sub in data:
				subdomain = sub + "." + Domain
				is_up = False	# default status
				
				try:	
					subprocess.check_call(
					['ping', '-c', '2', subdomain],
					stdout=DEVNULL,
					stderr=DEVNULL
					)
					is_up = True
					if is_up:
						print( DONE + '\t' + subdomain)
						os.system(f"echo https://{subdomain} >> alive.txt")
				
				except subprocess.CalledProcessError:
					is_up = False
	
		print(RESET+"\n")
		return data

	except requests.RequestException:
		print(ERROR + "[!] failed to establish connection with securtiy trails API")

	except json.JSONDecodeError:
		print(ERROR + "[!] could not read response properly")

	except:
		print(ERROR + "[!] " + response.text)

	print("\n")




#----------------------------------------------Nuclei Integeration-------------------------------------------------------
# runs Nuclei for the alive subdomains that is saved in alive.txt
def Nuclei_Report():
	print(PHASE +"[~] Vulnerability Scanning Phase " + RESET + "\n")
	try:
		subprocess.run(["nuclei" , "-l" , "alive.txt" , "-s" , "low,medium,high,critical" , "-o" , "./NucleiReport.txt"])
	except:
		print(ERROR + "couldn't find nuclei in" + RESET + IMPORTANT + " /usr/bin/nuclei" + RESET)
		print(IMPORTANT + "download NUCLEI tool " + ONGOING + "sudo apt install nuclei" + RESET)

# run nuclei for one domain
def Nuclei_Report(domain):
	print(PHASE +"[~] Vulnerability scanning phase for " + domain + RESET + "\n")
	try:
		subprocess.run(["nuclei" , "-u" , domain , "-s" , "low,medium,high,critical" , "-o" , "./NucleiReport.txt"])
	except:
		print(ERROR + "couldn't find nuclei in" + RESET + IMPORTANT + " /usr/bin/nuclei" + RESET)
		print(IMPORTANT + "download NUCLEI tool " + ONGOING + "sudo apt install nuclei" + RESET)




#----------------------------------------------Nmap automation-------------------------------------------------------
# runs nmap to scan the open ports of the provided domain and save the results in a file
def Nmap_Report(Domain):
	try:
		print(PHASE + "[~] Service Scanning Phase " + ONGOING + " " + Domain)
		print(RESET)
		os.system(f"nmap -sV -T4 {Domain} -o ./{Domain}/NmapReport.txt")
		print(RESET)
	
	except OSError:
		print(ERROR + "Nmap could not run"+ RESET)
		print(IMPORTANT + "install nmap: " + ONGOING + "sudo apt install nmap" + RESET)
		print(IMPORTANT + "then try running it again for " + Domain + RESET)
	
	except:
		print(ERROR + " Error occured while running Nmap " + RESET)




#----------------------------------------------wafw00f Integeration------------------------------------------------------
# checks if there is web applicatoin firewall (WAF)
def wafw00f_report(Domain):
	print(PHASE + "[~] WAF Detection Phase " + ONGOING + " " + Domain + RESET)
	
	try:
		os.system(f"wafw00f {Domain} -o ./{Domain}/WAF_Report.txt | grep 'is behind'")
		print('\n')
	
	except OSError:
		print(ERROR + " couldn't find " + IMPORTANT + " /bin/wafw00f " + RESET)
		print(IMPORTANT + "install wafw00f then try running it again for " + Domain + RESET)
	
	except IndexError:
		print(ERROR + " ERROR: wafw00f failed to detect WAF " + RESET)
	
	finally:
		print(ERROR + " Error occured while running wafw00f " + RESET)




#----------------------------------------------Gobuster Integeration------------------------------------------------------
# fuzz the directories of the provieded domain
def dirsearch(Domain):
	print(PHASE + "[~] Directory Fuzzing Phase " + IMPORTANT + " " + Domain + RESET)

	try:
		os.system(f"gobuster dir -q --url https://{Domain} --random-agent --wordlist /usr/share/wordlists/dirb/common.txt --output='./{Domain}/Directories.txt'")
    
	except:
		print("Couldn't conduct directory search, make sure you have gobuster and the common wordlist at /usr/share/wordlists/dirb/common.txt ")




#--------------------------------------------------------------------------------------------------------------------------
# creates an html file that read all the outputs to be view from place
def create_Report(subdomain):
	try:
		f= open( subdomain+"/index.html", 'w')
		content = "<html><head><title>Recon Report</title><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css' rel='stylesheet'><script src='https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js'></script><style>section{padding: 20px;}\niframe{color: green;background-color: white;}</style></head><body class='bg-dark text-bg-primary'><section class='row bg-dark text-bg-primary'><h1 class='center'>" + subdomain + " Report</h1><div class='col' id='nmap'><h2>Port Scan</h2><p class='container'><iframe style='color: green;background-color: white;' src='./NmapReport.txt' width='95%' height='800'></iframe></p></div><div class='col' id='dir'><h2>Busted Directories</h2><p class='container'><iframe style='color: green;background-color: white;' src='./Directories.txt' width='95%' height='800'></iframe></p></div><div class='col' id='waf'><h2>Detected WAF</h2><p class='container'><iframe style='color: green;background-color: white;' src='./WAF_Report.txt' width='95%' height='800'></iframe></p></div></section></body></html>"
		f.write(content)
		f.close()
	except:
		print(ERROR + " COULD NOT WRITE REPORT FILE " + RESET)



#------------------------------------------Main function------------------------------------------------------


if __name__ == "__main__":

	print(ONGOING + choice(banner) + RESET)
	print(IMPORTANT + statment + RESET)

	def process(subdomain):
		os.system("mkdir " + "./" + subdomain)
		wafw00f_report		(subdomain)
		wapplayzer_report	(subdomain)
		Nmap_Report			(subdomain)
		dirsearch			(subdomain)
		create_Report		(subdomain)


	def main():
		if len(sys.argv)==2 :
			subdomains = SecTrails(sys.argv[1])
			try:
				for sub in subdomains:
					process(f"{sub}.{sys.argv[1]}")
			except IndexError:
				if len(subdomains)<2:
					print(ERROR + "could not fetch subdomains" + RESET)
					print(ONGOING + "[~] running on the main domain only" + RESET)
					process(sys.argv[1])
					quit()
				else:
					print(colorama.Fore.RED + "A non-fatal error occured during running subdomain enumeration" + RESET)
					for sub in subdomains: 
						process(f"{sub}.{sys.argv[1]}")

		# take user input if was not provided as an argument
		else:
			apexDomain = ""
			while apexDomain == "":
				apexDomain= input(INPUT + "Enter Apex Domain: ")
				print(RESET)

			subdomains = SecTrails(apexDomain)

			for sub in subdomains:
				process(f"{sub}.{apexDomain}")

	main()
	Nuclei_Report()

# run plz

#TODO:
	# must add validators.domain({Apex Domain}) for invalid input at a suitable location
	# nmap can output in xml format, maybe we could render that in the report in  much more readable way
