#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "[NSA-TRACKER]: Please run as ROOT!"
  exit
fi

LOG_DIR="./Logs/"
if ! [[ -d "$LOG_DIR" ]]; then
  mkdir Logs
fi

TEMPLATES="./Webpages/"
if ! [[ -d "$TEMPLATES" ]]; then
  echo "[NSA-TRACKER]: Missing Templates!"  
  exit
fi

OUTPUT_DIR="./Output/"
if ! [[ -d "$OUTPUT_DIR" ]]; then
  mkdir Output
fi

echo '[NSA-TRACKER]: Updating...'
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null &&
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list >/dev/null  &&
apt-get update > ./Logs/Install.log
echo '[NSA-TRACKER]: Installing Dependencies...'
echo '[+] Python3'
apt-get -y install python3 python3-pip &>> ./Logs/Install.log
echo '[+] PHP'
apt-get -y install php &>> ./Logs/Install.log
echo '[+] SSH'
apt-get -y install ssh &>> ./Logs/Install.log
echo '[+] Python3 Requests'
pip3 install requests &>> ./Logs/Install.log
echo '[+] Ngrok Tunnel'
apt-get install ngrok &>> ./Logs/Install.log      
echo '[NSA-TRACKER] Setting Permissions...'
touch ./Output/Info.txt
chmod 777 ./Output/Info.txt
touch ./Output/Results.txt
chmod 777 ./Output/Results.txt
touch ./Output/Results.csv
echo "Captures" > ./Output/Results.csv
echo '[NSA-TRACKER] Tracking Tool Installed.'