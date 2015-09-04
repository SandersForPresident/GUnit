from flask import Flask
import csv
import json
import re
import requests


app = Flask(__name__)




@app.route("/<doc_id>/")
def dump(doc_id):

    CSV_URL     = "http://docs.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=csv&gid=0" % doc_id
    csv_file    = requests.get(CSV_URL).text
    fields      = [re.sub(r'\W+', '_', field.lower()) for field in csv_file.split("\r\n")[0].split(",")]
    reader      = csv.DictReader(csv_file.split("\r\n")[1:], fields)

    return json.dumps([row for row in reader])

if __name__ == "__main__":
    app.debug = True
    app.run()