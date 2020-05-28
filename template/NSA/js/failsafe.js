function require(ip)
{//var url="https://whatismyipaddress.com/ip/";
//url=url.concat(ip);
var xhr=new XMLHttpRequest();
xhr.open('GET',"https://ipinfo.io/json",true);
xhr.send();
xhr.onreadystatechange=processRequest;
var ip;
var host;
var city;
var country;
var location;
var organisation;
var postalcode;

function processRequest(e)
{if(xhr.readyState==4 && xhr.status==200)
{var response=JSON.parse(xhr.responseText);
ip=response.ip;
host=response.hostname;
city=response.city;
country=response.country;
location=response.loc;
organisation=response.org;
postalcode=response.postal;
}}}