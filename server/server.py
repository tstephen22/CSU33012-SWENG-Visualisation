from flask import Flask 
import json
app = Flask(__name__)

@app.route("/members")
def members():
    f = open("Visualisation_data.json")
    data = json.load(f)
    return data

if __name__ == "__main__":
    app.run(debug=True)