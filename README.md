<img src="https://raw.githubusercontent.com/SecYuri/E3numer/master/logopresentation.jpg" alt="E3nummer logo">

## Installation

Make sure you have pip and python3 installed:

```bash
sudo apt-get install python3 -y
```

```bash
sudo apt-get install python3-pip
```

Clone the repo and do these steps:

```bash
git clone https://github.com/SecYuri/E3numer.git
chmod +x setup.sh
sudo ./setup.sh
```

## Usage

```bash
python3 E3numer.py
```

## Instructions

The tool is developed to automate the Recon and auditing process, It's been designed to be plug-in and play style, you need only need to specify the domain and it will

1.  take your domain and enumerate subdomains then filter for the live subdomains the tool
2.  pipe the live subdomains to check what technologies they run and their versions by integrating with wappalyzer
3.  It will also detect WAF presence and its type
4.  it will run gobuster against each alive subdomain found.
5.  it will Nmap scan again all live subdomains
6.  it will nuclei against every alive subdomain found

## API-Key

The tool is using [security trails](https://securitytrails.com/) and [wappalyzer](https://www.wappalyzer.com/api/) non-commercial api-keys, we strongly recommend you register an account on both and use your own api-keys to avoid quota errors.

## Hint

1. you will find directories created named after each alive subdomain found, under each directory, you will find `nmap.txt` , `gobuster.txt` , `waf result`,..etc.
   you will also file the `result.html` file that contains every information found that belongs to that subdomain, and this applies to each directory (for each subdomain found), The tool will generate a nuclei output file.
2. You might see some errors popping off to the terminal while the tool is running as the tool might try to Nmap a directory that doesn't respond or try to run gobuster against a randomly configured subdomain as the tool try to squeeze for every single piece of info, however, the tool will continue running until it finishes.

## Creators

https://www.linkedin.com/in/ahmed-mamdouh-b563081b6/

https://www.linkedin.com/in/ziad-hassan-a973441bb/
