import sys
from PyQt4.QtGui import *

import main_window


def callback(arg):
    print "hello world"
    print arg


app = QApplication(sys.argv)
window = QMainWindow()

ui_mainWindow = main_window.Ui_MainWindow()
ui_mainWindow.setupUi(window)

ui_mainWindow.b00.setText("Something")

button = QToolButton()

ui_mainWindow.gridLayout.addWidget(button, 1, 4, 1, 1)

button.clicked.connect(callback)



window.show()
sys.exit(app.exec_())