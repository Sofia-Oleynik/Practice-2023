# get_ipython().system('pip install mediapipe==0.10.2 opencv-python')


import time
import math
import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


delt_code_1_1 = 0.05
delt_code_1_2 = 0.02
delt_angle_max = 100
delt_angle_min = 80
delt_code_3_1 = 0.03

flag_spine = False

time_11 = 0
time_12 = 0
time_31 = 0
time_32 = 0
time_4 = 0

waiting_time = 600

min_spine_length = 0.0

code_11 = '11'
code_12 = '12'
code_31 = '31'
code_32 = '32'
code_4 = '4'
code_0 = '0'
code_1 = '1'


def calculate_angle(a, b, c):
    a = np.array(a)  # первая точка
    b = np.array(b)  # вторая точка
    c = np.array(c)  # третья точка

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:  # установка порогов доверия
    while cap.isOpened():
        ret, frame = cap.read()

        # изменение цвета на RGB формат
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False  # без записи

        # обнаружение
        results = pose.process(image)

        # обратно меняем цвет
        image.flags.writeable = True  # записываем
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark  # выводим только фактические точки (если они за пределами, не выводим)
            # ------------------координаты ориентиров
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]

            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y]

            left_ear = [landmarks[mp_pose.PoseLandmark.LEFT_EAR].x, landmarks[mp_pose.PoseLandmark.LEFT_EAR].y]
            right_ear = [landmarks[mp_pose.PoseLandmark.RIGHT_EAR].x, landmarks[mp_pose.PoseLandmark.RIGHT_EAR].y]
            nose = [landmarks[mp_pose.PoseLandmark.NOSE].x, landmarks[mp_pose.PoseLandmark.NOSE].y]

            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y]

            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y]

            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y]

            # ------------------отрисовка средней линии позвоночника
            # отрисовка средней точки плечевого пояса
            avg_point_shoulder = (
            (left_shoulder[0] + right_shoulder[0]) / 2, (left_shoulder[1] + right_shoulder[1]) / 2)
            cv2.circle(image,
                       (int(avg_point_shoulder[0] * frame.shape[1]), int(avg_point_shoulder[1] * frame.shape[0])), 5,
                       (0, 0, 255), -1)
            # отрисовка средней точки тазового пояса
            avg_point_hip = ((left_hip[0] + right_hip[0]) / 2, (left_hip[1] + right_hip[1]) / 2)
            cv2.circle(image,
                       (int(avg_point_hip[0] * frame.shape[1]), int(avg_point_hip[1] * frame.shape[0])), 5, (0, 0, 255),
                       -1)

            cv2.line(image, (int(avg_point_shoulder[0] * frame.shape[1]), int(avg_point_shoulder[1] * frame.shape[0])),
                     (int(avg_point_hip[0] * frame.shape[1]), int(avg_point_hip[1] * frame.shape[0])), (255, 0, 0), 2)

            # ---------------------------------------------------------------------------------3 контроль спины
            # определение длины позвоночника при сутулости

            while flag_spine != True:
                local_flag = True
                if local_flag:
                    print(code_0)
                    time.sleep(7)
                    local_flag = False
                min_spine_length = math.sqrt(
                    (avg_point_shoulder[0] - avg_point_hip[0]) ** 2 + (avg_point_shoulder[1] - avg_point_hip[1]) ** 2)
                print(code_1)
                flag_spine = True
            
            if abs(math.sqrt((avg_point_shoulder[0] - avg_point_hip[0]) ** 2 + (
                    avg_point_shoulder[1] - avg_point_hip[1]) ** 2) - min_spine_length) < delt_code_3_1:
                time_31 += 1
                if time_31 > waiting_time:
                    print(code_31)
                    time_31 = 0
            else:
                time_31 = 0
            # считаем угол между туловищем и ногами
            angle_l_spine = calculate_angle(left_shoulder, left_hip, left_knee)
            angle_r_spine = calculate_angle(right_shoulder, right_hip, right_knee)

            if angle_l_spine > delt_angle_max or angle_l_spine < delt_angle_min or angle_r_spine > delt_angle_max or angle_r_spine < delt_angle_min:
                time_32 += 1
                if time_32 > waiting_time:
                    print(code_32)
                    time_32 = 0
            else:
                time_32 = 0

            # ---------------------------------------------------------------------------------1 контроль головы
            # приблизительно одна прямая уха и средней точки плечевого пояса

            if abs(avg_point_shoulder[0] - right_ear[0]) > delt_code_1_1 or abs(
                    avg_point_shoulder[0] - left_ear[0]) > delt_code_1_1:
                time_11 += 1
                if time_11 > waiting_time:
                    print(code_11)
                    time_11 = 0
            else:
                time_11 = 0

            # приблизительно одна прямая уха и носа


            if abs(nose[1] - right_ear[1]) > delt_code_1_2 or abs(nose[1] - left_ear[1]) > delt_code_1_2:
                time_12 += 1
                if time_12 > waiting_time:
                    print(code_12)
                    time_12 = 0
            else:
                time_12 = 0


            # ---------------------------------------------------------------------------------4 контроль ног

            # считаем угол по трем точкам
            angle_l_foot = calculate_angle(left_hip, left_knee, left_ankle)
            angle_r_foot = calculate_angle(right_hip, right_knee, right_ankle)

            # выводим угол в поток изображения
            
            if angle_l_foot > delt_angle_max or angle_l_foot < delt_angle_min or angle_r_foot > delt_angle_max or angle_r_foot < delt_angle_min:
                time_4 += 1
                if time_4 > waiting_time:
                    print(code_4)
                    time_4 = 0
            else:
                time_4 = 0


        except:  # если у нас есть не все точки или появилась какая-то ошибка, то мы не разрываем цикл, а просто его пропускаем
            pass

        # рисуем в image результаты обнаружения (точки) и соединения, устанавливая цвет и размеры
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
