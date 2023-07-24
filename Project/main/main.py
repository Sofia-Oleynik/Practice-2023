import sys
import time
import pygame
import datetime as dt
import math
import csv
import numpy as np
import mediapipe as mp
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QLabel, QLineEdit, QMessageBox, QVBoxLayout, QFileDialog, QGraphicsScene, QGraphicsView
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QImage, QPixmap, QPen
from PyQt5.QtCore import QTimer
from ctypes import *
import matplotlib.pyplot as plt

WIDTH = windll.user32.GetSystemMetrics(0)
HEIGHT = windll.user32.GetSystemMetrics(1)

FLAG = False

pygame.init()

count = 0

with open("data.csv", "r") as file:
    reader = csv.reader(file)
    lines = list(reader)
    day, today, my_time, exercise_count = lines[-1]

FLAG_DATE = False
if today != str(dt.date.today()):
    day += 1
    FLAG_DATE = True
    my_time = 0
    exercise_count = 0
    today = dt.date.today()

global_cap = cv2.VideoCapture(0)

def skeleton_recognition():
    global global_cap
    global FLAG
    global count
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

    waiting_time = 100

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

    cap = global_cap


    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:  # установка порогов доверия
        while FLAG:

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


                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y]

                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y]

                # ------------------отрисовка средней линии позвоночника
                # отрисовка средней точки плечевого пояса
                avg_point_shoulder = (
                    (left_shoulder[0] + right_shoulder[0]) / 2, (left_shoulder[1] + right_shoulder[1]) / 2)
                cv2.circle(image,
                           (int(avg_point_shoulder[0] * frame.shape[1]), int(avg_point_shoulder[1] * frame.shape[0])),
                           5,
                           (0, 0, 255), -1)
                # отрисовка средней точки тазового пояса
                avg_point_hip = ((left_hip[0] + right_hip[0]) / 2, (left_hip[1] + right_hip[1]) / 2)
                cv2.circle(image,
                           (int(avg_point_hip[0] * frame.shape[1]), int(avg_point_hip[1] * frame.shape[0])), 5,
                           (0, 0, 255),
                           -1)

                cv2.line(image,
                         (int(avg_point_shoulder[0] * frame.shape[1]), int(avg_point_shoulder[1] * frame.shape[0])),
                         (int(avg_point_hip[0] * frame.shape[1]), int(avg_point_hip[1] * frame.shape[0])), (255, 0, 0),
                         2)

                # ---------------------------------------------------------------------------------3 контроль спины
                # определение длины позвоночника при сутулости

                while flag_spine != True:
                    local_flag = True
                    if local_flag:
                        print(code_0)
                        pygame.mixer.music.load("Voices/code_0.mp3")
                        pygame.mixer.music.play()
                        pygame.time.wait(4000)
                        pygame.mixer.music.stop()
                        time.sleep(5)
                        local_flag = False
                    min_spine_length = math.sqrt(
                        (avg_point_shoulder[0] - avg_point_hip[0]) ** 2 + (
                                    avg_point_shoulder[1] - avg_point_hip[1]) ** 2)
                    print(code_1)
                    pygame.mixer.music.load("Voices/code_1.mp3")
                    pygame.mixer.music.play()
                    pygame.time.wait(2000)
                    pygame.mixer.music.stop()
                    flag_spine = True

                if abs(math.sqrt((avg_point_shoulder[0] - avg_point_hip[0]) ** 2 + (
                        avg_point_shoulder[1] - avg_point_hip[1]) ** 2) - min_spine_length) < delt_code_3_1:
                    time_31 += 1
                    if time_31 > waiting_time:
                        print(code_31)
                        pygame.mixer.music.load("Voices/code_31.mp3")
                        pygame.mixer.music.play()
                        pygame.time.wait(4000)
                        pygame.mixer.music.stop()
                        time_31 = 0
                else:
                    time_31 = 0
                    count += 1

                # считаем угол между туловищем и ногами
                angle_l_spine = calculate_angle(left_shoulder, left_hip, left_knee)
                angle_r_spine = calculate_angle(right_shoulder, right_hip, right_knee)

                if angle_l_spine > delt_angle_max or angle_l_spine < delt_angle_min or angle_r_spine > delt_angle_max or angle_r_spine < delt_angle_min:
                    time_32 += 1
                    if time_32 > waiting_time:
                        print(code_32)
                        pygame.mixer.music.load("Voices/code_32.mp3")
                        pygame.mixer.music.play()
                        pygame.time.wait(5000)
                        pygame.mixer.music.stop()
                        time_32 = 0
                else:
                    time_32 = 0
                    count += 1

                # ---------------------------------------------------------------------------------1 контроль головы
                # приблизительно одна прямая уха и средней точки плечевого пояса

                if abs(avg_point_shoulder[0] - right_ear[0]) > delt_code_1_1 or abs(
                        avg_point_shoulder[0] - left_ear[0]) > delt_code_1_1:
                    time_11 += 1
                    if time_11 > waiting_time:
                        print(code_11)
                        pygame.mixer.music.load("Voices/code_11.mp3")
                        pygame.mixer.music.play()
                        pygame.time.wait(2000)
                        pygame.mixer.music.stop()
                        time_11 = 0
                else:
                    time_11 = 0
                    count += 1

                # приблизительно одна прямая уха и носа

                if abs(nose[1] - right_ear[1]) > delt_code_1_2 or abs(nose[1] - left_ear[1]) > delt_code_1_2:
                    time_12 += 1
                    if time_12 > waiting_time:
                        print(code_12)
                        pygame.mixer.music.load("Voices/code_12.mp3")
                        pygame.mixer.music.play()
                        pygame.time.wait(2000)
                        pygame.mixer.music.stop()
                        time_12 = 0
                else:
                    time_12 = 0
                    count += 1

                # ---------------------------------------------------------------------------------4 контроль ног

                # считаем угол по трем точкам
                angle_l_foot = calculate_angle(left_hip, left_knee, left_ankle)
                angle_r_foot = calculate_angle(right_hip, right_knee, right_ankle)

                # выводим угол в поток изображения

                if angle_l_foot > delt_angle_max or angle_l_foot < delt_angle_min or angle_r_foot > delt_angle_max or angle_r_foot < delt_angle_min:
                    time_4 += 1
                    if time_4 > waiting_time:
                        print(code_4)
                        pygame.mixer.music.load("Voices/code_4.mp3")
                        pygame.mixer.music.play()
                        pygame.time.wait(4000)
                        pygame.mixer.music.stop()
                        time_4 = 0
                else:
                    time_4 = 0
                    count += 1


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


class PageMain(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #264653;")
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setWindowTitle('Коррекция осанки')

        self.btn_progress = QPushButton("Посмотреть прогресс", self)
        self.btn_progress.setGeometry(WIDTH / 2 + 100, HEIGHT / 2 + 50, WIDTH - 200 - WIDTH / 2, 50)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_progress.setFont(font)
        self.btn_progress.setStyleSheet("background-color: #f4a261;\n"
                                        "border-radius: 10px;")
        self.btn_progress.setObjectName("btn_progress")
        self.btn_progress.clicked.connect(self.open_page_progress)

        self.btn_do_exer = QPushButton('Выполнить упражнения', self)
        self.btn_do_exer.setGeometry(WIDTH / 2 + 100, HEIGHT / 2 + 110, WIDTH - 200 - WIDTH / 2, 50)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_do_exer.setFont(font)
        self.btn_do_exer.setStyleSheet("background-color: #f4a261;\n"
                                       "border-radius: 10px;")
        self.btn_do_exer.setObjectName("btn_do_exer")
        self.btn_do_exer.clicked.connect(self.open_page_exercise)

        self.btn_parent = QPushButton("Родительский режим", self)
        self.btn_parent.setGeometry(WIDTH / 2 + 100, HEIGHT / 2 + 170, WIDTH - 200 - WIDTH / 2, 50)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_parent.setFont(font)
        self.btn_parent.setStyleSheet("background-color: #e9c46a;\n"
                                      "border-radius: 10px;")
        self.btn_parent.setObjectName("btn_parent")
        self.btn_parent.clicked.connect(self.open_page_input_pw)

        self.lbl_molod = QLabel('Ты сегодня сидишь правильно ' + str(my_time) + ' минут!', self)
        self.lbl_molod.setGeometry(WIDTH / 2 + 80, HEIGHT / 2 - 50, WIDTH - 180 - WIDTH / 2, 30)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_molod.setFont(font)
        self.lbl_molod.setStyleSheet("color: #ffffff")
        self.lbl_molod.setObjectName("lbl_molod")

        self.btn_start = QPushButton('CТАРТ', self)
        self.btn_start.setStyleSheet("background-color: #2a9d8f;"
                                     "color: rgb(255, 255, 255);"
                                     "border-radius: 10px;")
        self.btn_start.setGeometry(WIDTH / 2 + 100, HEIGHT / 2 - 250, 200, 70)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.btn_start.setFont(font)
        self.btn_start.setObjectName("btn_start")
        self.btn_start.clicked.connect(self.push_on)

        self.btn_stop = QPushButton('СТОП', self)
        self.btn_stop.setStyleSheet("background-color: #e76f51;"
                                    "color: #ffffff;"
                                    "border-radius: 10px;")
        self.btn_stop.setGeometry(WIDTH - 100 - 200, HEIGHT / 2 - 250, 200, 70)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setBold(True)
        font.setPointSize(18)
        font.setWeight(75)
        self.btn_stop.setFont(font)
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.clicked.connect(self.push_off)


        self.lbl_transl = QLabel("Трансляция", self)
        # self.lbl_transl.resize(640, 480)
        self.lbl_transl.move(60, 60)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_transl.setFont(font)
        self.lbl_transl.setStyleSheet("color: #ffffff;")
        self.lbl_transl.setObjectName("lbl_transl")

        self.lbl_video = QLabel("Видео-поток", self)
        self.lbl_video.setFixedSize(WIDTH / 2 - 20, HEIGHT - 50)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_video)
        self.setLayout(layout)

        self.camera = global_cap
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_video_stream)
        self.timer.start(30)

    def update_video_stream(self):
        # Чтение кадра видео

        ret, frame = self.camera.read()
        if ret:
            # Преобразование кадра в формат QImage
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(
                frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QtGui.QImage.Format_RGB888
            )
            # Отображение кадра на виджете QLabel
            self.lbl_video.setPixmap(QtGui.QPixmap.fromImage(image))

        else:
            self.timer.stop()

    def push_on(self):
        global FLAG
        FLAG = True
        skeleton_recognition()


    def push_off(self):
        global FLAG_DATE
        global count
        global my_time
        global day
        global today
        global exercise_count
        my_time = int(my_time)
        my_time += int(count / 2400)
        count = 0

        if FLAG_DATE:
            with open("data.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([day, today, my_time, exercise_count])
        else:
            with open("data.csv", "r") as file:
                reader = csv.reader(file)
                lines = list(reader)
            lines[-1] = [day, today, my_time, exercise_count]

            with open("data.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(lines)

        global FLAG
        FLAG = False
        print(FLAG)




    def open_page_exercise(self):
        self.page_exercise = PageExercise()
        self.page_exercise.show()
        self.hide()

    def open_page_progress(self):
        self.page_progress = PageProgress()
        self.page_progress.show()
        self.hide()

    def open_page_input_pw(self):
        self.page_input_pw = PageInputPassword()
        self.page_input_pw.show()
        self.hide()


class PageExercise(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.setStyleSheet("background-color: #264653;")
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setWindowTitle('Упражнения')

        self.btn_back = QPushButton("Назад", self)
        self.btn_back.setGeometry(WIDTH - 120 - 40, HEIGHT - 100 - 50, 120, 50)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setWeight(75)
        self.btn_back.setFont(font)
        self.btn_back.setStyleSheet("background-color: #e76f51;\n"
                                    "border-radius: 10px;")
        self.btn_back.clicked.connect(self.open_main_page)

        # Создание кнопок "Старт" и "Стоп"
        self.btn_start = QPushButton('CТАРТ', self)
        self.btn_start.setStyleSheet("background-color: #2a9d8f;"
                                     "color: rgb(255, 255, 255);"
                                     "border-radius: 10px;")
        self.btn_start.resize(100, 30)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.btn_start.setFont(font)
        self.btn_start.setObjectName("btn_start")
        self.btn_start.clicked.connect(self.start_recording)

        self.btn_stop = QPushButton('СТОП', self)
        self.btn_stop.setStyleSheet("background-color: #e76f51;"
                                    "color: #ffffff;"
                                    "border-radius: 10px;")
        self.btn_stop.resize(100, 30)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setBold(True)
        font.setPointSize(18)
        font.setWeight(75)
        self.btn_stop.setFont(font)
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.clicked.connect(self.stop_recording)

        # создание виджета для вывода видео-потока
        self.videoWidget = QLabel(self)
        self.videoWidget.resize(640, 480)

        # self.videoWidget.setMinimumSize(WIDTH - 20, HEIGHT - 20)

        # создание главного вертикального лэйаута
        self.vbox = QVBoxLayout()
        # self.vbox.setFixedSize(800, 600)
        self.vbox.addWidget(self.btn_start)
        self.vbox.addWidget(self.btn_stop)
        self.vbox.addWidget(self.btn_back)
        self.vbox.addWidget(self.videoWidget)

        # установка лэйаута в окно
        self.setLayout(self.vbox)

    def start_recording(self):
        # создание объекта захвата видео с камеры
        self.cap = global_cap

        # создание объекта записи видео в формате AVI
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter((str(dt.datetime.now().date()) + str(dt.datetime.now().time()))[:12] + ".avi",
                                   fourcc, 20.0, (640, 480))

        # запуск цикла чтения и записи кадров с камеры
        while (self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                # вывод кадра на виджет
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                self.videoWidget.setPixmap(QPixmap.fromImage(img))

                # запись кадра в файл
                self.out.write(frame)

                # обновление виджета
                QApplication.processEvents()
            else:
                break

    def stop_recording(self):
        # остановка записи видео в файл
        self.out.release()


    def open_main_page(self):
        self.page_main = PageMain()
        self.page_main.show()
        self.hide()


class PageProgress(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #264653;")
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setWindowTitle('Прогресс')

        self.btn_back = QPushButton("Назад", self)
        self.btn_back.setGeometry(WIDTH - 120 - 40, HEIGHT - 100 - 50, 120, 50)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setWeight(75)
        self.btn_back.setFont(font)
        self.btn_back.setStyleSheet("background-color: #e76f51;\n"
                                    "border-radius: 10px;")
        self.btn_back.clicked.connect(self.open_main_page)

    def open_main_page(self):
        self.page_main = PageMain()
        self.page_main.show()
        self.hide()



class PageInputPassword(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #264653;")
        self.setGeometry(WIDTH / 2 - 200, 200, 400, 200)
        self.setWindowTitle("Ввод пароля")

        self.lbl_password = QLabel('Введите пароль: ', self)
        self.lbl_password.setGeometry(50, 70, 1300, 30)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(8)
        font.setWeight(75)
        self.lbl_password.setFont(font)
        self.lbl_password.setStyleSheet("color: #ffffff;")

        self.lned_input_pw = QLineEdit(self)
        self.lned_input_pw.setEchoMode(QLineEdit.Password)
        self.lned_input_pw.setGeometry(210, 70, 110, 20)
        self.lned_input_pw.setStyleSheet("color: #ffffff;")

        self.btn_submit = QPushButton('Отправить', self)
        self.btn_submit.setGeometry(150, 130, 110, 30)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(8)
        font.setWeight(75)
        self.btn_submit.setFont(font)
        self.btn_submit.setStyleSheet("background-color: #e9c46a;\n"
                                      "border-radius: 10px;")
        self.btn_submit.clicked.connect(self.check_password)

        self.btn_back = QPushButton("Назад", self)
        self.btn_back.setGeometry(320, 160, 70, 30)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(8)
        font.setWeight(75)
        self.btn_back.setFont(font)
        self.btn_back.setStyleSheet("background-color: #e76f51;\n"
                                    "border-radius: 10px;")
        self.btn_back.clicked.connect(self.open_main_page)

    def open_main_page(self):
        self.page_main = PageMain()
        self.page_main.show()
        self.hide()

    def check_password(self):
        password = self.lned_input_pw.text()

        if password == '1234':
            self.open_page_parent()
        else:
            error = QMessageBox()
            # error.se
            error.setWindowTitle("Ошибка доступа")
            error.setText('Введен неверный пароль')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.buttonClicked.connect(self.popup_action)
            error.exec_()
            # QMessageBox.warning(self, "Ошибка доступа", 'Введен не верный пароль')

    def popup_action(self, btn):
        # self.lbl_password.setText('')
        self.lned_input_pw.setText('')
        # print("print ok")

    def open_page_parent(self):
        self.page_parent = PageParent()
        self.page_parent.show()
        self.hide()


class PageParent(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #264653;")
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setWindowTitle('Родительский режим')

        self.btn_back = QPushButton("Назад", self)
        self.btn_back.setGeometry(WIDTH - 120 - 40, HEIGHT - 100 - 50, 120, 50)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setWeight(75)
        self.btn_back.setFont(font)
        self.btn_back.setStyleSheet("background-color: #f4a261;\n"
                                    "border-radius: 10px;")
        self.btn_back.clicked.connect(self.open_main_page)

        # Создание кнопки "Посмотреть"
        self.btn_play = QPushButton('Посмотреть', self)
        self.btn_play.setGeometry(WIDTH / 2 + 100, HEIGHT / 2 - 250, WIDTH - 200 - WIDTH / 2, 70)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setWeight(75)
        self.btn_play.setFont(font)
        self.btn_play.setStyleSheet("background-color: #e9c46a;\n"
                                    "border-radius: 10px;")
        self.btn_play.clicked.connect(self.play_video)
        # Создание кнопки "Принять"
        self.btn_accept = QPushButton('Принять', self)
        self.btn_accept.setGeometry(WIDTH / 2 + 100, HEIGHT / 2 - 150, 200, 70)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setWeight(75)
        self.btn_accept.setFont(font)
        self.btn_accept.setStyleSheet("background-color: #2a9d8f;\n"
                                      "border-radius: 10px;")
        self.btn_accept.clicked.connect(self.count_exercise)

        # Создание кнопки "Отклонить"
        self.btn_reject = QPushButton('Отклонить', self)
        self.btn_reject.setGeometry(WIDTH - 100 - 200, HEIGHT / 2 - 150, 200, 70)
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setWeight(75)
        self.btn_reject.setFont(font)
        self.btn_reject.setStyleSheet("background-color: #e76f51;\n"
                                      "border-radius: 10px;")
        # !!!!!self.btn_reject.clicked.connect(self.play_video)

        # Создание метки для отображения видео-потока
        self.lbl_video = QLabel("Видео-поток", self)
        self.lbl_video.setFixedSize(WIDTH / 2 - 20, HEIGHT - 50)
        self.lbl_video.resize(640, 480)
        self.lbl_video.move(50, 50)

        # Инициализация переменных
        self.cap = None

    def count_exercise(self):
        global FLAG_DATE
        global my_time
        global day
        global today
        global exercise_count
        exercise_count = int(exercise_count)
        exercise_count += 1

        if FLAG_DATE:
            with open("data.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([day, today, my_time, exercise_count])
        else:
            with open("data.csv", "r") as file:
                reader = csv.reader(file)
                lines = list(reader)
            lines[-1] = [day, today, my_time, exercise_count]

            with open("data.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(lines)




    def play_video(self):
        # Выбор файла видео
        filename, _ = QFileDialog.getOpenFileName(self, 'Выберите файл', '', 'Видео (*.avi)')
        if filename:
            # Открытие файла видео
            self.cap = cv2.VideoCapture(filename)
            # Чтение и отображение кадров видео-потока в метке
            while True:
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = frame.shape
                    bytes_per_line = ch * w
                    q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_image)
                    self.lbl_video.setPixmap(pixmap)
                    QApplication.processEvents()  # Обновление интерфейса
                else:
                    break
            self.cap.release()

    def open_main_page(self):
        self.page_main = PageMain()
        self.page_main.show()
        self.hide()


if __name__ == "__main__":
    global_cap = cv2.VideoCapture(0)
    app = QApplication(sys.argv)
    main_page = PageMain()
    main_page.show()
    sys.exit(app.exec_(), global_cap.release(), pygame.quit())


