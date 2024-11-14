import os, shutil, subprocess, pwd
from flask import Flask, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)


def get_username():
    return pwd.getpwuid(os.getuid())[0]


# Assumes that you have the toscan directory under the scandata directory under the repos directory
uname = get_username()
upload_folder = f'/escnfs/home/{uname}/repos/scandata/toscan' 
allowed_extensions = {'zip', 'tar.gz', 'tgz', 'tar'}

app.config['upload_folder'] = upload_folder

# Checks if the file inputted is a valid type of file (.zip, .tar.gz, .tgz, .or .tar)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/upload', methods=['POST'])
def upload_file():
    #TODO
    pass

# Runs the scanner.sh script and returns the result
def run_scan(file_path):
    #TODO
    pass

if __name__ = '__main__':
    app.run(hose='0.0.0.0', port=5000, debug=True)
    

