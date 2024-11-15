import os, shutil, subprocess
from flask import Flask, request, jsonify, redirect, url_for, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)


# Assumes that you have the toscan directory under the scandata directory under the repos directory
UPLOAD_FOLDER = None 
allowed_extensions = {'zip', 'tar.gz', 'tgz', 'tar'}

# Checks if the file inputted is a valid type of file (.zip, .tar.gz, .tgz, .or .tar)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/')
def index():
    return render_template('flask_interface.html')

@app.route('/set_upload_folder', methods=['POST'])
def set_upload_file():
    global UPLOAD_FOLDER
    folder = request.form.get('upload_folder')

    if not folder:
        return jsonify({"error": "Upload folder not provided"}), 400

    if not os.path.isdir(folder):
        return jsonify({"error": f"'{folder}' is not a valid directory"}), 400
    
    UPLOAD_FOLDER = folder
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    print(f"Upload folder set to {UPLOAD_FOLDER}")
    return jsonify({"message": f"Upload folder set to {UPLOAD_FOLDER}"}), 200


@app.route('/upload', methods=['POST'])
def upload_file():
    global UPLOAD_FOLDER
    
    if not UPLOAD_FOLDER:
        return jsonify({"error": "Upload folder not set. Set it using /set_upload_folder"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(file_path)

        scan_result = run_scan(file_path)

        return jsonify({"result": scan_result}), 200

    return jsonify({"error": "File type not allowed"}), 400        

# Runs the scanner.sh script and returns the result
def run_scan(file_path):
    scan_script = "scanner.sh"
    path_to_approved = '../../../scandata/approved'
    path_to_quarantined = '../../../scandata/quarantined'
    path_to_log = '../../../scandata/log'
    path_to_badsites = '../hw07/badsites-10.csv'

    process = subprocess.Popen([scan_script, UPLOAD_FOLDER, path_to_approved, path_to_quarantined, path_to_log, path_to_badsites], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return f"Error: {stderr.decode('utf-8')}"

    return stdout.decode('utf-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=54143, debug=True)
    

