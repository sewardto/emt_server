import subprocess
import requests
from os.path import abspath, isfile, join
from flask import Flask, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

RASP_HOST='http://192.168.137.250:5000/'

@app.route('/')
def hello_world():
    return 'hello, World!'

@app.route('/model', methods=['POST', 'OPTIONS'])
def upload_model():
    if request.method == 'OPTIONS':
        return ''
    model = request.files['model']
    model_name = secure_filename(model.filename)
    model.save('origin_model/' + model_name)
    if request.form.get('Tool') == 'dabnn':
        dab_model_name = model_name.replace('.onnx', '.dab')
        subprocess.run(['./onnx2bnn', 'origin_model/' + model_name, 'model/' + dab_model_name])
        files = {'file': (dab_model_name, open('model/' + dab_model_name, 'rb'), 'multipart/form-data')}
        r = requests.post(RASP_HOST + 'model', files=files)
        return r.text
    elif request.form.get('Tool') == 'ncnn':
        return 'no'
    else:
        return 'wrong'

@app.route('/image', methods=['POST', 'OPTIONS'])
def upload_image():
    if request.method == 'OPTIONS':
        return ''
    image = request.files['image']
    image_name = secure_filename(image.filename)
    image.save('image/' + image_name)
    files = {'file':(image_name, open('image/'+image_name, 'rb'), 'image/jpg')}
    r = requests.post(RASP_HOST + 'image', files=files, data=request.form)
    return r.text
    