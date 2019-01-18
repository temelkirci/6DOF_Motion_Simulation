import struct
import sys
from PyQt5.QtWidgets import *

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Motion Axes Data'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 600

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tableWidget = QTableWidget()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)

        self.setLayout(self.layout)

        self.openFileButton = QPushButton('Open File', self)
        self.openFileButton.setGeometry(870,100,100,50)
        self.openFileButton.clicked.connect(self.openFileNameDialog)

        # Show widget
        self.show()

    def createTable(self, file):
        f = open(file, mode="rb")
        myBytes = f.read()

        size = int(len(myBytes))  # float = 4 byte
        print("total file size : " + str(int((size)/1024)) + " KB")

        myfile = open("temelkirci.csv", "w")

        self.tableWidget.setRowCount(4000)
        self.tableWidget.setColumnCount(6)

        self.row = 0
        self.column = -1

        self.PreviousValue = 0.0

        for x in range(92, size, 4):
            if self.PreviousValue != 0.0:
                self.PreviousValue = float(str(struct.unpack("f", myBytes[x-4: x: 1])).replace("(" , "").replace(")", "").replace("," , ""))

            myCurrentValue = float(str(struct.unpack("f", myBytes[x: x + 4: 1])).replace("(", "").replace(")", "").replace(",", ""))

            if self.PreviousValue == 0.0 and myCurrentValue != 0.0:
                if self.column > 4:
                    break
                else :
                    self.column = self.column + 1
                    self.tableWidget.setItem(self.row, self.column, QTableWidgetItem(str(myCurrentValue)))
                    myfile.writelines( "Axes" + str(self.column) + "," + "\n\n" + str(myCurrentValue) + "," + "\n")
                    print("Axes" + str(self.column) + " : " + str(myCurrentValue))
                    self.row = 0
                    self.PreviousValue = myCurrentValue

            else:
                if myCurrentValue != 0.0:
                    self.tableWidget.setItem(self.row, self.column, QTableWidgetItem(str(myCurrentValue)))
                    myfile.writelines(str(myCurrentValue) + "," + "\n")
                    self.row = self.row + 1

        self.tableWidget.setGeometry(50, 50, 800, 500)

        self.tableWidget.setHorizontalHeaderLabels(['Axes-1', 'Axes-2', 'Axes-3', 'Axes-4', 'Axes-5', 'Axes-6'])

    def openFileNameDialog(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open .dat File", "",
                                              "All Files (*);;Data Files (*.dat)", options=options)
        if fileName:
            self.createTable(fileName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()


    sys.exit(app.exec_())
