from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime

app = Flask(__name__)
app.secret_key = 'jangyehjins'

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_info(file_path):
    return {
        'name': os.path.basename(file_path),
        'created': datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M'),
        'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M'),
        'size': os.path.getsize(file_path)
    }

@app.route('/')
def index():
    files = [get_file_info(os.path.join(app.config['UPLOAD_FOLDER'], f)) for f in os.listdir(app.config['UPLOAD_FOLDER'])]
    return render_template('index.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Only allowed {txt, pdf, png, jpg, jpeg, gif}','error') 
            return redirect(request.url)
    return render_template('upload.html')


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'{filename} deleted successfully')
    else:
        flash('File not found!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
