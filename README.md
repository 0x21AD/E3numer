# E3numer
## Installation
### make sure you have pip and python3
### clone the repo and chmod +x setup.sh
### sudo ./setup.sh and you are ready to go

## Usage 
### python3 E3numer.py  OR python3 E3numer.py

#### Tool is developed to automate the Recon and auditing process, It's been designed to be plug-in and play style , you need only need to specify the domain and it will: #### 1. take your domain and enumerate subdomains then filter for the live subdomains the tool 
#### 2.pipe the live subdomains to check what technologies they run and their versions by integrating with wappalyzer 
#### 3. It will also detect for WAF presence and it's type 
#### 4. it will run gobuster against each alive subdomain found.
#### 5. it will nmap scan again all live subdomains
#### 6. it will nuclei against every alive subdomain found

## Api-Key
The tool is using security trails and wappalyzer non-commercial api-keys, we strongly recommend you to register account on both and use your own api-keys to avoid quota errors.

## Hint
#### 1.you will find directories created named after each alive subdomain found, under each directory you will find nmap.txt , gobuster.txt , waf result ,..etc. you will also file result.html file that contains every information found belongs to that subdomain, and this applies to each directory(for each subdomain found), the tool will generate a nuclei output file.
#### 2.you might see some errors popping off to the terminal while the tool is running as the tool might try to nmap a directory which doesn't respond or try a to run gobuster against random configured subdomain as the tool try to sequeeze for every single piece of info, however the tool will continue running until it finishes.

### Creators
https://www.linkedin.com/in/ahmed-mamdouh-b563081b6/ 
https://www.linkedin.com/in/zeyad-hassan-a973441bb/

