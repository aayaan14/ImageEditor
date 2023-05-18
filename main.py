from flask import Flask, render_template , request , flash
from werkzeug.utils import secure_filename
import os
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'the random string'

def processImage(filename, operation):
    print(f'the operation is {operation} and filename is {filename}')
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case 'cgray':
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(f'static/{filename}', imgProcessed)
            return filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        operation = request.form.get('operation')
        # check if the post request has the file part
        # if 'file' not in request.files:
            # flash('No file part')
            # return 'error'

        files = request.files.getlist("file")
        # file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        # if file.filename == '':
        #     flash('No selected file')
        #     return 'error'
        for file in files:
            # file.save(file.filename)
            # if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/static/{filename}'> here")
            
    return render_template('index.html')


app.run(debug=True, port=5002)