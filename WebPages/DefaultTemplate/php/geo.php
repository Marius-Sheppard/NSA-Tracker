<?php
header('Content-Type: text/html');
{

$lat=$_POST['Lat'];
$lon=$_POST['Lon'];
$acc=$_POST['Acc'];
$alt=$_POST['Alt'];
$dir=$_POST['Dir'];
$spd=$_POST['Spd']; 

$data['dev']=array();
$data['dev'][]=array('platform'=>$ptf,
'browser'=>$brw,'cores'=>$cc,
'ram'=>$ram,'vendor'=>$ven,
'render'=>$ren,'ip'=>$ip,
'ht'=>$ht,'wd'=>$wd,'os'=>$os,
'lang'=>$lang,'on'=>$on,'prod'=>$prod,
'lat'=>$lat,'lon'=>$lon,'acc'=>$acc,
'alt'=>$alt,'dir'=>$dir,'spd'=>$spd);
$jdata=json_encode($data);
$f=fopen('./../../../Output/Results.txt','w+');
fwrite($f,$jdata);
fclose($f);}
?>