import flask 
from flask import Flask, request 

app = Flask(__name__)

@app.route("/hwids", methods=["POST"])
def hwid():
    hwid = request.form.get("hwid")
    hwids = open("Auth/hwids.txt")
    if(hwid in hwids.read()):
        print("(*) ! Authed User Logged In [%s]" % (hwid))
        return "Authed"
    else:
        return "Not Authed!"

@app.route("/status", methods=["GET"])
def status():
    try:
        return "Auth Is Online!"
    except Exception as err:
        return "Error: %s" % err
    
app.run("0.0.0.0", 80, debug=True)
