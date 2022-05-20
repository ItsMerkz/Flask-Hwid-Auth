import flask 
from flask import Flask, request 

app = Flask(__name__)

@app.route("/hwids", methods=["POST"])
def hwid():
    hwid = request.form.get("hwid")
    hwids = open("Auth/hwids.txt")
    if(hwid in hwids.read()):
        return "Authed"
    else:
        return "Not Authed!"
    
app.run("0.0.0.0", 80, debug=True)
