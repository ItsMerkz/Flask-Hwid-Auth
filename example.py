import httpx 
import subprocess
import requests 
import os 
import json 

config = json.load(open("config.json", encoding="utf-8", errors="ignore"))

hwid = str(str(subprocess.check_output('wmic csproduct get uuid')).strip().replace(r"\r", "").split(r"\n")[1].strip())
resp = requests.post("%s/hwids" % (config["Server"]["Url"]), data={"hwid": hwid}) 
if resp.text == "Authed":
    print("Your Authed, Congrats...")
    # code here, maybe call the function 
elif resp.text == "Not Authed!":
    print("Send Your Hwid To An Owner [%s]" % (hwid))
    os.system("exit")
else:
    print("Error...")
