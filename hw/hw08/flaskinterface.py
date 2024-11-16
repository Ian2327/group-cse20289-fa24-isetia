import os, shutil, subprocess, pwd
from flask import Flask, request, jsonify, redirect, url_for,render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)


# Assumes that you have the toscan directory under the scandata directory under the repos directory
#uname = get_username()
#upload_folder = f'/escnfs/home/{uname}/repos/scandata/toscan' 
#app.config['upload_folder'] = upload_folder

app.config['UPLOAD_FOLDER'] = 'test'
app.config['ALLOWED_EXTENSIONS'] = {'zip', 'tar.gz', 'tgz', 'tar'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Render the upload form."""
    return render_template('upload.html')

def get_username():
    return pwd.getpwuid(os.getuid())[0]

# Checks if the file inputted is a valid type of file (.zip, .tar.gz, .tgz, .or .tar)
def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle the uploaded file."""
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    if file and allowed_file(file.filename):
        # Save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Run the external Python script with the uploaded file as input
        #script_output = run_python_script(filepath)

        # Return the output to the user
        #return jsonify({"result": script_output})
        return f"File uploaded successfully: {filepath}"

    return "Invalid file type", 400

def run_python_script(filepath):
    """Run a Python script with the given file and return its output."""
    try:
        # Example: Call `process_file.py` with the uploaded file as argument
        result = subprocess.run(
            ['python3', 'testscript.sh'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check for errors
        if result.returncode != 0:
            return f"Error: {result.stderr}"

        return result.stdout
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(hose='0.0.0.0', port=5000, debug=True)
    





