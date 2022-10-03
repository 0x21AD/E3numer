pip3 install -r requirements.txt
apt install dirsearch wafw00f -y
git clone https://github.com/projectdiscovery/nuclei.git 
cd nuclei/v2/cmd/nuclei/
go build .
cp nuclei /usr/local/bin
