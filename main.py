from flask import Flask, render_template, request
import pickledb as dbms
import werkzeug
from random import randint

# DB Initialization
ipdb = dbms.load("ips.json", True)
# END DB Initialization

app = Flask("Hilda's Favour")
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/application')
def formx():
    ipdb.set(str(request.remote_addr), randint(000000,999999))
    return render_template('form.html')

app.run(host="0.0.0.0")