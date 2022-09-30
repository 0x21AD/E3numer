import os 

if(os.system("ping -c 1 google.com")):
    print("host is up")