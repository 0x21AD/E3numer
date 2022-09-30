#!/bin/python
import subprocess
print("Running Nuclei Scanner on the alive subdomains.\n")
try:
    subprocess.run(["nuclei" , "-l" , "alive.txt" , "-s" , "low,medium,high,critical" , "-o" , "nuclei.txt"]) 
except:
    print("couldn't find nuclei in /usr/bin/nuclei")    