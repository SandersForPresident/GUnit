from flask import Flask, Response
import csv
import json
import os
import re
import requests


app = Flask(__name__)

@app.route("/<doc_id>/")
def dump(doc_id):

    CSV_URL         = "http://docs.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=csv&gid=0" % doc_id
    csv_file        = requests.get(CSV_URL).text

    fields          = [re.sub(r'\W+', '_', field.lower()) for field in csv_file.split("\r\n")[0].split(",")]
    reader          = csv.DictReader(csv_file.split("\r\n")[1:], fields)
    
    response_body   = json.dumps([row for row in reader])

    response        = Response(response_body)
    response.headers['Content-type'] = 'text/json'

    return response






if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.debug = port == 5000
    app.run(host='0.0.0.0', port=port)