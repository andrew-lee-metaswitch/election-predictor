from flask import Flask, request, render_template, flash, jsonify, redirect
import sys
import wtforms as wt
from wtforms import TextField, Form

from brexit_election.election_predictior import CONS_d, get_constituency_data_by_name

cons_names = [CONS_d[cons]['Name'] for cons in CONS_d.keys()]
sys.path.append('.')

class SearchForm(Form):
    autocomp= TextField('Constituency',id='autocomplete')

app = Flask(__name__)
app.secret_key = "supersecret"

@app.route("/")
def index():
    form = SearchForm(request.form)
    return render_template("index.html", form=form)

@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    search = request.args.get('term')
    app.logger.debug(search)
    return jsonify(json_list=cons_names)

@app.route("/constituency", methods=['POST'])
def redirecter():
    cons_name = request.form['autocomp']
    return redirect("http://localhost:5000/constituency/%s" % cons_name, code=302)

@app.route("/constituency/<cons_name>")
def display_constituency(cons_name):
    form = SearchForm(request.form)
    cons_data = get_constituency_data_by_name(cons_name)
    return render_template("constituency.html", data=cons_data, form=form)

if __name__ == "__main__":
    app.run(host="localhost")