import httpx 
import subprocess
import requests 
import os 

hwid = str(str(subprocess.check_output('wmic csproduct get uuid')).strip().replace(r"\r", "").split(r"\n")[1].strip())
resp = httpx.get("") # put your link that is displayed once you run the server.py here, make sure its open port if your planning to use it!
if resp.text == "Authed":
    print("Your Authed, Congrats...")
    # code here, maybe call the function 
if resp.text == "Not Authed":
    print("Your Not Authed!")
    os.system("exit")
else:
    print("Error...")
