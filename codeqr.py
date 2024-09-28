import qrcode
from PIL import Image


text = input("Hãy nhập vào: ")

def text_to_qr(text, file_name=None):

    if file_name is None:
        file_name = f"{text}.png".replace('/', '_').replace('\\', '_')
    qr = qrcode.QRCode(
        version=1,  
        error_correction=qrcode.constants.ERROR_CORRECT_L,  
        box_size=10,  # kích thước mỗi ô của mã QR
        border=2,  
    )

    qr.add_data(text)
    qr.make(fit=True)
    
    # Tạo ảnh mã QR
    img = qr.make_image(fill='black', back_color='white')
    
    # Chuyển ảnh mã QR về kích thước 400x400
    img = img.resize((400, 400), Image.Resampling.LANCZOS)
    
    # Lưu mã QR thành file ảnh
    img.save(file_name)
    print(f"Mã QR đã được lưu thành công với tên {file_name}")

text_to_qr(text)
