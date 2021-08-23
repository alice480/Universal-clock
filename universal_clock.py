import sys
import datetime as dt
import sqlite3
import csv

from PyQt5 import QtCore, QtMultimedia, uic
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QStyleFactory, QFileDialog


class DateError(Exception):
    pass


class Clock(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('clock.ui', self)
        self.create_spisok()
        self.comboBox.addItems(self.zones)
        self.comboBox_2.addItems(self.zones)
        self.comboBox_4.addItems(self.zones)
        self.lcdNumber.display(dt.datetime.now().strftime('%H:%M'))
        self.lcdNumber_5.display('00:00')
        self.lcdNumber_6.display('00:00')
        self.lcdNumber_7.display('00:00')
        self.lcdNumber.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
        self.lcdNumber_2.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
        self.lcdNumber_3.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
        self.lcdNumber_5.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
        self.lcdNumber_6.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
        self.lcdNumber_7.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
        self.design_number = 0
        self.circle_number = 1
        self.pushButton_2.clicked.connect(self.adding)
        self.pushButton.clicked.connect(self.subtraction)
        connection = sqlite3.connect("Music1.db")
        cur = connection.cursor()
        cur.execute('DELETE from music')
        connection.commit()
        connection.close()
        self.comboBox_3.addItem('Добавте мелодию')
        self.pushButton_19.clicked.connect(self.add_music)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.comboBox.currentIndexChanged.connect(self.time_in_zones)
        self.flag = False
        self.timer_flag = False
        self.stopwatch_flag = False
        self.show_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)
        self.lcdNumber_3.setDigitCount(8)
        self.lcdNumber_3.display('00:00:00')
        self.create_table()
        self.pushButton_17.setEnabled(False)
        self.pushButton_17.clicked.connect(self.reading_csv)
        self.pushButton_18.clicked.connect(self.clear_circles)
        self.pushButton_18.setEnabled(False)
        self.pushButton_9.clicked.connect(self.stopwatch_turn)
        self.pushButton_10.clicked.connect(self.stopwatch_pause)
        self.pushButton_11.clicked.connect(self.stopwatch_off)
        self.row = -1
        self.csv_row = []
        self.first = False
        self.pushButton_14.setEnabled(False)
        self.pushButton_14.clicked.connect(self.circle)
        self.stopwatch_time = dt.timedelta(hours=0, minutes=0, seconds=0)
        self.pushButton_3.clicked.connect(self.begin)
        self.pushButton_4.clicked.connect(self.pause)
        self.pushButton_15.setEnabled(False)
        self.pushButton_15.clicked.connect(self.stop)
        self.pushButton_16.clicked.connect(self.zeroing)
        self.lcdNumber_2.setDigitCount(8)
        self.lcdNumber_2.display('00:00:00')
        self.pushButton_13.setEnabled(False)
        self.pushButton_13.clicked.connect(self.disconnection)
        self.lcdNumber_4.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
        self.lcdNumber_4.display('00:00')
        self.pushButton_5.clicked.connect(self.reset)
        self.pushButton_6.clicked.connect(self.set)
        self.pushButton_7.clicked.connect(self.record)
        self.pushButton_8.clicked.connect(self.clear_listWidget)

    # Зададим дизайн виджетам lcdNumber
    def design(self):
        if self.design_number == 0:
            self.lcdNumber.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
            self.lcdNumber_2.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
            self.lcdNumber_3.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
            self.lcdNumber_4.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
            self.lcdNumber_5.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
            self.lcdNumber_6.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
            self.lcdNumber_7.setStyleSheet("""QLCDNumber { background-color: white; color: black }""")
        elif self.design_number == 1:
            self.lcdNumber.setStyleSheet("""QLCDNumber { background-color: white; color: blue }""")
            self.lcdNumber_2.setStyleSheet("""QLCDNumber { background-color: white; color: blue }""")
            self.lcdNumber_3.setStyleSheet("""QLCDNumber { background-color: white; color: blue }""")
            self.lcdNumber_4.setStyleSheet("""QLCDNumber { background-color: white; color: blue }""")
            self.lcdNumber_5.setStyleSheet("""QLCDNumber { background-color: white; color: blue }""")
            self.lcdNumber_6.setStyleSheet("""QLCDNumber { background-color: white; color: blue }""")
            self.lcdNumber_7.setStyleSheet("""QLCDNumber { background-color: white; color: blue }""")
        elif self.design_number == 2:
            self.lcdNumber.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: yellow }""")
            self.lcdNumber_2.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: yellow }""")
            self.lcdNumber_3.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: yellow }""")
            self.lcdNumber_4.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: yellow }""")
            self.lcdNumber_5.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: yellow }""")
            self.lcdNumber_6.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: yellow }""")
            self.lcdNumber_7.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: yellow }""")
        elif self.design_number == 3:
            self.lcdNumber.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: white }""")
            self.lcdNumber_2.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: white }""")
            self.lcdNumber_3.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: white }""")
            self.lcdNumber_4.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: white }""")
            self.lcdNumber_5.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: white }""")
            self.lcdNumber_6.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: white }""")
            self.lcdNumber_7.setStyleSheet("""QLCDNumber { background-color: darkCyan; color: white }""")
        elif self.design_number == 4:
            self.lcdNumber.setStyleSheet("""QLCDNumber { background-color: yellow; color: black }""")
            self.lcdNumber_2.setStyleSheet("""QLCDNumber { background-color: yellow; color: black }""")
            self.lcdNumber_3.setStyleSheet("""QLCDNumber { background-color: yellow; color: black }""")
            self.lcdNumber_4.setStyleSheet("""QLCDNumber { background-color: yellow; color: black }""")
            self.lcdNumber_5.setStyleSheet("""QLCDNumber { background-color: yellow; color: black }""")
            self.lcdNumber_6.setStyleSheet("""QLCDNumber { background-color: yellow; color: black }""")
            self.lcdNumber_7.setStyleSheet("""QLCDNumber { background-color: yellow; color: black }""")
        elif self.design_number == 5:
            self.lcdNumber.setStyleSheet("""QLCDNumber { background-color: yellow; color: orange }""")
            self.lcdNumber_2.setStyleSheet("""QLCDNumber { background-color: yellow; color: orange }""")
            self.lcdNumber_3.setStyleSheet("""QLCDNumber { background-color: yellow; color: orange }""")
            self.lcdNumber_4.setStyleSheet("""QLCDNumber { background-color: yellow; color: orange }""")
            self.lcdNumber_5.setStyleSheet("""QLCDNumber { background-color: yellow; color: orange }""")
            self.lcdNumber_6.setStyleSheet("""QLCDNumber { background-color: yellow; color: orange }""")
            self.lcdNumber_7.setStyleSheet("""QLCDNumber { background-color: yellow; color: orange }""")
        elif self.design_number == 6:
            self.lcdNumber.setStyleSheet("""QLCDNumber { background-color: green; color: white }""")
            self.lcdNumber_2.setStyleSheet("""QLCDNumber { background-color: green; color: white }""")
            self.lcdNumber_3.setStyleSheet("""QLCDNumber { background-color: green; color: white }""")
            self.lcdNumber_4.setStyleSheet("""QLCDNumber { background-color: green; color: white }""")
            self.lcdNumber_5.setStyleSheet("""QLCDNumber { background-color: green; color: white }""")
            self.lcdNumber_6.setStyleSheet("""QLCDNumber { background-color: green; color: white }""")
            self.lcdNumber_7.setStyleSheet("""QLCDNumber { background-color: green; color: white }""")
        elif self.design_number == 7:
            self.lcdNumber.setStyleSheet("""QLCDNumber { background-color: green; color: yellow }""")
            self.lcdNumber_2.setStyleSheet("""QLCDNumber { background-color: green; color: yellow }""")
            self.lcdNumber_3.setStyleSheet("""QLCDNumber { background-color: green; color: yellow }""")
            self.lcdNumber_4.setStyleSheet("""QLCDNumber { background-color: green; color: yellow }""")
            self.lcdNumber_5.setStyleSheet("""QLCDNumber { background-color: green; color: yellow }""")
            self.lcdNumber_6.setStyleSheet("""QLCDNumber { background-color: green; color: yellow }""")
            self.lcdNumber_7.setStyleSheet("""QLCDNumber { background-color: green; color: yellow }""")

    # Обработка нажатий клавиатуры
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_4:
            self.subtraction()
        elif event.key() == Qt.Key_6:
            self.adding()
        elif event.key() == Qt.Key_S:
            self.set()
        elif event.key() == Qt.Key_R:
            self.reset()
        elif event.key() == Qt.Key_Insert:
            self.record()
        elif event.key() == Qt.Key_Delete:
            self.clear_listWidget()
        elif event.key() == Qt.Key_Home:
            self.begin()
        elif event.key() == Qt.Key_End:
            self.zeroing()
        elif event.key() == Qt.Key_Shift:
            self.stopwatch_turn()
        elif event.key() == Qt.Key_CapsLock:
            self.stopwatch_off()

    # Методы adding и subtraction задают номер дизайна, выбранного пользователем
    def adding(self):
        self.design_number += 1
        if self.design_number > 7:
            self.design_number = 7
        self.design()

    def subtraction(self):
        self.design_number -= 1
        if self.design_number < 0:
            self.design_number = 0
        self.design()

    # Получение часовых поясов из базы данных
    def create_spisok(self):
        self.zones = []
        connection = sqlite3.connect("TimeZones.db")
        cur = connection.cursor()
        result = cur.execute("""SELECT * FROM Zones""").fetchall()
        for elem in result:
            self.zones.append(elem[1] + ' ' + elem[2])
        connection.close()

    # Создание времени, соответствующего выбранному часовому поясу
    def time_in_zones(self):
        if self.comboBox.currentIndex() == 1:
            self.time1 = dt.datetime.now() - dt.timedelta(hours = 7)
        elif self.comboBox.currentIndex() == 2:
            self.time1 = dt.datetime.now() - dt.timedelta(hours = 6)
        elif self.comboBox.currentIndex() == 3:
            self.time1 = dt.datetime.now() - dt.timedelta(hours = 5)
        elif self.comboBox.currentIndex() == 4:
            self.time1 = dt.datetime.now() - dt.timedelta(hours = 4)
        elif self.comboBox.currentIndex() == 5:
            self.time1 = dt.datetime.now() - dt.timedelta(hours = 3)
        elif self.comboBox.currentIndex() == 6:
            self.time1 = dt.datetime.now() - dt.timedelta(hours = 2)
        elif self.comboBox.currentIndex() == 7:
            self.time1 = dt.datetime.now() - dt.timedelta(hours = 1)
        elif self.comboBox.currentIndex() == 8:
            self.time1 = dt.datetime.now()
        elif self.comboBox.currentIndex() == 9:
            self.time1 = dt.datetime.now() + dt.timedelta(hours = 1)
        if self.comboBox_2.currentIndex() == 1:
            self.time2 = dt.datetime.now() - dt.timedelta(hours = 7)
        elif self.comboBox_2.currentIndex() == 2:
            self.time2 = dt.datetime.now() - dt.timedelta(hours = 6)
        elif self.comboBox_2.currentIndex() == 3:
            self.time2 = dt.datetime.now() - dt.timedelta(hours = 5)
        elif self.comboBox_2.currentIndex() == 4:
            self.time2 = dt.datetime.now() - dt.timedelta(hours = 4)
        elif self.comboBox_2.currentIndex() == 5:
            self.time2 = dt.datetime.now() - dt.timedelta(hours = 3)
        elif self.comboBox_2.currentIndex() == 6:
            self.time2 = dt.datetime.now() - dt.timedelta(hours = 2)
        elif self.comboBox_2.currentIndex() == 7:
            self.time2 = dt.datetime.now() - dt.timedelta(hours = 1)
        elif self.comboBox_2.currentIndex() == 8:
            self.time2 = dt.datetime.now()
        elif self.comboBox_2.currentIndex() == 9:
            self.time2 = dt.datetime.now() + dt.timedelta(hours = 1)
        if self.comboBox_4.currentIndex() == 1:
            self.time3 = dt.datetime.now() - dt.timedelta(hours = 7)
        elif self.comboBox_4.currentIndex() == 2:
            self.time3 = dt.datetime.now() - dt.timedelta(hours = 6)
        elif self.comboBox_4.currentIndex() == 3:
            self.time3 = dt.datetime.now() - dt.timedelta(hours = 5)
        elif self.comboBox_4.currentIndex() == 4:
            self.time3 = dt.datetime.now() - dt.timedelta(hours = 4)
        elif self.comboBox_4.currentIndex() == 5:
            self.time3 = dt.datetime.now() - dt.timedelta(hours = 3)
        elif self.comboBox_4.currentIndex() == 6:
            self.time3 = dt.datetime.now() - dt.timedelta(hours = 2)
        elif self.comboBox_4.currentIndex() == 7:
            self.time3 = dt.datetime.now() - dt.timedelta(hours = 1)
        elif self.comboBox_4.currentIndex() == 8:
            self.time3 = dt.datetime.now()
        elif self.comboBox_4.currentIndex() == 9:
            self.time3 = dt.datetime.now() + dt.timedelta(hours = 1)

    # Вывод значений времени в виджеты lcdNumber
    def show_time(self):
        self.time_in_zones()
        if self.comboBox.currentIndex() == 0:
            self.lcdNumber_5.display('00:00')
        else:
            if int(dt.datetime.now().strftime('%S')) % 2 == 0:
                self.lcdNumber_5.display(self.time1.strftime('%H:%M'))
            else:
                self.lcdNumber_5.display(self.time1.strftime('%H %M'))
        if self.comboBox_2.currentIndex() == 0:
            self.lcdNumber_7.display('00:00')
        else:
            if int(dt.datetime.now().strftime('%S')) % 2 == 0:
                self.lcdNumber_7.display(self.time2.strftime('%H:%M'))
            else:
                self.lcdNumber_7.display(self.time2.strftime('%H %M'))
        if self.comboBox_4.currentIndex() == 0:
            self.lcdNumber_6.display('00:00')
        else:
            if int(dt.datetime.now().strftime('%S')) % 2 == 0:
                self.lcdNumber_6.display(self.time3.strftime('%H:%M'))
            else:
                self.lcdNumber_6.display(self.time3.strftime('%H %M'))
        if int(dt.datetime.now().strftime('%S')) % 2 == 0:
            self.lcdNumber.display(dt.datetime.now().strftime('%H:%M'))
        else:
            self.lcdNumber.display(dt.datetime.now().strftime('%H %M'))
        if self.flag:
            if self.chosen_time == dt.datetime.now().strftime('%H:%M') and self.date == self.chosen_date:
                self.flag = False
                self.activation()
        if self.timer_flag:
            if self.countdown == dt.timedelta(hours=0, minutes=0, seconds=0):
                self.timer_flag = False
                self.ring()
            else:
                self.countdown -= dt.timedelta(hours=0, minutes=0, seconds=1)
                self.lcdNumber_2.display('0' + str(self.countdown))
        if self.stopwatch_flag:
            self.stopwatch_time += dt.timedelta(hours=0, minutes=0, seconds=1)
            self.lcdNumber_3.display('0' + str(self.stopwatch_time))
        self.message()

    # Вывод напоминаний в определенное время
    def message(self):
        time = dt.datetime.now().time().strftime('%H:%M')
        if time == '12:50':
            self.label_8.setText('Время {}: не забудь пообедать'.format(time))
            self.label_8.setFont(QFont("Times", 24, QFont.Bold))
            self.label_8.setStyleSheet("QLabel { background-color : #ff4040; color : #fffafa; }")
        elif time == '14:30':
            self.label_8.setText('Время {}: сделай зарядку для глаз'.format(time))
            self.label_8.setFont(QFont("Times", 24, QFont.Bold))
            self.label_8.setStyleSheet("QLabel { background-color : #ff4040; color : #fffafa; }")
        elif time == '18:50':
            self.label_8.setText('Время {}: не забудь поужинать'.format(time))
            self.label_8.setFont(QFont("Times", 24, QFont.Bold))
            self.label_8.setStyleSheet("QLabel { background-color : #ff4040; color : #fffafa; }")
        elif time == '22:50':
            self.label_8.setText('Время {}: тебе следует лечь спать'.format(time))
            self.label_8.setFont(QFont("Times", 24, QFont.Bold))
            self.label_8.setStyleSheet("QLabel { background-color : #ff4040; color : #fffafa; }")
        elif dt.datetime.now().time().strftime('%M') == '20':
            self.label_8.setText('Время {}: выпрями спину'.format(time))
            self.label_8.setFont(QFont("Times", 24, QFont.Bold))
            self.label_8.setStyleSheet("QLabel { background-color : #ff4040; color : #fffafa; }")
        else:
            self.label_8.setText('')
            self.label_8.setStyleSheet("QLabel { background-color : transparent; color :transparent; }")

    # Вывод информации о музыкальных файлах из базы данных
    def create_music_spisok(self):
        connection = sqlite3.connect("Music1.db")
        cur = connection.cursor()
        result = cur.execute("""SELECT * FROM music""").fetchall()
        self.music = []
        self.way = {}
        for elem in result:
            if elem[1] not in self.way:
                self.way[elem[1]] = elem[0]
                self.music.append(elem[1])
        self.comboBox_3.addItems(self.music)
        connection.close()
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)

    # Добавление информации о музыкальных файлах в базу данных и виджет comboBox
    def add_music(self):
        way = QFileDialog.getOpenFileName(self, 'Выбрать композицию', '', 'Файл (*.mp3)')[0]
        name = way.split('/')
        name = name[len(name) - 1]
        connection = sqlite3.connect("Music1.db")
        cur = connection.cursor()
        cur.execute('INSERT INTO music(way, name) VALUES (?, ?)', (way, name))
        connection.commit()
        connection.close()
        self.comboBox_3.clear()
        self.create_music_spisok()

    # Выбор даты и времени для установки будильника
    # Вывод сообщения об ошибке при выборе прошедшего времени
    def set(self):
        self.chosen_time = self.dateTimeEdit.time().toString('HH:mm')
        self.chosen_date = self.dateTimeEdit.date().toString('dd-MM-yyyy')
        try:
            if self.comparison():
                self.lcdNumber_4.display(self.chosen_time)
                self.flag = True
                self.label_7.setText('')
        except DateError as de:
            self.label_7.setText('Ошибка: {}'.format(de))

    # Сброс установленного времени
    def reset(self):
        self.lcdNumber_4.display('00:00')
        self.flag = False

    # Сравнение даты и времени в данный момент с датой и временем, на которые установлен будильник
    def comparison(self):
        self.date = dt.date.today().strftime('%d-%m-%Y')
        self.spisok1 = self.date.split('-')
        self.spisok2 = self.chosen_date.split('-')
        if int(self.spisok1[2]) > int(self.spisok2[2]):
            fit = False
        elif int(self.spisok1[2]) < int(self.spisok2[2]):
            fit = True
        else:
            if int(self.spisok1[1]) < int(self.spisok2[1]):
                fit = True
            else:
                if int(self.spisok1[0]) < int(self.spisok2[0]):
                    fit = True
                elif int(self.spisok1[0]) == int(self.spisok2[0]) \
                        and self.chosen_time >= dt.datetime.now().strftime('%H:%M'):
                    fit = True
                else:
                    fit = False
        if fit:
            return True
        else:
            raise DateError('Выбраны недопустимые дата и время')

    # Воспроизведение выбранной мелодии при наступлении выбранного времени
    def activation(self):
        filename = self.way[self.music[self.comboBox_3.currentIndex()]]
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()
        self.pushButton_13.setEnabled(True)

    # Отключение будильника
    def disconnection(self):
        self.pushButton_13.setEnabled(False)
        self.player.stop()

    # Считывание пользовательского ввода из виджета lineEdit, добавление в listWidget
    def record(self):
        self.text = self.lineEdit.text()
        self.listWidget.addItem(self.text)

    # Очистка listWidget
    def clear_listWidget(self):
        self.listWidget.clear()

    # Установка выбранного времени в lcdNumber, запуск работы таймера
    def begin(self):
        self.countdown = self.timeEdit.dateTime().toString('HH:mm:ss')
        self.lcdNumber_2.display(self.countdown)
        self.countdown = self.countdown.split(':')
        self.countdown = dt.timedelta(hours=int(self.countdown[0]),
                                      minutes=int(self.countdown[1]), seconds=int(self.countdown[2]))
        self.timer_flag = True
        self.pushButton_15.setEnabled(False)

    # Воспроизведение сигнала об окончании по истечении времени
    def ring(self):
        media = QtCore.QUrl.fromLocalFile('beep.mp3')
        content = QtMultimedia.QMediaContent(media)
        self.player2 = QtMultimedia.QMediaPlayer()
        self.player2.setMedia(content)
        self.player2.play()
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_16.setEnabled(False)
        self.pushButton_15.setEnabled(True)

    # Установка таймера на паузу/остановка паузы таймера
    def pause(self):
        if self.sender().text() == 'Пауза':
            self.timer_flag = False
            self.pushButton_4.setText('Продолжить')
        else:
            self.timer_flag = True
            self.pushButton_4.setText('Пауза')

    # Выключение сигнала об окончании
    def stop(self):
        self.player2.stop()
        self.lcdNumber_2.display('00:00:00')
        self.timer_flag = False
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_16.setEnabled(True)

    # Обнуление таймера
    def zeroing(self):
        self.lcdNumber_2.display('00:00:00')
        self.timer_flag = False

    # Включение секундомера
    def stopwatch_turn(self):
        self.pushButton_14.setEnabled(True)
        self.pushButton_10.setEnabled(True)
        self.stopwatch_flag = True
        self.pushButton_9.setEnabled(False)

    # Установка секундомера на паузу/остановка паузы секундомера
    def stopwatch_pause(self):
        if self.sender().text() == 'Пауза':
            self.stopwatch_flag = False
            self.pushButton_14.setEnabled(False)
            self.pushButton_10.setText('Продолжить')
        else:
            self.stopwatch_flag = True
            self.pushButton_10.setText('Пауза')
            self.pushButton_14.setEnabled(True)

    def stopwatch_off(self):
        self.stopwatch_flag = False
        self.pushButton_10.setEnabled(False)
        self.pushButton_14.setEnabled(False)
        self.pushButton_17.setEnabled(True)
        self.pushButton_9.setEnabled(True)
        self.lcdNumber_3.display('00:00:00')
        self.stopwatch_time = dt.timedelta(hours=0, minutes=0, seconds=0)
        self.circle_number = 1
        self.row = -1
        if self.tableWidget.item(0, 0) is not None:
            self.write_to_csv()
        count = self.tableWidget.rowCount()
        for i in range(count):
            self.tableWidget.removeRow(0)

    # Создание столбцов и заголовков в tableWidget для записи времени кругов
    def create_table(self):
        self.tableWidget.setColumnCount(2)
        item1 = QTableWidgetItem('Номер круга')
        item1.setBackground(QColor(31, 206, 203))
        self.tableWidget.setHorizontalHeaderItem(0,item1)
        item2 = QTableWidgetItem('Время')
        item2.setBackground(QColor(31, 206, 203))
        self.tableWidget.setHorizontalHeaderItem(1,item2)

    # Добавление времени одного круга в tableWidget
    def circle(self):
        self.result = QTableWidgetItem(str(self.stopwatch_time))
        self.item = QTableWidgetItem(str(self.circle_number))
        self.item.setTextAlignment(Qt.AlignHCenter)
        self.result.setTextAlignment(Qt.AlignHCenter)
        self.row += 1
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setItem(self.row, 0, self.item)
        self.tableWidget.setItem(self.row, 1, self.result)
        self.circle_number += 1

    # Добавление данных из tableWidget в csv-файл
    def write_to_csv(self):
        with open('circles.csv', 'w', newline='', encoding="utf8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([self.tableWidget.horizontalHeaderItem(i).text() for i in range(2)])
            for i in range(0, len(self.csv_row) - 1, 2):
                row = []
                row.append(self.csv_row[i])
                row.append(self.csv_row[i + 1])
                writer.writerow(row)
            for i in range(self.tableWidget.rowCount()):
                row = []
                for j in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(i, j)
                    if item is not None:
                        row.append(item.text())
                        self.csv_row.append(item.text())
                writer.writerow(row)
            csvfile.close()

    # Чтение csv-файла и вывод информации в listWidget
    def reading_csv(self):
        count = 1
        self.listWidget_2.clear()
        self.pushButton_18.setEnabled(True)
        with open('circles.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for index, row in enumerate(reader):
                if row[0] == '1':
                    self.listWidget_2.addItem(str(count) + ' запись')
                    count += 1
                if row[0] != 'Номер круга':
                    self.listWidget_2.addItem(row[0] + ':   ' + row[1])
            csvfile.close()

    # Очистка listWidget от всех записей
    def clear_circles(self):
        self.csv_row = []
        self.listWidget_2.clear()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = Clock()
    ex.show()
    ex.setWindowTitle("Универсальные часы")
    sys.excepthook = except_hook
    sys.exit(app.exec())