import os, json
from flask import Flask, render_template, request, redirect, url_for
from lxml import etree

import gtr

app = Flask(__name__)

# static front page
@app.route('/')
def index():
    # see if we've been asked for anything
    entity = request.args.get("entity")
    id = request.args.get("id")
    
    if entity == "project":
        return redirect("/project/" + id)
    
    if entity == "person":
        return redirect("/person/" + id)
        
    if entity == "output":
        return redirect("/output/" + id)
        
    if entity == "fund":
        return redirect("/fund/" + id)
        
    if entity == "org":
        return redirect("/org/" + id)
    
    # if we didn't get a request, then just show the index page
    return render_template('index.html')

@app.route("/project/<id>")
def project(id):
    project = gtr.get_project(id)
    return render_template("project.html", project=project)

@app.route("/person/<id>")
def person(id):
    pers = gtr.get_person(id)
    return render_template("person.html", person=pers)
    
@app.route("/output/<id>")
def output(id):
    return render_template("output.html")
    
@app.route("/fund/<id>")
def fund(id):
    fund = gtr.get_fund(id)
    return render_template("fund.html", fund=fund)
    
@app.route("/org/<id>")
def org(id):
    org = gtr.get_org(id)
    return render_template("org.html", org=org)
    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
