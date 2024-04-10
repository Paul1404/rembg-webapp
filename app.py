from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages

# Configure these variables
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                input_image = Image.open(file.stream)
            except UnidentifiedImageError:
                flash('Uploaded file is not a valid image')
                return redirect(request.url)
            output_image = remove(input_image, post_process_mask=True)
            img_io = BytesIO()
            output_image.save(img_io, 'PNG', quality=70)
            img_io.seek(0)
            return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='processed_image.png')
        else:
            flash('Invalid file type')
            return redirect(request.url)
    return render_template('index.html')


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5100
    url = f"http://{host}:{port}"
    print(f"Running on {url} (Press CTRL+C to quit)")
    app.run(host=host, port=port, debug=True)
