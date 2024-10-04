from ugot import ugot
import time
import cv2
import numpy as np

got = ugot.UGOT()
got.initialize('192.168.1.214')
got.open_camera()
got.load_models(["apriltag_qrcode"])
got.set_track_recognition_line(0)  # 0: mono line, 1: double line


def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

qr_codes = []
def qr_scan(index):
    start_time = time.time()
    delay = 5
    angles = range(-50, 51, 5)  
    detector = cv2.QRCodeDetector()  
    
    while True:
        if time.time() - start_time >= delay:
            return None
        frame = got.read_camera_data()  
        if frame is not None:
            nparr = np.frombuffer(frame, np.uint8)
            data = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if data is not None:
                cv2.imshow("frame", data) 
                rgb_image = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)

                for angle in angles:
                    rotated_image = rotate_image(rgb_image, angle)  
                    data_qr, bbox, rectified_image_qr = detector.detectAndDecode(rotated_image)
                    
                    if data_qr: 
                        # Làm sạch chuỗi data_qr
                        data_qr = data_qr.strip()
                        qr_codes.append(data_qr)

                        print(f"Tin hieu tram so {index}: {data_qr}")
                        got.screen_print_text_newline(f"Tin hieu tram so {index}: {data_qr}", 1)
                        return data_qr

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  
    cv2.destroyAllWindows()

def action_qr_code():
    if qr_codes:  
        first_qr_code = qr_codes.pop(0)

        # Process each character in the QR code string
        for char in first_qr_code:
            if char == 'f':
                got.mecanum_move_speed_times(0,30,2,0)
            elif char == 'b':
                got.mecanum_move_speed_times(1,30,2,0)
            elif char == 'l':
                got.mecanum_turn_speed_times(2,60,2,0)
            elif char == 'r':
                got.mecanum_turn_speed_times(3,60,2,0)
            else:
                got.screen_print_text_newline(f"Chưa biết ký tự: {char}",0)
                print(f"Chưa biết ký tự: {char}")

    else:
        got.screen_print_text_newline("Chưa có mã QR nào được quét.",0)
        print("Chưa có mã QR nào được quét.")


while True:
    qr_code = qr_scan(1)  
    
    action_qr_code()
    print(f"Processed QR code: {qr_code}")

    time.sleep(1)
    
    frame = got.read_camera_data()
    if frame is not None:
        nparr = np.frombuffer(frame, np.uint8)
        data = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow("frame", data)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    time.sleep(0.1)