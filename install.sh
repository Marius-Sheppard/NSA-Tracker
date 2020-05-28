echo '[NSA] Tracking Tool Updating...'
apt-get update > install.log
echo
echo '[NSA] Installing Dependencies...'
echo '    Python3'
apt-get -y install python3 python3-pip &>> install.log
echo '    PHP'
apt-get -y install php &>> install.log
echo '    ssh'
apt-get -y install ssh &>> install.log
echo '    Requests'
pip3 install requests &>> install.log
echo
echo '[-] Setting Permissions...'
chmod 777 template/NSA/php/info.txt
chmod 777 template/NSA/php/result.txt
echo
echo '[NSA] Tracking Tool Installed.'