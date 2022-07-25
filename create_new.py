from re import S
import threading
from PyQt5 import QtCore, QtGui, QtWidgets

from input_listener import InputListener

class Create(object):
    def setupUi(self, MainWindow, ParentWindow):
        self.listener = InputListener()

        self.MainWindow = MainWindow
        self.ParentWindow = ParentWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(412, 166)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.project_name = QtWidgets.QTextEdit(self.centralwidget)
        self.project_name.setGeometry(QtCore.QRect(190, 20, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.project_name.setFont(font)
        self.project_name.setObjectName("project_name")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 60, 231, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setStrikeOut(False)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 411, 131))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.raise_()
        self.project_name.raise_()
        self.label.raise_()
        self.pushButton.raise_()
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 412, 26))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "AMS - Create New"))
        self.project_name.setText(_translate("MainWindow", "Untitled Project"))
        self.label.setText(_translate("MainWindow", "Project Name"))
        self.pushButton.setText(_translate("MainWindow", "Record Macros"))
        self.pushButton.clicked.connect(self.clicked)

    def clicked(self):
        self.ParentWindow.showMinimized()
        self.MainWindow.showMinimized()
        self.pushButton.setText(f"{self.listener.hotkey} to stop")
        self.listener.start()
        self.listener.wait_for_hotkey()
        self.listener.stop()
        self.listener.save_events(self.project_name.toPlainText())
        self.pushButton.setText("Record")
        self.label.setText("Saved Project!")
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Create()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
