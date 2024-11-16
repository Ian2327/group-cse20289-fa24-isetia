#Ian Setia
#isetia@nd.edu
import os, shutil, subprocess
from flask import Flask, request, jsonify, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
import glob
import time
import signal

app = Flask(__name__)

app.secret_key = os.urandom(24)

# Assumes that you have the toscan directory under the scandata directory under the repos directory, if not, you must enter one
UPLOAD_FOLDER = "../../../scandata/toscan" # Default toscan directory relative location
allowed_extensions = {'zip', 'tar.gz', 'tgz', 'tar'}

# Checks if the file inputted is a valid type of file (.zip, .tar.gz, .tgz, .or .tar)
def allowed_file(filename):
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

        session['scan_result'] = scan_result

        return redirect(url_for('scan_result'))

    return jsonify({"error": "File type not allowed"}), 400        
@app.route('/result')
def scan_result():
    result = session.get('scan_result', None)  # Get the result passed from the upload page
    if result is None:
        return redirect(url_for('index'))

    if "error" in result:
        return render_template('scan_result.html', error=result["error"])
    return render_template('scan_result.html', approved=result["approved"], quarantined=result["quarantined"])

# Runs the scanner.sh script and returns the result
def run_scan(file_path):
    scan_script = os.path.abspath("scanner.sh")
    path_to_approved = '../../../scandata/approved'
    path_to_quarantined = '../../../scandata/quarantined'
    path_to_log = '../../../scandata/log'
    path_to_badsites = '../hw07/badsite-10.csv'

    process = subprocess.Popen(['sh', scan_script, UPLOAD_FOLDER, path_to_approved, path_to_quarantined, path_to_log, path_to_badsites])
    time.sleep(2) # Gives scanner script time to run before going to results page
    

    if process.poll() is None:
        print("THE PROCESS IS STILL RUNNING.")
    else:
        print(f"The process has finished with exit code: {process.poll()}")


    log_file = find_latest_log(path_to_log)
    if log_file:
        approved, quarantined = parse_log(log_file)
        return {"approved": approved, "quarantined": quarantined}
    else:
        return {"error": "Log file not found or unreadable"}


def find_latest_log(log_dir):
    log_files = glob.glob(os.path.join(log_dir, '*.log'))
    if not log_files:
        return None
    return max(log_files, key=os.path.getmtime)

def parse_log(log_file):
    approved = []
    quarantined = []

    with open(log_file, 'r') as f:
        for line in f:
            if "APPROVE" in line:
                approved.append(line.strip())
            elif "QUARANTINE" in line:
                quarantined.append(line.strip())

    return approved, quarantined


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=54143, debug=True)
    

