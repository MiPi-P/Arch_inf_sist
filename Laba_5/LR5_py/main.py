# диаметр колема 6 см
import numpy as np
import cv2
import math
import requests
import json
import time

url = 'http://192.168.1.101:8080/commands'


def sndpost(data):
    print('Отправляю:', data)
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print('Request successful!')
        print('Response JSON:', response.json())
    else:
        print(f'Request failed with status code {response.status_code}')
        print('Response text:', response.text)


def decode_qr_code_cv2(frame):
    detector = cv2.QRCodeDetector() # находит и распознаёт qr
    retval, data, bbox, straight_qrcode = detector.detectAndDecodeMulti(frame)

    if retval:  # если хотя бы 1 qr найден
        return retval, data, bbox # возвращяем (найден ли qr1/0), (что внутри qr), (кооддинаты всех qr)
    else:
        #print('QR не найден')
        return None, None, None


def search_centers(points):
    points = points.astype(int)
    x_center = (points[0][0] + points[2][0]) // 2
    y_center = (points[0][1] + points[2][1]) // 2
    return (x_center, y_center)


def data_to_center(bbox, data):
    center = dict()
    for points, qr_data in zip(bbox, data):
        qr_data = qr_data.strip() # убираем пробелы до и после текста QR

        if qr_data == '':
            continue

        center[qr_data] = search_centers(points) # () здесь кортеж что бы не изменить случайно координаты
    return center


def drawing(frame, bbox):
    for points in bbox:
        points = points.astype(int)
        x_center, y_center = search_centers(points)
        cv2.circle(frame, (x_center, y_center), 5, (255, 0, 0), -1)

        for i in range(len(points)):
            pt1 = points[i]
            pt2 = points[(i + 1) % len(points)]
            cv2.line(frame, pt1, pt2, (255, 0, 0), 10) # синяя линия


def search_trajectory(frame, center, bbox):
    # длина qr на машине в см (измерить вручную)
    cm = 7 # 7 см
    points = bbox[0].astype(int)
    side = ((points[1][0] - points[0][0]) ** 2 + (points[1][1] - points[0][1]) ** 2) ** 0.5
    k = cm / side # длина 1 стороны квадрата '1'

    if center.get('robotA') is not None \
            and center.get('robotB') is not None \
            and center.get('coffee') is not None:

        # robotA — перед робота
        x_car1 = center.get('robotA')[0]
        y_car1 = center.get('robotA')[1]

        # robotB — зад робота
        x_car2 = center.get('robotB')[0]
        y_car2 = center.get('robotB')[1]

        # coffee — база / цель
        x_baze = center.get('coffee')[0]
        y_baze = center.get('coffee')[1]
    else:
        print('Нужны QR: robotA, robotB, coffee. Сейчас найдено:', center.keys())
        return None, None

    x_car_center = (x_car1 + x_car2) // 2
    y_car_center = (y_car1 + y_car2) // 2
    car_center = (x_car_center, y_car_center)

    dx_base = x_baze - x_car_center
    dy_base = y_baze - y_car_center
    length_line_pixel = (dx_base ** 2 + dy_base ** 2) ** 0.5
    length_line_cm = k * length_line_pixel # сколько надо проехать в см

    angle_line = math.degrees(math.atan2(dy_base, dx_base)) # угол линии и Ox (в градусах)

    # угол поворота машины
    # robotA — перед, robotB — зад, поэтому направление робота: robotB -> robotA
    dx_car = x_car1 - x_car2
    dy_car = y_car1 - y_car2

    angle_car = math.degrees(math.atan2(dy_car, dx_car)) # угол наклона машины

    turn = int(angle_line - angle_car) # угол поворота вправо в градусах

    if turn > 180:
        turn -= 360
    elif turn < -180:
        turn += 360

    cv2.circle(frame, car_center, 15, (0, 0, 255), -1)
    cv2.line(frame, car_center, (x_baze, y_baze), (0, 0, 255), 3)
    cv2.putText(frame, str(turn) + ' degrees', (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return length_line_cm, turn


# Камера =================================
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print('Не открылась камера')
    exit()

# ===== ПАРАМЕТРЫ РОБОТА =====
WHEEL_DIAMETER = 6.0  # см
WHEEL_CIRCUMFERENCE = math.pi * WHEEL_DIAMETER  # ~18.84 см

CM_PER_SEC = 30.0  # примерная скорость (подгони!)
TURN_TIME = 0.2
MIN_TURN_ANGLE = 20
MIN_DISTANCE_CM = 8

# ===== СОСТОЯНИЯ =====
STATE_FIND = 0
STATE_ROTATE = 1
STATE_FORWARD = 2

state = STATE_FIND
action_end_time = 0

while True:
    ret, frame = cam.read() # кадр с камеры

    if not ret:
        print('Не удалось получить кадр')
        break

    # frame = cv2.imread('Photo_2.png', 255)# фото

    retval, data, bbox = decode_qr_code_cv2(frame)
    now = time.time()

    if retval is not None and bbox is not None and data is not None:
        center = data_to_center(bbox, data)
        drawing(frame, bbox)

        if state == STATE_FIND:
            print('Найдены QR:', center.keys())

            length_line_cm, turn = search_trajectory(frame, center, bbox)

            if length_line_cm is not None:
                print('Длина в см:', int(length_line_cm), 'Поворот:', turn)

                if abs(turn) >= MIN_TURN_ANGLE:
                    if turn > 0:
                        send_data = {
                            'left_time': TURN_TIME,
                            'right_time': 0,
                            'forward_time': 0
                        }
                    else:
                        send_data = {
                            'left_time': 0,
                            'right_time': TURN_TIME,
                            'forward_time': 0
                        }

                    print('Поворачиваем, пока угол не станет меньше 20°:', send_data)
                    sndpost(send_data)

                    action_end_time = now + TURN_TIME
                    state = STATE_ROTATE

                else:
                    print('Угол меньше 20°, едем вперёд на нужное расстояние')

                    if length_line_cm <= MIN_DISTANCE_CM:
                        print('Робот уже рядом с базой, движение не нужно')
                        send_data = {
                            'left_time': 0,
                            'right_time': 0,
                            'forward_time': 0
                        }
                    else:
                        forward_time = length_line_cm / CM_PER_SEC

                        # ограничение, чтобы не ехал слишком долго за один раз
                        if forward_time > 1.5:
                            forward_time = 1.5

                        send_data = {
                            'left_time': 0,
                            'right_time': 0,
                            'forward_time': round(forward_time, 3)
                        }

                    print('Едем вперёд:', send_data)
                    sndpost(send_data)

                    action_end_time = now + send_data['forward_time']
                    state = STATE_FORWARD

    # ================= СОСТОЯНИЕ: ПОВОРОТ =================
    if state == STATE_ROTATE:
        if now >= action_end_time:
            print('Поворот завершён → снова сверяемся по камере')
            state = STATE_FIND

    # ================= СОСТОЯНИЕ: ДВИЖЕНИЕ =================
    elif state == STATE_FORWARD:
        if now >= action_end_time:
            print('Движение завершено → новая корректировка')
            state = STATE_FIND

    # ================= ОТРИСОВКА =================
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

# # Test ====================================================
# img = cv2.imread('Photo_test.png', 0)
#
# cv2.circle(img, (50, 50), 25, (0, 255, 0), 3) # Рисование
# cv2.imshow('img')
# cv2.waitKey(10000)
# cv2.destroyAllWindows()