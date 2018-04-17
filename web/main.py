import os

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
GoogleMaps(app)
app.secret_key = 'LargeData2018SpringGroup10'

#google map api: AIzaSyDHswQXkT2wmHJXUeY6GvyTITMJF_iKC2k

@app.route("/")
def index():

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
