from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import qrcode
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'static/qrcodes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    url = request.form['url']
    filename = secure_filename(request.form['filename'])
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_filename = f'{filename}_qrcode.png'
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/qrcodes', 'qrcode.png')
    img.save(img_path)
    
    return render_template('qrcode.html', img_filename=img_filename)

@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

