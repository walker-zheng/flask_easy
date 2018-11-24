from flask import Flask, Response, jsonify, request, send_from_directory
from flask_restplus import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug import secure_filename
import requests
import os
from subprocess import call
# import hashlib

app = Flask(__name__)
api = Api(app, version='1.0', title='My API', validate=False)

UPLOAD_FOLDER = './upload_files'
DOWNLOAD_FOLDER = './download_files'
ALLOWED_EXTENSIONS = set(['mp4', 'avi', 'wmv', 'png'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['FEATURE_EXTRATION'] = os.path.join(app.root_path, "./bin/FeatureExtraction")

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@api.route('/upload')
class Upload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        file = args['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            directory = os.path.join(app.root_path ,app.config['UPLOAD_FOLDER'])
            # file_md5 = hashlib.md5(file.read()).hexdigest()
            # directory = os.path.join(app.config['UPLOAD_FOLDER'], file_md5)
            # if not os.path.exists(directory):
            #     os.makedirs(directory)            
            if not os.path.exists(os.path.join(directory, filename)):
                file.save(os.path.join(directory, filename))
                return {'message': 'File saved', 'filename': filename}, 201
            else:
                return {'message': 'File exists', 'filename': filename}, 200
        else:
            return {'message': 'File not save', 'filename': file.filename}, 205

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print(uploads, filename)
    return send_from_directory(directory=uploads, filename=filename)

def download_file(url):
    local_filename = url.split('/')[-1]
    download_dir = os.path.join(app.root_path, app.config['DOWNLOAD_FOLDER'])
    local_filename = os.path.join(download_dir, local_filename)
    if os.path.exists(local_filename):
        os.remove(local_filename)
    wget = ["wget", "-O", local_filename, url]
    curl = ["curl", "-o", local_filename, url]
    call(wget)
    return local_filename
def extract_file(in_file, out_file):
    openface = [ app.config['FEATURE_EXTRATION'], "-q", "-f", in_file, "-outroot", os.path.join(app.root_path, 'test'), "-of", os.path.basename(out_file)]
    print(app.config['FEATURE_EXTRATION'], out_file)
    if os.path.exists(out_file):
        os.remove(out_file)
    call(openface)

@api.route('/extract')
class Extract(Resource):
    def post(self):
        msg = api.payload
        video_url = msg.get('video_url', '')
        # print(video_url)
        file = download_file(video_url)
        extract_file(file, file + '.csv')
        # print('file download done', file)
        if os.path.exists(file):
            print('file download', 'ok', video_url)
        else:
            print('file download', 'failed', video_url)
        

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=9000, debug=True)
