#!/usr/bin/env python3
# coding=utf-8

import sys
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QButtonGroup

answers = ['', '', '']  # 1 - form2, 2 - form3, 3 - form4


class Form1(QtWidgets.QMainWindow):
    # аргумент str говорит о том, что сигнал должен быть сторокового типа
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form1, self).__init__()
        uic.loadUi('uis/form1.ui', self)

        self.setWindowTitle('Приветсвтие')
        self.setWindowIcon(QtGui.QIcon('images/icon.png'))

        self.btn_exit.clicked.connect(self.close)
        self.btn_begin.clicked.connect(self.next)

    def next(self):
        self.switch_window.emit('1>2')


class Form2(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form2, self).__init__()
        uic.loadUi('uis/form3.ui', self)

        self.setWindowTitle('Детсво')

        self.setWindowIcon(QtGui.QIcon('images/icon.png'))
        self.label_img.setPixmap(QPixmap('images/student.png'))
        self.label_img.setScaledContents(True)

        if answers[0] is not None:
            self.label_selected.setText('Выбрано: ' + answers[0])

        self.button_group = QButtonGroup()

        self.button_group.addButton(self.checkBox, 1)
        self.button_group.addButton(self.checkBox_2, 2)
        self.button_group.addButton(self.checkBox_3, 3)
        self.button_group.addButton(self.checkBox_4, 4)

        self.checkBox.stateChanged.connect(
            lambda: self.onToggled(self.checkBox))
        self.checkBox_2.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_2))
        self.checkBox_3.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_3))
        self.checkBox_4.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_4))

        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)

        self.onToggled(self.checkBox)

    def onToggled(self, checkbox):
        if checkbox.isChecked():
            answers[0] = checkbox.text()
            self.label_selected.setText('Выбрано: ' + answers[0])

    def back(self):
        self.switch_window.emit('1<2')

    def next(self):
        self.switch_window.emit('2>3')


class Form3(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form3, self).__init__()
        uic.loadUi('uis/form2.ui', self)

        self.setWindowTitle('Отрочество')
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))
        self.label_img.setPixmap(QPixmap('images/games.png'))
        self.label_img.setScaledContents(True)

        # запрещаем редактирование таблицы
        #        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)

    def back(self):
        self.switch_window.emit('2<3')

    def next(self):
        self.switch_window.emit('3>4')
        answers[1] = self.tableWidget.item(0, 0).text()


class Form4(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form4, self).__init__()
        uic.loadUi('uis/form4.ui', self)

        self.setWindowTitle('Юность')

        self.setWindowIcon(QtGui.QIcon('images/logo.png'))
        self.label_img.setPixmap(QPixmap('images/subjects.png'))
        self.label_img.setScaledContents(True)

        if answers[2] is not None:
            self.label_selected.setText('Выбрано: ' + answers[2])

        self.listWidget.clicked.connect(self.listWidget_clicked)
        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)

        self.listWidget.setCurrentRow(0)
        self.listWidget_clicked()

    def listWidget_clicked(self):
        answers[2] = self.listWidget.currentItem().text()
        self.label_selected.setText('Выбрано: ' + answers[2])

    def back(self):
        self.switch_window.emit('3<4')

    def next(self):
        self.switch_window.emit('4>5')


class Form5(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form5, self).__init__()
        uic.loadUi('uis/form5.ui', self)

        self.setWindowTitle('Результат')
        self.setWindowIcon(QtGui.QIcon('images/icon.png'))

        # запрещаем редактирование таблицы
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # присваиваем значение ячейкам таблицы
        self.tableWidget.setItem(0, 0,
                                 QTableWidgetItem('Ваш любимый мультфильм'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(answers[0]))

        self.tableWidget.setItem(1, 0,
                                 QTableWidgetItem('Ваша любимая компьютерная игра'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem(answers[1]))

        self.tableWidget.setItem(2, 0,
                                 QTableWidgetItem('Ваша цель в жизни'))
        self.tableWidget.setItem(2, 1, QTableWidgetItem(answers[2]))

        self.btn_back.clicked.connect(self.back)
        self.btn_exit.clicked.connect(self.close)

    def back(self):
        self.switch_window.emit("4<5")


'''
Класс управления переключения окон
'''


class Controller:
    def __init__(self):
        pass

    def select_forms(self, text):
        if text == '1':
            self.form1 = Form1()
            self.form1.switch_window.connect(self.select_forms)
            self.form1.show()

        if text == '1>2':
            self.form2 = Form2()
            self.form2.switch_window.connect(self.select_forms)
            self.form2.show()
            self.form1.close()

        if text == '2>3':
            self.form3 = Form3()
            self.form3.switch_window.connect(self.select_forms)
            self.form3.show()
            self.form2.close()

        if text == '3>4':
            self.form4 = Form4()
            self.form4.switch_window.connect(self.select_forms)
            self.form4.show()
            self.form3.close()

        if text == '4>5':
            self.form5 = Form5()
            self.form5.switch_window.connect(self.select_forms)
            self.form5.show()
            self.form4.close()

        if text == '4<5':
            self.form4 = Form4()
            self.form4.switch_window.connect(self.select_forms)
            self.form4.show()
            self.form5.close()

        if text == '3<4':
            self.form3 = Form3()
            self.form3.switch_window.connect(self.select_forms)
            self.form3.show()
            self.form4.close()

        if text == '2<3':
            self.form2 = Form2()
            self.form2.switch_window.connect(self.select_forms)
            self.form2.show()
            self.form3.close()

        if text == '1<2':
            self.form1 = Form1()
            self.form1.switch_window.connect(self.select_forms)
            self.form1.show()
            self.form2.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.select_forms("1")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
