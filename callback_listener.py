from flask import Flask, Response, jsonify, request, send_from_directory
from flask_restplus import Api, Resource, reqparse
import requests
import os
from subprocess import call
# import hashlib

app = Flask(__name__)
api = Api(app, version='1.0', title='My API', validate=False)

@api.route('/rest/detect_callback')
class Callback(Resource):
    def post(self):
        msg = self.api.payload
        print(msg)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=44001, debug=True)
