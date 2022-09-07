from flask import Flask, render_template, request, jsonify
from aws.s3 import s3_obj
from aws.sqs import sqs_obj
from aws import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/upload', methods=['GET'])
def render_upload_file_page():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        s3_obj.upload_file(f.read(), f.filename)
        s3_obj.exist(f.filename)
        return f.filename


@app.route('/analyze_file_portion', methods=['POST'])
def analyze_file_portion():
    body = request.json
    start = body['start']
    end = body['end']
    file_name = body['file_name']
    read_file = s3_obj.read(file_name)
    df = csv.read(read_file, start, end)
    #TODO send it async
    sqs_obj.send_message(df)
    
    return jsonify(
        {
            "success": True
        }
    )
