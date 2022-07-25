import threading
from PyQt5 import QtCore, QtGui, QtWidgets

from input_listener import InputListener

class Play(object):
    def setupUi(self, MainWindow, ParentWindow, project):
        self.project = project
        self.play_toggle = True
        self.listener = InputListener()

        self.MainWindow = MainWindow
        self.ParentWindow = ParentWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(530, 173)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 531, 281))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(75, 40, 381, 103))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 700, 31))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(470, 10, 101, 35))
        font = QtGui.QFont()
        font.setFamily("Perpetua")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 530, 26))
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
        self.MainWindow.setWindowTitle(_translate("MainWindow", f"AMS - Play: {self.project}"))
        self.pushButton.setText(_translate("MainWindow", "Play"))
        self.pushButton.setStyleSheet("background-color:rgb(151, 152, 153); color:white")
        self.frame.setStyleSheet("background-color:rgb(90, 90, 90)")
        self.label_2.setText(f"<font color='light gray'>Play: {self.project}</font>")
        self.label_3.setText("<font color='light gray'>Play</font>")
        self.pushButton.clicked.connect(self.clicked)
    
    def clicked(self):
        if self.play_toggle:
            self.ParentWindow.showMinimized()
            self.MainWindow.showMinimized()
            self.pushButton.setText("Stop")
            self.label_3.setGeometry(QtCore.QRect(420, 10, 101, 35))
            self.label_3.setText("<font color='light gray'>Playing</font>")
            self.listener.play(self.project)
            threading.Thread(target=self.check_listener).start()
            self.play_toggle = False
        else:
            self.pushButton.setText("Play")
            self.label_3.setGeometry(QtCore.QRect(470, 10, 101, 35))
            self.label_3.setText("<font color='light gray'>Play</font>")
            self.play_toggle = True
    
    def check_listener(self):
        while True:
            if not self.listener.is_playing:
                self.clicked()
                break