from flask import Flask, render_template, request, redirect
import pickledb as dbms
import werkzeug
from random import randint
import pickle
import requests

ipdb = dbms.load("ips.json", True)

class User(object):
    def __init__(self, ip, userid=1, *args, **kwargs):
        self.ip = ip
        self.userid = "#" + str(randint(100000,999999))
    def getId(self):
        return self.userid
    def getIp(self):
        return self.ip
    def commitChanges(self):
        ipdb.set(self.ip, self.userid)

# DB Initialization
# END DB Initialization

true = True
false = False


app = Flask("Hilda's Favour")
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/application')
def formx():
    User(request.remote_addr).commitChanges()
    return render_template('form.html')

@app.route('/processform', methods = ['GET', 'POST'])
def processform():
    webhookdata = {
  "username": request.args.get("name"),
  "avatar_url": "https://i.imgur.com/4M34hi2.png",
  "embeds": [
    {
      "author": {
        "name": str(request.args.get("name")),
        "url": "https://www.reddit.com/r/cats/",
        "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
      },
      "title": "New Application",
      "url": "https://HildasFavour0.foundingtitan.repl.co/",
      "description": "A new application has been submitted from **"+str(request.args.get("name"))+"**",
      "color": 15258703,
      "fields": [
        {
          "name": "Why I wanna apply",
          "value": str(request.args.get("why")),
          "inline": false
        }
      ],
      "thumbnail": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/4-Nature-Wallpapers-2014-1_ukaavUI.jpg"
      },
      "image": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/A_picture_from_China_every_day_108.jpg"
      },
      "footer": {
        "text": "Woah! So cool! :smirk:",
        "icon_url": "https://i.imgur.com/fKL31aD.jpg"
      }
    }
  ]
}
    x = requests.request("POST", "https://discord.com/api/webhooks/844951692344033290/tO-lADL0PHinhoGVbx-LcEpBv8R5FMMfTcPyz-2UTfkH3UDwcAWkLTkAnuqTguNZitT9", json=webhookdata)

    return redirect("/thankyou")

@app.route('/thankyou')
def thanks():
    return render_template("welcome.html")

app.run(host="0.0.0.0")