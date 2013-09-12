import os, glob, sys
import json
import urllib2
import time
from flask import Flask, render_template, request, Response, redirect, url_for, send_file
from werkzeug import secure_filename

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['obj'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/remove_js_files', methods=['GET'])
def remove_js_files():
    str = "The dir before removal of path : %s" %os.listdir(os.getcwd());
    # # removing
    for i in range(len(glob.glob("*.js"))-1):
        try:
            os.remove(glob.glob("*.js")[i])
        except:
            pass
    str = str + " <br>" + "The dir after removal of path : %s" %os.listdir(os.getcwd())
    # listing directories after removing path
    return str

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ts = int(time.time())
            outfilename = 'workfile'+str(ts)+'.js'
            os.system('python convert_obj_three.py -i '+filename+' -o '+outfilename)
            os.remove(glob.glob(filename)[0])
            path_to_file = "./"+outfilename

            return send_file(
                path_to_file,
                mimetype="application/javascript",
                as_attachment=False,
                attachment_filename=outfilename)
        else:
            return "Sorry dude you can only upload obj files."

    else:
		return render_template('index.html')

if __name__ == "__main__":
	app.run()