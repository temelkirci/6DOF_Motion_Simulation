import sys
import os
import traceback
import socket
from threading import Thread

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Server import Server
from StewartPlatform import StewartPlatform
from PlotCanvas import WidgetPlot, Hexapod3D

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'DOF Motion Simulator'

        screenShape = QDesktopWidget().screenGeometry()

        self.left = 0
        self.top = 0
        self.width = screenShape.width()
        self.height = screenShape.height()

        QMainWindow.__init__(self)
        self.title = 'DOF Motion Editor'
        self.statusBar().showMessage('Ready')

        self.startPLCAuto = QPushButton('Start PLC Auto', self)
        self.startPLCAuto.clicked.connect(self.startPlcAuto)
        self.startPLCAuto.setGeometry(1050, 80, 100, 50)

        self.startPLCManual = QPushButton('Start PLC Manual', self)
        self.startPLCManual.clicked.connect(self.startPlcManual)
        self.startPLCManual.setGeometry(1050, 150, 100, 50)


        self.frame1 = QFrame(self)
        self.frame1.setGeometry(QRect(1000, 250, 180, 580))

        self.slider_roll = QSlider(self.frame1)
        self.slider_roll.setValue(0)
        self.slider_roll.setFocusPolicy(Qt.StrongFocus)
        self.slider_roll.setTickPosition(QSlider.TicksBothSides)
        self.slider_roll.setTickInterval(10)
        self.slider_roll.setSingleStep(1)
        self.slider_roll.setMaximum(15)
        self.slider_roll.setMinimum(-15)
        self.slider_roll.move(10, 50)


        self.slider_pitch = QSlider(self.frame1)
        self.slider_pitch.setValue(0)
        self.slider_pitch.setFocusPolicy(Qt.StrongFocus)
        self.slider_pitch.setTickPosition(QSlider.TicksBothSides)
        self.slider_pitch.setTickInterval(10)
        self.slider_pitch.setSingleStep(1)
        self.slider_pitch.setMaximum(15)
        self.slider_pitch.setMinimum(-15)
        self.slider_pitch.move(80, 50)


        self.slider_yaw = QSlider(self.frame1)
        self.slider_yaw.setValue(0)
        self.slider_yaw.setFocusPolicy(Qt.StrongFocus)
        self.slider_yaw.setTickPosition(QSlider.TicksBothSides)
        self.slider_yaw.setTickInterval(10)
        self.slider_yaw.setSingleStep(1)
        self.slider_yaw.setMaximum(15)
        self.slider_yaw.setMinimum(-15)
        self.slider_yaw.move(150, 50)


        self.widgetPlot = WidgetPlot(self)
        self.widgetPlot.setGeometry(0,0,1000,screenShape.height()-80)

        self.widgetHexapod = Hexapod3D(self)
        self.widgetHexapod.setGeometry(1020, 420, screenShape.width()/2 - 100, screenShape.height()/2)

        self.initUI()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "All Files (*);;Text Files (*.txt);; CSV Files (*.csv);; Dat Files (*.dat)", options=options)
        if filePath:
            fileName = os.path.basename(filePath)
            self.statusBar().showMessage(fileName + '  was saved')
            print(fileName)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "All Files (*);;Text Files (*.txt);; CSV Files (*.csv);; Dat Files (*.dat)", options=options)
        if filePath:
            fileName = os.path.basename(filePath)
            self.statusBar().showMessage('Selected File : ' + fileName)
            print(fileName)


    def initUI(self):
        self.setWindowTitle(self.title)
        #self.setMinimumSize(QSize(1280, 640))
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setFixedSize(self.width, self.height)
        #self.setWindowIcon(QIcon('web.png'))

        self.GameIP = QLabel("Game IP Address :  " + socket.gethostbyname(socket.gethostname()), self)
        self.GameIP.setFont(QFont('SansSerif', 11, QFont.Normal))
        self.GameIP.setGeometry(1500, 50, 300, 100)

        self.initMenu()
        """
        self.myIP = QLabel("My IP Address     :  " + self.serverOBJ.TCP_IP, self)
        self.myIP.setFont(QtGui.QFont('SansSerif', 11, QFont.Bold))
        self.myIP.setGeometry(50, 50, 300, 100)
        
        self.myPort = QLabel("My Port Number  :  " + str(self.serverOBJ.TCP_PORT), self)
        self.myPort.setFont(QtGui.QFont('SansSerif', 11, QFont.Bold))
        self.myPort.setGeometry(50, 80, 300, 100)

        self.roll = QLabel("Roll ", self)
        self.roll.setFont(QtGui.QFont('SansSerif', 10, QFont.Bold))
        self.roll.setGeometry(50, 300, 100, 100)

        self.pitch = QLabel("Pitch ", self)
        self.pitch.setFont(QtGui.QFont('SansSerif', 10, QFont.Bold))
        self.pitch.setGeometry(50, 350, 100, 100)

        self.yaw = QLabel("Yaw " , self)
        self.yaw.setFont(QtGui.QFont('SansSerif', 10, QFont.Bold))
        self.yaw.setGeometry(50, 400, 100, 100)

        self.surge = QLabel("Surge ", self)
        self.surge.setFont(QtGui.QFont('SansSerif', 10, QFont.Bold))
        self.surge.setGeometry(50, 450, 100, 100)

        self.sway = QLabel("Sway ", self)
        self.sway.setFont(QtGui.QFont('SansSerif', 10, QFont.Bold))
        self.sway.setGeometry(50, 500, 100, 100)

        self.heave = QLabel("Heave ", self)
        self.heave.setFont(QtGui.QFont('SansSerif', 10, QFont.Bold))
        self.heave.setGeometry(50, 550, 100, 100)

        self.rawDegree = QLabel("Raw Degree ", self)
        self.rawDegree.setFont(QtGui.QFont('SansSerif', 10, QFont.Bold))
        self.rawDegree.setGeometry(150, 250, 100, 100)

        self.Degree = QLabel("Degree ", self)
        self.Degree.setFont(QtGui.QFont('SansSerif', 10, QFont.Bold))
        self.Degree.setGeometry(250, 250, 100, 100)

        self.minimum = QLabel("Minimum ", self)
        self.minimum.setFont(QtGui.QFont('SansSerif', 10, QFont.Bold))
        self.minimum.setGeometry(350, 250, 100, 100)

        self.maximum = QLabel("Maximum ", self)
        self.maximum.setFont(QtGui.QFont('SansSerif', 10, QFont.Bold))
        self.maximum.setGeometry(450, 250, 100, 100)
        """

    def initMenu(self):
        # Create new action
        newAction = QAction(QIcon('new.png'), '&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        # newAction.triggered.connect(self.newCall)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open CSV File', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open document')
        openAction.triggered.connect(self.openFileNameDialog)

        # Create new action
        saveAsCSV_Action = QAction(QIcon('open.png'), '&Save as CSV', self)
        saveAsCSV_Action.setShortcut('Ctrl+O')
        saveAsCSV_Action.setStatusTip('Save document')
        saveAsCSV_Action.triggered.connect(self.saveFileDialog)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(app.quit)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAsCSV_Action)
        fileMenu.addAction(exitAction)

        self.show()

    def exit_program(self):
        app.quit()


    def message_click(self):
        if self.buttonReply == QMessageBox.Yes:
            print("Yeah")
        else:
            print("Nah")

    def startPlcAuto(self):
        try:
            plc_thread = Thread(target=serverOBJ.listenTCP)
            plc_thread.setDaemon(True)
            plc_thread.start()

        except Exception:
            traceback.print_exc()


    def startPlcManual(self):
        try:
            self.slider_roll.valueChanged.connect(self.loop)
            self.slider_pitch.valueChanged.connect(self.loop)
            self.slider_yaw.valueChanged.connect(self.loop)

        except Exception:
            traceback.print_exc()


    def loop(self):
        serverOBJ.manuel_plc(self.slider_roll.value(), self.slider_pitch.value(), self.slider_yaw.value())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()

    #ex.showFullScreen

    platformOBJ = StewartPlatform()
    serverOBJ = Server(platformOBJ, ex.widgetPlot.figureCanvas, ex.widgetHexapod)

    sys.exit(app.exec_())