# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1050, 490)
        #Form.setStyleSheet("")
        #Form.setWindowIcon(QIcon('./friend.jpg'))
        self.text_2 = QtWidgets.QTextEdit(Form)
        self.text_2.setGeometry(QtCore.QRect(50, 120, 201, 241))
        self.text_2.setObjectName("text_2")
        self.button_1 = QtWidgets.QPushButton(Form)
        self.button_1.setGeometry(QtCore.QRect(270, 180, 90, 35))
        self.button_1.setObjectName("button_1")
        self.button_2 = QtWidgets.QPushButton(Form)
        self.button_2.setGeometry(QtCore.QRect(100, 380, 110, 25))
        self.button_2.setObjectName("button_2")
        self.button_3 = QtWidgets.QPushButton(Form)
        self.button_3.setGeometry(QtCore.QRect(600, 380, 110, 25))
        self.button_3.setObjectName("button_3")
        self.button_4 = QtWidgets.QPushButton(Form)
        self.button_4.setGeometry(QtCore.QRect(270, 250, 90, 25))
        self.button_4.setObjectName("button_4")
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setGeometry(QtCore.QRect(60, 90, 191, 16))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(630, 90, 131, 16))
        self.label_2.setObjectName("label_2")
        self.text_1 = QtWidgets.QTextEdit(Form)
        self.text_1.setGeometry(QtCore.QRect(380, 120, 600, 241))
        self.text_1.setObjectName("text_1")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(350, 10, 350, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        self.button_1.clicked.connect(Form.telnetping)
        self.button_2.clicked.connect(Form.telnetonly)
        self.button_3.clicked.connect(Form.pingonly)
        self.button_4.clicked.connect(Form.cleantext)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "全时IP、端口连通性检测"))
        self.button_1.setText(_translate("Form", "Start test"))
        self.button_1.setToolTip(_translate("Form","开始telnet和ping测试\n两个测试全部完成后才显示结果"))
        self.button_2.setText(_translate("Form", "Start telnet"))
        self.button_2.setToolTip(_translate("Form","开始telnet测试"))
        self.button_3.setText(_translate("Form", "Start ping"))
        self.button_3.setToolTip(_translate("Form","开始ping测试"))
        self.button_4.setText(_translate("Form", "Clean Text"))
        self.button_4.setToolTip(_translate("Form","清空文本框"))
        self.label_1.setText(_translate("Form", "显示telnet不通的IP和端口"))
        self.label_2.setText(_translate("Form", "显示ping不通的结果"))
        self.label_3.setText(_translate("Form", "Welcome to this IP test tool!"))

