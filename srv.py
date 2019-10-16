#!/usr/bin/python3

from flask import Flask
from flask import request, jsonify, send_file
import os
from flask_cors import CORS
import subprocess
from gfonts import download

app = Flask(__name__)
CORS(app)


@app.route('/')
def idx():
    return send_file('index.html')


@app.route('/zip', methods=['POST'])
def ziproute():
    l = request.form['link']
    zipfile, fonts = download(l, False)
    return send_file(zipfile, mimetype='application/zip', as_attachment=True, attachment_filename='gfonts.zip')


port = int(os.getenv('PORT', '8000'))
app.run(host='0.0.0.0', port=port)
