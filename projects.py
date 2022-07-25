import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets

from play import Play
from create_new import Create
from input_listener import InputListener

class Projects(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(800, 586)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.root = QtWidgets.QFrame(self.centralwidget)
        self.root.setGeometry(QtCore.QRect(0, 0, 801, 571))
        self.root.setAutoFillBackground(False)
        self.root.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.root.setFrameShadow(QtWidgets.QFrame.Raised)
        self.root.setObjectName("root")
        self.play = QtWidgets.QPushButton(self.centralwidget)
        self.play.setGeometry(QtCore.QRect(540, 440, 251, 111))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.play.setFont(font)
        self.play.setObjectName("play")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.list = QtWidgets.QListWidget(self.centralwidget)
        self.list.setGeometry(QtCore.QRect(10, 30, 781, 401))
        self.list.setObjectName("list")
        self.load = QtWidgets.QPushButton(self.centralwidget)
        self.load.setGeometry(QtCore.QRect(275, 440, 251, 111))
        self.MainWindow.setCentralWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.load.setFont(font)
        self.load.setObjectName("load")
        self.create_new = QtWidgets.QPushButton(self.centralwidget)
        self.create_new.setGeometry(QtCore.QRect(10, 440, 251, 111))
        self.settings = QtWidgets.QPushButton(self.centralwidget)
        self.settings.setGeometry(QtCore.QRect(727, 10, 60, 20))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.create_new.setFont(font)
        self.create_new.setObjectName("settings")
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.create_new.setFont(font)
        self.create_new.setObjectName("create_new")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.play.setText(_translate("MainWindow", "Play"))
        self.load.setText(_translate("MainWindow", "Load"))
        self.create_new.setText(_translate("MainWindow", "Create New"))
        self.settings.setText(_translate("MainWindow", "Settings"))
        self.root.setStyleSheet("background-color:rgb(90, 90, 90)")
        self.create_new.setStyleSheet("background-color:rgb(151, 152, 153); color:white")
        self.play.setStyleSheet("background-color:rgb(151, 152, 153); color:white")
        self.load.setStyleSheet("background-color:rgb(151, 152, 153); color:white")
        self.label.setText("<font color='light gray'>Projects</font>")
        self.list.itemPressed.connect(self.onItemSelect)
        self.play.clicked.connect(self.play_window)
        self.create_new.clicked.connect(self.create_window)
        self.load.clicked.connect(self.load_file)
        
        try:
            self.list.addItems(InputListener().get_projects())
        except:
            pass
    
    def onItemSelect(self, item):
        self.selectedItem = item.text()

    def play_window(self):
        self.play_win = QtWidgets.QMainWindow()
        self.ui = Play()
        self.ui.setupUi(self.play_win, self.MainWindow, self.selectedItem)
        self.play_win.show()

    def create_window(self):
        self.create_win = QtWidgets.QMainWindow()
        self.ui = Create()
        self.ui.setupUi(self.create_win, self.MainWindow)
        self.create_win.show()
    
    def load_file(self):
        os.startfile(f"projects\{self.selectedItem}.log")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Projects()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
