# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Thu Oct  8 19:54:49 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(491, 320)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 30, 381, 221))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.b10 = QtGui.QToolButton(self.gridLayoutWidget)
        self.b10.setObjectName(_fromUtf8("b10"))
        self.gridLayout.addWidget(self.b10, 1, 1, 1, 1)
        self.b00 = QtGui.QToolButton(self.gridLayoutWidget)
        self.b00.setObjectName(_fromUtf8("b00"))
        self.gridLayout.addWidget(self.b00, 1, 0, 1, 1)
        self.b21 = QtGui.QToolButton(self.gridLayoutWidget)
        self.b21.setObjectName(_fromUtf8("b21"))
        self.gridLayout.addWidget(self.b21, 0, 2, 1, 1)
        self.b11 = QtGui.QToolButton(self.gridLayoutWidget)
        self.b11.setObjectName(_fromUtf8("b11"))
        self.gridLayout.addWidget(self.b11, 0, 1, 1, 1)
        self.b01 = QtGui.QToolButton(self.gridLayoutWidget)
        self.b01.setObjectName(_fromUtf8("b01"))
        self.gridLayout.addWidget(self.b01, 0, 0, 1, 1)
        self.b31 = QtGui.QToolButton(self.gridLayoutWidget)
        self.b31.setObjectName(_fromUtf8("b31"))
        self.gridLayout.addWidget(self.b31, 0, 3, 1, 1)
        self.b20 = QtGui.QToolButton(self.gridLayoutWidget)
        self.b20.setObjectName(_fromUtf8("b20"))
        self.gridLayout.addWidget(self.b20, 1, 2, 1, 1)
        self.b30 = QtGui.QToolButton(self.gridLayoutWidget)
        self.b30.setObjectName(_fromUtf8("b30"))
        self.gridLayout.addWidget(self.b30, 1, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 491, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.b10.setText(_translate("MainWindow", "...", None))
        self.b00.setText(_translate("MainWindow", "...", None))
        self.b21.setText(_translate("MainWindow", "...", None))
        self.b11.setText(_translate("MainWindow", "...", None))
        self.b01.setText(_translate("MainWindow", "...", None))
        self.b31.setText(_translate("MainWindow", "...", None))
        self.b20.setText(_translate("MainWindow", "...", None))
        self.b30.setText(_translate("MainWindow", "...", None))
