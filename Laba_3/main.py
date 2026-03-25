import numpy as np
import cv2

def decode_qr_code_cv2(frame):
    detector = cv2.QRCodeDetector() # находит и распознаёт qr
    retval, data, bbox, straight_qrcode = detector.detectAndDecodeMulti(frame)

    if retval:  # если хотя бы 1 qr найден
        # рисуем квадрат на qr
        if bbox is not None:
            for points in bbox:
                points = points.astype(int)

                x_center = int((points[0][0] + points[2][0]) / 2)
                y_center = int((points[0][1] + points[2][1]) / 2)
                centre = [x_center, y_center]
                cv2.circle(frame, (x_center, y_center), 5, (255, 0, 0), -1)

                for i in range(len(points)):
                    pt1 = tuple(points[i])
                    pt2 = tuple(points[(i+1) % len(points)])
                    cv2.line(frame, pt1, pt2, (255, 0, 0), 10) # синяя линия


            # показываем
            # cv2.imshow("QR Code Detection", frame)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        return data # возвращяем то что в qr
    else:
        #print("QR Code not detected or could not be decoded.")
        return None


# Камера =================================
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print('Не открылась камера')
    exit()

while(True):
    ret, frame = cam.read() # кадр с камеры

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # преобразуем в серый

    data = decode_qr_code_cv2(frame)

    cv2.imshow('frame',frame)

    if data is not None:
        # data — список строк, выводим каждую
        for d in data:
            print(d)
    else:
        print(None)

    if cv2.waitKey(1) & 0xFF == ord('q'): # по q выход
        break

cam.release()
cv2.destroyAllWindows()

# # Test ====================================================
# img = cv2.imread('Photo_test.png', 0)
#
# cv2.circle(img, (50, 50), 25, (0, 255, 0), 3) # Рисование
# cv2.imshow('img', img)
# cv2.waitKey(10000)
# cv2.destroyAllWindows()