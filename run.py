#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flaskext.uploads import (UploadSet, configure_uploads, IMAGES,
                                      UploadNotAllowed)
from json import dumps

app = Flask(__name__)
api = Api(app)

uploaded_photos = UploadSet('photos', IMAGES)
configure_uploads(app, uploaded_photos)


class Upload(Resource):
    def post(self):
        msg = api.payload.get('file', '')
        photo = request.files.get('photo')
        if not (photo and title and caption):
            flash("You must fill in all the fields")
        else:
            try:
                filename = uploaded_photos.save(photo)
            except UploadNotAllowed:
                flash("The upload was not allowed")
            else:
                post = Post(title=title, caption=caption, filename=filename)
                post.id = unique_id()
                post.store()
                flash("Post successful")
return to_index()
        return jsonify({'status':'success'})

class Download(Resource):
    def post(self):
        video_url = api.payload.get('video_url', '')
        return jsonify({'status':'success'})

api.add_resource(Upload, '/upload') # Route_1
api.add_resource(Download, '/download') # Route_1


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8000, debug=True)
