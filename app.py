import qrcode
from PIL import Image
from flask import Flask, render_template, request, send_from_directory, Response
import os
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'static/qrcodes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data_type = request.form['data_type']
    data = request.form['data']
    filename = request.form['filename']

    if data_type == 'url':
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_filename = f'{filename}_qrcode.png'  # Nombre de archivo basado en el nombre proporcionado por el usuario
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        img.save(img_path)
    else:
        # Para datos de texto
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_filename = f'{filename}_text_qrcode.png'  # Nombre de archivo basado en el nombre proporcionado por el usuario
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        img.save(img_path)

    # Devuelve la imagen como una respuesta HTTP
    with open(img_path, 'rb') as img_file:
        img_data = img_file.read()
    return Response(img_data, content_type='image/png')

@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        import sys
        sys.exit()
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror(title="Generador qr con flask", message=f"{e}")
