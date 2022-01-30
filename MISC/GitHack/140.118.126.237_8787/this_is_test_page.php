<!DOCTYPE html>
<form  method="GET">
  
<input type="text" name="url" placeholder='12%12%ereH02%LRU02%epyT' > 
<input type="submit" value="meow"> 
</form>

<?php

$ch = curl_init();

$options = array(
    CURLOPT_URL            => urldecode(strrev($_GET["url"])),
    CURLOPT_RETURNTRANSFER => true,   // return web page
    CURLOPT_HEADER         => true,  // don't return headers
    CURLOPT_FOLLOWLOCATION => true,   // follow redirects
    CURLOPT_MAXREDIRS      => 10,     // stop after 10 redirects
    CURLOPT_ENCODING       => "",     // handle compressed
    CURLOPT_USERAGENT      => $_SERVER['HTTP_USER_AGENT'], // name of client
    CURLOPT_AUTOREFERER    => true,   // set referrer on redirect
    CURLOPT_CONNECTTIMEOUT => 1,    // time-out on connect
    CURLOPT_TIMEOUT        => 1,    // time-out on response
); 

curl_setopt_array($ch,$options);
$result = curl_exec($ch);
curl_close($ch);

echo strrev($result);
?>
