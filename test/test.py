import requests
import json
import os

class UT():
    def __init__(self, url):
        self.url = url
        # self.file = 'haha.png'
        self.file = 'default.wmv'
    def test_download(self):
        if os.path.exists(self.file):
            print('file found:', self.file)
            os.remove(self.file)
            print('file rm:', self.file)
        from subprocess import call
        wget = ["wget", "-O", self.file, self.url + '/download/' + self.file]
        curl = ["curl", "-o", self.file, self.url + '/download/' + self.file]
        call(curl)
        if os.path.exists(self.file):
            print('file download', self.file)
        else:
            print('file download', 'failed')
    def test_upload(self):
        if os.path.exists(self.file):
            print('file found:', self.file)
            files = {'file': open(self.file,'rb')}
            data = dict()
            res = requests.post(self.url + '/upload', files=files, data=data)
            if res and res.status_code == 200:
                print('upload ok', res.status_code)
            else:
                print('upload failed', res.status_code)
        else:
            print('file not found:', self.file)
    def test_extract(self):
        data = dict()
        data['video_url'] = 'http://localhost:8000' + '/download/' + self.file
        print(data)
        headers = {'Content-Type': 'application/json'}
        res = requests.post(self.url + '/extract', data=json.dumps(data), headers=headers)
        if res and res.status_code == 200:
            print('extract ok', res.status_code)
        else:
            print('extract failed', res.status_code)

if __name__ == "__main__":
    t = UT('http://localhost:8000')
    t.test_upload()
    t.test_download()
    t_2 = UT('http://localhost:9000')
    t_2.test_extract()

