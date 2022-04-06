# URL Based Location Tracker
Tracking Tool based on open-source resources.  
Fingerprint and log geolocation data from devices (over LAN or WAN) visiting the target website.  
[NEW] Improved accuracy and better functionality.

## Install
```
git clone https://github.com/Marius-Sheppard/NSA-Tracker
cd NSA-Tracker
chmod +x ./Install.sh
sudo ./Install.sh
python3 ./NSA.py --help
```

## Making your own website from the template:
- Duplicate  the "DefaultTemplate" directory from ./WebPages/ 
- Rename the directory to your own template name
- Edit the coresponding html, css and js files to suit your needs
- Run the NSA.py script with the new template name as an argument 
```bash
cp -r DefaultTemplate ./WebPages/<your_template_name>
python3 NSA.py --site <your_template_name>
```
