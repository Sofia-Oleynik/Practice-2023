#get_ipython().system('pip install mediapipe==0.10.2 opencv-python')

"""
1. Контроль головы:
 1.1. Мочка уха и средняя точка плечевого пояса должны лежать на одной прямой - mistake_code 1.1
 1.2. Мочка уха и нос должны лежать на одной прямой - code 1.2
2. Контроль рук (точки плеча, локтя, кисти), угол в пределах 80-100 градусов - mistake_code 2
3. Контроль длины (длина спины, средняя точка плечевого пояса, тазового пояса, колена)
4. Контроль ног (крайняя точка тазового пояса, колена и лодыжки), угол в пределах 80-100 градусов - mistake_code 4

"""

import cv2
import numpy as np
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

delt_code_1_1 = 0.05
delt_code_1_2 = 0.02
delt_angle_max = 100
delt_angle_min = 80
delt_code_3_1 = 0.05
delt_code_3_2 = 0.05


def calculate_angle(a, b, c):
    a = np.array(a) # первая точка
    b = np.array(b) # вторая точка
    c = np.array(c) # третья точка
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle

    return angle 

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose: # установка порогов доверия
    while cap.isOpened():
        ret, frame = cap.read()
        
        # изменение цвета на RGB формат
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False # без записи
      
        # обнаружение
        results = pose.process(image)
    
        # обратно меняем цвет
        image.flags.writeable = True # записываем
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        try:
            landmarks = results.pose_landmarks.landmark # выводим только фактические точки (если они за пределами, не выводим)
            # ------------------координаты ориентиров
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]

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

            #------------------отрисовка средней линии позвоночника
            # отрисовка средней точки плечевого пояса
            avg_point_shoulder = ((left_shoulder[0] + right_shoulder[0]) / 2, (left_shoulder[1] + right_shoulder[1]) / 2)
            cv2.circle(image, (int(avg_point_shoulder[0] * frame.shape[1]), int(avg_point_shoulder[1] * frame.shape[0])), 5, (0, 0, 255), -1)
            # отрисовка средней точки тазового пояса
            avg_point_hip = ((left_hip[0] + right_hip[0]) / 2, (left_hip[1] + right_hip[1]) / 2)
            cv2.circle(image,
                       (int(avg_point_hip[0] * frame.shape[1]), int(avg_point_hip[1] * frame.shape[0])), 5, (0, 0, 255), -1)

            cv2.line(image, (int(avg_point_shoulder[0] * frame.shape[1]), int(avg_point_shoulder[1] * frame.shape[0])),
                     (int(avg_point_hip[0] * frame.shape[1]), int(avg_point_hip[1] * frame.shape[0])), (255, 0, 0), 2)

            # ---------------------------------------------------------------------------------1 контроль головы
            # приблизительно одна прямая уха и средней точки плечевого пояса
            """
            cv2.putText(image, str(right_ear[0]),
                        tuple(np.multiply(right_ear, [640, 480]).astype(int)),
                        # выводим рядом с нужной точкой в координатах для изображения
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA  # устанавливаем шрифт
                        )
            cv2.putText(image, str(avg_point_shoulder[0]),
                        tuple(np.multiply(avg_point_shoulder, [640, 480]).astype(int)),
                        # выводим рядом с нужной точкой в координатах для изображения
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA  # устанавливаем шрифт
                        )
            """
            if abs(avg_point_shoulder[0] - right_ear[0]) > delt_code_1_1 or abs(avg_point_shoulder[0] - left_ear[0]) > delt_code_1_1:
                print('mistake_code 1.1')

            # приблизительно одна прямая уха и носа

            """
            cv2.putText(image, str(right_ear[1]),
                        tuple(np.multiply(right_ear, [640, 480]).astype(int)),
                        # выводим рядом с нужной точкой в координатах для изображения
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA  # устанавливаем шрифт
                        )
            cv2.putText(image, str(nose[1]),
                        tuple(np.multiply(nose, [640, 480]).astype(int)),
                        # выводим рядом с нужной точкой в координатах для изображения
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA  # устанавливаем шрифт
                        )
            """

            if abs(nose[1] - right_ear[1]) > delt_code_1_2 or abs(nose[1] - left_ear[1]) > delt_code_1_2:
                print('mistake_code 1.2')

            # ---------------------------------------------------------------------------------2 контроль рук

            # считаем угол по трем точкам
            angle_l_hand = calculate_angle(left_shoulder, left_elbow, left_wrist)
            angle_r_hand = calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # выводим угол в поток изображения
            """
            cv2.putText(image, str(angle_l),
                           tuple(np.multiply(left_elbow, [640, 480]).astype(int)), # выводим рядом с нужной точкой в координатах для изображения
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA # устанавливаем шрифт
                                )
            cv2.putText(image, str(angle_r),
                        tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                        # выводим рядом с нужной точкой в координатах для изображения
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA  # устанавливаем шрифт
                        )
            """
            if angle_l_hand > delt_angle_max or angle_l_hand < delt_angle_min or angle_r_hand > delt_angle_max or angle_r_hand < delt_angle_min:
                print('mistake_code 2')

                # ---------------------------------------------------------------------------------4 контроль ног

                # считаем угол по трем точкам
                angle_l_foot = calculate_angle(left_hip, left_knee, left_ankle)
                angle_r_foot = calculate_angle(right_hip, right_knee, right_ankle)

                # выводим угол в поток изображения
                """
                cv2.putText(image, str(angle_l),
                               tuple(np.multiply(left_elbow, [640, 480]).astype(int)), # выводим рядом с нужной точкой в координатах для изображения
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA # устанавливаем шрифт
                                    )
                cv2.putText(image, str(angle_r),
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                            # выводим рядом с нужной точкой в координатах для изображения
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA  # устанавливаем шрифт
                            )
                """
                if angle_l_foot > delt_angle_max or angle_l_foot < delt_angle_min or angle_r_foot > delt_angle_max or angle_r_foot < delt_angle_min:
                    print('mistake_code 4')
                        

        except: # если у нас есть не все точки или появилась какая-то ошибка, то мы не разрываем цикл, а просто его пропускаем
            pass
        
        
        # рисуем в image результаты обнаружения (точки) и соединения, устанавливая цвет и размеры
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                 )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
