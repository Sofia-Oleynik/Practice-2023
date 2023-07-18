import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets


class PageMain(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(150, 150, 750, 550)
        self.setWindowTitle('Main page')

        self.btn_start = QPushButton('START', self)
        self.btn_start.setGeometry(QtCore.QRect(370, 120, 150, 50))
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.btn_start.setFont(font)
        self.btn_start.setStyleSheet("background-color: rgb(35, 108, 56);\n"
"color: rgb(255, 255, 255);")
        self.btn_start.setObjectName("btn_start")

        self.btn_stop = QPushButton('STOP', self)
        self.btn_stop.setGeometry(QtCore.QRect(530, 120, 150, 50))
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.btn_stop.setFont(font)
        self.btn_stop.setStyleSheet("background-color: rgb(235, 11, 119);\n"
"color: rgb(255, 255, 255);")
        self.btn_stop.setObjectName("btn_stop")

        self.btn_progress = QPushButton("Посмотреть прогресс", self)
        self.btn_progress.setGeometry(QtCore.QRect(370, 310, 300, 40))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_progress.setFont(font)
        self.btn_progress.setStyleSheet("")
        self.btn_progress.setObjectName("btn_progress")
        self.btn_progress.clicked.connect(self.open_page_progress)

        self.btn_do_exer = QPushButton('Выполнить упражнения', self)
        self.btn_do_exer.setGeometry(QtCore.QRect(370, 350, 300, 40))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_do_exer.setFont(font)
        self.btn_do_exer.setStyleSheet("")
        self.btn_do_exer.setObjectName("btn_do_exer")
        self.btn_do_exer.clicked.connect(self.open_page_exercise)

        self.btn_parent = QPushButton("Родительский режим", self)
        self.btn_parent.setGeometry(QtCore.QRect(370, 390, 300, 40))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_parent.setFont(font)
        self.btn_parent.setStyleSheet("")
        self.btn_parent.setObjectName("btn_parent")
        self.btn_parent.clicked.connect(self.open_page_input_pw)

        self.lbl_molod = QLabel('Молодец! Ты сидишь ровно!', self)
        self.lbl_molod.setGeometry(QtCore.QRect(390, 230, 261, 31))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_molod.setFont(font)
        self.lbl_molod.setObjectName("lbl_molod")

        self.lbl_transl = QLabel("Трансляция", self)
        self.lbl_transl.setGeometry(QtCore.QRect(110, 30, 131, 31))
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_transl.setFont(font)
        self.lbl_transl.setObjectName("lbl_transl")

        self.lbl_image = QLabel('Картинка/видео', self)
        self.lbl_image.setGeometry(QtCore.QRect(40, 90, 300, 400))
        self.lbl_image.setText("")
        self.lbl_image.setPixmap(QtGui.QPixmap("мышка в малине.jpg"))
        self.lbl_image.setObjectName("lbl_image")

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
        self.setGeometry(150, 150, 750, 550)
        self.setWindowTitle('Упражнения')

        self.btn_back = QPushButton("Назад", self)
        self.btn_back.setGeometry(10, 10, 50, 20)
        self.btn_back.clicked.connect(self.open_main_page)

    def open_main_page(self):
        self.page_main = PageMain()
        self.page_main.show()
        self.hide()

class PageProgress(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(150, 150, 750, 550)
        self.setWindowTitle('Прогресс')

        self.btn_back = QPushButton("Назад", self)
        self.btn_back.setGeometry(10, 10, 50, 20)
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
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Ввод пароля")

        self.lbl_password = QLabel('Password: ', self)
        self.lbl_password.setGeometry(50, 50, 100, 30)

        self.lned_input_pw = QLineEdit(self)
        self.lned_input_pw.setEchoMode(QLineEdit.Password)
        self.lned_input_pw.setGeometry(160, 50, 100, 30)

        self.btn_submit = QPushButton('Отправить', self)
        self.btn_submit.setGeometry(100, 100, 100, 30)
        self.btn_submit.clicked.connect(self.check_password)

        self.btn_back = QPushButton("Назад", self)
        self.btn_back.setGeometry(10, 10, 50, 20)
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
            error.setWindowTitle("Ошибка доступа")
            error.setText('Введен неверный пароль')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.buttonClicked.connect(self.popup_action)  #!!! че за дичь
            error.exec_()
            #QMessageBox.warning(self, "Ошибка доступа", 'Введен не верный пароль')

    def popup_action(self, btn):
        #self.lbl_password.setText('')
        self.lned_input_pw.setText('')
        #print("print ok")

    def open_page_parent(self):
        self.page_parent = PageParent()
        self.page_parent.show()
        self.hide()

class PageParent(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(150, 150, 750, 550)
        self.setWindowTitle('Родительский режим')

        self.btn_back = QPushButton("Назад", self)
        self.btn_back.setGeometry(10, 10, 50, 20)
        self.btn_back.clicked.connect(self.open_main_page)

    def open_main_page(self):
        self.page_main = PageMain()
        self.page_main.show()
        self.hide()

class NewPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_page = PageMain()
    main_page.show()
    sys.exit(app.exec_())
