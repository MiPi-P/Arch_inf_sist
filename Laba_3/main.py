import numpy as np
import cv2
import math

def decode_qr_code_cv2(frame):
    detector = cv2.QRCodeDetector() # находит и распознаёт qr
    retval, data, bbox, straight_qrcode = detector.detectAndDecodeMulti(frame)

    if retval:  # если хотя бы 1 qr найден
        return retval, data, bbox # возвращяем (найден ли qr1/0), (что внутри qr), (кооддинаты всех qr)
    else:
        #print("QR не найден")
        return None, None, None


def search_centers(points):
    points = points.astype(int)
    x_center = (points[0][0] + points[2][0]) // 2
    y_center = (points[0][1] + points[2][1]) // 2
    return (x_center, y_center)



def data_to_center(bbox, data):
    center = dict()
    for points, qr_data in zip(bbox, data):
        center[qr_data] = search_centers(points) # () здесь кортеж что бы не изменить случайно координаты
    return center




def drawing(frame, bbox):
    for points in bbox:
        points = points.astype(int)
        x_center, y_center = search_centers(points)
        cv2.circle(frame, (x_center, y_center), 5, (255, 0, 0), -1)

        for i in range(len(points)):
            pt1 = points[i]
            pt2 = points[(i+1) % len(points)]
            cv2.line(frame, pt1, pt2, (255, 0, 0), 10) # синяя линия



def search_trajectory(frame, center, bbox):
    # длина qr на машине в см (измерить вручную)
    cm = 7 # 7 см
    points = bbox[0].astype(int)
    side = ((points[1][0] - points[0][0]) ** 2 + (points[1][1] - points[0][1]) ** 2) ** 0.5
    k = cm /(side) # длина 1 стороны квадрата "1"


    if len(center) == 3 and center.get('1') is not None \
            and center.get('2') is not None and center.get('bottom') is not None:

        x_car1 = center.get('1')[0]
        y_car1 = center.get('1')[1]
        x_car2 = center.get('2')[0]
        y_car2 = center.get('2')[1]
        x_baze = center.get('bottom')[0]
        y_baze = center.get('bottom')[1]
    else:
        return None, None

    x_car_center = (x_car1 + x_car2) // 2
    y_car_center = (y_car1 + y_car2) // 2
    car_center = (x_car_center, y_car_center)

    dx_base = x_baze - x_car_center
    dy_base = y_baze - y_car_center
    length_line_pixel = (dx_base**2 + dy_base**2)**0.5
    length_line_cm = k * length_line_pixel # сколько надо проехать в см

    angle_line = math.degrees(math.atan2(dy_base, dx_base)) # угол линии и Ox (в градусах)


    # угол поворота машины
    dx_car = x_car2 - x_car1
    dy_car = y_car2 - y_car1

    angle_car = math.degrees(math.atan2(dy_car, dx_car)) # угол наклона машины

    turn = int(angle_line - angle_car) # угол поворота вправо в градусах

    if turn > 180:
        turn -= 360
    elif turn < -180:
        turn += 360

    cv2.circle(frame, (car_center), 15, (0, 0, 255), -1)
    cv2.line(frame, car_center, (x_baze, y_baze), (0, 0, 255), 3)
    cv2.putText(frame, str(turn) + ' degrees', (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    return length_line_cm, turn






# Камера =================================
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print('Не открылась камера')
    exit()

while(True):
    ret, frame = cam.read() # кадр с камеры
    #frame = cv2.imread('Photo_4.png', 255)
    retval, data, bbox = decode_qr_code_cv2(frame)

    if retval is not None and bbox is not None and data is not None:

        center = data_to_center(bbox, data)
        drawing(frame, bbox)  # рисуем
        length_line_cm, turn = search_trajectory(frame, center, bbox)

        if length_line_cm is not None:
            print('Длина в см:', int(length_line_cm), 'Поворот:', turn)
        # data — список того что в qr
        #print('Qr:', *data)

    # else:
        # print('Qr: Не распознано')


    cv2.imshow('frame', frame)  # показываем
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