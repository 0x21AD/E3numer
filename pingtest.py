import pythonping
domain="learn.thndr.app"
from pythonping import ping
try:
    if(ping(domain, count=1)):
        print("Printing the alive domains/subdomains:")
        print(f"{domain} \n")
        f=open("alive.txt" , "a")
        f.wirte("hi")
    else:
        pass
except:
    pass
f.close()