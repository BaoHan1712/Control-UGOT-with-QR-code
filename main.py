from flask import Flask, render_template, request, send_file, url_for
import qrcode
from PIL import Image
import io
import os

app = Flask(__name__)

def text_to_qr(text):
    # Tạo tên file từ văn bản và thay thế các ký tự không hợp lệ
    file_name = f"{text}.png".replace('/', '_').replace('\\', '_')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Tạo ảnh mã QR
    img = qr.make_image(fill='black', back_color='white')

    # Chuyển ảnh mã QR về kích thước 400x400
    img = img.resize((400, 400), Image.LANCZOS)

    # Lưu ảnh vào bộ nhớ tạm thời
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    return byte_io, file_name

# Route chính để hiển thị form và tạo mã QR
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        qr_image, file_name = text_to_qr(text)

        # Trả file ảnh QR code về cho người dùng với tên file dựa trên văn bản
        return send_file(qr_image, mimetype='image/png', as_attachment=True, download_name=file_name)

    # Lấy danh sách ảnh mẫu từ thư mục uploads
    upload_folder = os.path.join(app.static_folder, 'uploads')
    sample_images = [{'path': url_for('static', filename='uploads/' + image), 'name': os.path.splitext(image)[0]} for image in os.listdir(upload_folder)]

    return render_template('index.html', sample_images=sample_images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
