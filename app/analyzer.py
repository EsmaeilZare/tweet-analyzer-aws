from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/upload', methods = ['GET'])
def render_upload_file_page():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
		
