from flask import Flask, render_template, request, redirect, make_response
import pickledb as dbms
import werkzeug
from random import randint
import pickle
import requests

ipdb = dbms.load("ips.json", True)
conf = dbms.load("config.json", True)

appsopen = "yes"

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
if conf.get("WEBHOOK_URL") == False:
    conf.set("WEBHOOK_URL","https://discord.com/api/webhooks/844969245553328198/_FLIEqb-TxXVugcUtGTPbEJgMz8tnr7QgxjKaqUztfJdIesRnhhQnerDXkkweGx3CiSn")
    conf.dump()
if conf.get("ADMINCOOKIE") == False:
    conf.set("ADMINCOOKIE", "adminCookie98608")
    conf.dump()
if conf.get("MASTERKEY") == False:
    conf.set("MASTERKEY", "keyMaster9988")
if conf.get("MASTERPASS") == False:
    conf.set("MASTERPASS", "defpass")
if conf.get("VIEWS") == False:
    conf.set("VIEWS", 0)


WEBHOOK_URL = conf.get("WEBHOOK_URL")
ADMINCOOKIE = conf.get('ADMINCOOKIE')
MASTERKEY = conf.get("MASTERKEY")
MASTERPASS = conf.get("MASTERPASS")
print(WEBHOOK_URL)

app = Flask("Hilda's Favour")
app.config['TEMPLATES_AUTO_RELOAD'] = True

def addviews(no = 1):
    conf.set('VIEWS', int(conf.get('VIEWS'))+int(no))

@app.route('/')
def index():
    addviews()
    return render_template('index.html', appsopen=appsopen)

@app.route('/application')
def formx():
    if not ipdb.get(request.remote_addr):
        User(request.remote_addr).commitChanges()
    addviews()
    return render_template('form.html', appsopen=appsopen)

@app.route('/toggleapps')
def toogleapps():
    global appsopen
    apx = appsopen
    if apx=="yes":
        appsopen="no"
    if apx=="no":
        appsopen="yes"
    return "done"

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
        },
        {
          "name": "ID",
          "value": ipdb.get(request.remote_addr),
          "inline": true
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
    x = requests.request("POST", WEBHOOK_URL, json=webhookdata)
    del x
    return redirect("/thankyou")

@app.route('/thankyou')
def thanks():
    return render_template("welcome.html")

@app.route('/admin/')
def adminredir():
    addviews()
    if request.cookies.get(ADMINCOOKIE) == False:
        return redirect('/admin/login')
    else:
        return redirect('/admin/dashboard')

@app.route('/admin/dashboard', methods=['GET'])
def admindash():
    addviews()
    if request.args.get('key') == MASTERKEY or request.cookies.get(ADMINCOOKIE) == MASTERKEY:
        return render_template('admindash.html', views = conf.get("VIEWS"))
    else:
        return redirect('/admin/login')

@app.route('/admin/login', methods=['GET', 'POST'])
def adminlogin():
    addviews()
    if request.cookies.get(ADMINCOOKIE) == MASTERKEY:
        return redirect('/admin/dashboard')
    elif not request.form.get('password') == None:
        if request.form.get('password') == MASTERPASS:
            resp = make_response(redirect('/admin/dashboard'))
            resp.set_cookie(ADMINCOOKIE, MASTERKEY)
            return resp
        else:
            return render_template('adminlogin.html', alert="Incorrect Password", type="danger")
    else:
        return render_template('adminlogin.html')

app.run(host="0.0.0.0")