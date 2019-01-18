from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import traceback
from matplotlib import style
from mpl_toolkits.mplot3d import  axes3d,Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import math

style.use('fivethirtyeight')
plt.style.use('ggplot')

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 14,
        }


class WidgetPlot(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.figureCanvas = PlotCanvas(self, width=13, height=8)
        self.toolbar = NavigationToolbar(self.figureCanvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.figureCanvas)


class Hexapod3D(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes3D = Axes3D(self.fig)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes3D.mouse_init(1 , 3)

        self.Base_between_Platform = 60
        self.Base_Scale = 1.0
        self.Platform_Scale = 1.0

        self.axes3D.set_xlim(-200, 200)
        self.axes3D.set_ylim(-200, 200)
        self.axes3D.set_zlim(0, 300)
        self.axes3D.set_xlabel('X')
        self.axes3D.set_ylabel('Y')
        self.axes3D.set_zlabel('Z')

        #timer = QTimer(self)
        #timer.timeout.connect(self.update_stewart_platform)
        #timer.start(100)

        self.update_stewart_platform(0,0,0)

        self.axes3D.view_init(elev=30, azim=90)


    def update_stewart_platform(self, roll, pitch, yaw):

        P1 = self.Platform_Scale * np.array([-86, -100, self.Base_between_Platform])
        P2 = self.Platform_Scale * np.array([86, -100, self.Base_between_Platform])
        P3 = self.Platform_Scale * np.array([130, -25, self.Base_between_Platform])
        P4 = self.Platform_Scale * np.array([43, 125, self.Base_between_Platform])
        P5 = self.Platform_Scale * np.array([-43, 125, self.Base_between_Platform])
        P6 = self.Platform_Scale * np.array([-130, -25, self.Base_between_Platform])

        P1 = np.dot(self.eulerAnglesToRotationMatrix(roll, pitch, yaw), P1)
        P2 = np.dot(self.eulerAnglesToRotationMatrix(roll, pitch, yaw), P2)
        P3 = np.dot(self.eulerAnglesToRotationMatrix(roll, pitch, yaw), P3)
        P4 = np.dot(self.eulerAnglesToRotationMatrix(roll, pitch, yaw), P4)
        P5 = np.dot(self.eulerAnglesToRotationMatrix(roll, pitch, yaw), P5)
        P6 = np.dot(self.eulerAnglesToRotationMatrix(roll, pitch, yaw), P6)


        B1 = self.Base_Scale * np.array([-43, -125, 0])
        B2 = self.Base_Scale * np.array([43, -125, 0])
        B3 = self.Base_Scale * np.array([130, 25, 0])
        B4 = self.Base_Scale * np.array([86, 100, 0])
        B5 = self.Base_Scale * np.array([-86, 100, 0])
        B6 = self.Base_Scale * np.array([-130, 25, 0])

        platform_vertice = np.array([P1, P2, P3, P4, P5, P6])
        base_vertice = np.array([B1, B2, B3, B4, B5, B6])

        #self.axes3D.scatter3D(platform_vertice[:, 0], platform_vertice[:, 1], platform_vertice[:, 2])

        platform = [ [platform_vertice[0], platform_vertice[1], platform_vertice[2], platform_vertice[3], platform_vertice[4], platform_vertice[5]] ]
        base = [ [base_vertice[0], base_vertice[1], base_vertice[2], base_vertice[3], base_vertice[4], base_vertice[5]] ]

        actuators = [
            [base_vertice[0], platform_vertice[0]],
            [base_vertice[1], platform_vertice[1]],
            [base_vertice[2], platform_vertice[2]],
            [base_vertice[3], platform_vertice[3]],
            [base_vertice[4], platform_vertice[4]],
            [base_vertice[5], platform_vertice[5]]
        ]

        self.axes3D.cla()

        self.axes3D.mouse_init(1, 3)
        self.axes3D.set_xlim(-200, 200)
        self.axes3D.set_ylim(-200, 200)
        self.axes3D.set_zlim(0, 300)
        self.axes3D.set_xlabel('X')
        self.axes3D.set_ylabel('Y')
        self.axes3D.set_zlabel('Z')

        self.axes3D.add_collection3d(Poly3DCollection(platform, facecolors='gray', linewidths=1, edgecolors='black'))
        self.axes3D.add_collection3d(Poly3DCollection(base, facecolors='gray', linewidths=1, edgecolors='black'))
        self.axes3D.add_collection3d(Line3DCollection(actuators, colors='black', linewidths=2, linestyles=':'))

        self.draw()




    def eulerAnglesToRotationMatrix(self, roll, pitch, yaw):
        try:
            roll = np.radians(roll)
            pitch = np.radians(pitch)
            yaw = np.radians(yaw)

            self.R_x = np.array([[1, 0, 0],
                                 [0, math.cos(roll), -math.sin(roll)],
                                 [0, math.sin(roll), math.cos(roll)]
                                 ])

            self.R_y = np.array([[math.cos(pitch), 0, math.sin(pitch)],
                                 [0, 1, 0],
                                 [-math.sin(pitch), 0, math.cos(pitch)]
                                 ])

            self.R_z = np.array([[math.cos(yaw), -math.sin(yaw), 0],
                                 [math.sin(yaw), math.cos(yaw), 0],
                                 [0, 0, 1]
                                 ])

            self.R = np.dot(self.R_z, np.dot(self.R_y, self.R_x))

            return self.R

        except Exception:
            traceback.print_exc()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=9, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes1 = fig.add_subplot(411)
        self.axes2 = fig.add_subplot(412)
        self.axes3 = fig.add_subplot(413)
        self.axes4 = fig.add_subplot(414)

        fig.subplots_adjust(hspace=1)

        self.axes1.set_ylabel("Roll", fontdict=font)
        self.axes2.set_ylabel("Pitch", fontdict=font)
        self.axes3.set_ylabel("Yaw", fontdict=font)
        self.axes4.set_ylabel("Actuators", fontdict=font)

        self.axes1.set_ylim([-20, 20])
        self.axes2.set_ylim([-20, 20])
        self.axes3.set_ylim([-20, 20])
        self.axes4.set_ylim([50, 150])

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.lx = self.axes4.axhline(color='k')  # the horiz line
        self.ly = self.axes4.axvline(color='k')  # the vert line

        size = 20
        time = np.linspace(0, 30, size + 1)[0:-1]

        self.roll_vec = np.zeros(size)
        self.pitch_vec = np.zeros(size)
        self.yaw_vec = np.zeros(size)

        self.hexapod1 = np.zeros(size)
        self.hexapod2 = np.zeros(size)
        self.hexapod3 = np.zeros(size)
        self.hexapod4 = np.zeros(size)
        self.hexapod5 = np.zeros(size)
        self.hexapod6 = np.zeros(size)

        self.line1, = self.axes1.plot(time, self.roll_vec, '-o', alpha=1)
        self.line2, = self.axes2.plot(time, self.pitch_vec, '-o', alpha=1)
        self.line3, = self.axes3.plot(time, self.yaw_vec, '-o', alpha=1)

        self.actuator1, = self.axes4.plot(time, self.hexapod1, '-o', alpha=1)
        self.actuator2, = self.axes4.plot(time, self.hexapod2, '-o', alpha=1)
        self.actuator3, = self.axes4.plot(time, self.hexapod3, '-o', alpha=1)
        self.actuator4, = self.axes4.plot(time, self.hexapod4, '-o', alpha=1)
        self.actuator5, = self.axes4.plot(time, self.hexapod5, '-o', alpha=1)
        self.actuator6, = self.axes4.plot(time, self.hexapod6, '-o', alpha=1)


    def onclick(self, event):
        print(event.button, event.x, event.y, event.xdata, event.ydata)


    def myPlot(self, roll, pitch, yaw, myActuators):
        try:
            self.roll_vec[-1] = roll
            self.line1.set_ydata(self.roll_vec)

            self.pitch_vec[-1] = pitch
            self.line2.set_ydata(self.pitch_vec)

            self.yaw_vec[-1] = yaw
            self.line3.set_ydata(self.yaw_vec)


            self.hexapod1[-1] = myActuators[0]
            self.actuator1.set_ydata(self.hexapod1)

            self.hexapod2[-1] = myActuators[1]
            self.actuator2.set_ydata(self.hexapod2)

            self.hexapod3[-1] = myActuators[2]
            self.actuator3.set_ydata(self.hexapod3)

            self.hexapod4[-1] = myActuators[3]
            self.actuator4.set_ydata(self.hexapod4)

            self.hexapod5[-1] = myActuators[4]
            self.actuator5.set_ydata(self.hexapod5)

            self.hexapod6[-1] = myActuators[5]
            self.actuator6.set_ydata(self.hexapod6)


            if np.min(self.roll_vec) <= self.line1.axes.get_ylim()[0] or np.max(self.roll_vec) >= self.line1.axes.get_ylim()[1]:
                plt.ylim([np.min(self.roll_vec) - np.std(self.roll_vec), np.max(self.roll_vec) + np.std(self.roll_vec)])

            if np.min(self.pitch_vec) <= self.line2.axes.get_ylim()[0] or np.max(self.pitch_vec) >= self.line2.axes.get_ylim()[1]:
                plt.ylim([np.min(self.pitch_vec) - np.std(self.pitch_vec), np.max(self.pitch_vec) + np.std(self.pitch_vec)])

            if np.min(self.yaw_vec) <= self.line3.axes.get_ylim()[0] or np.max(self.yaw_vec) >= self.line3.axes.get_ylim()[1]:
                plt.ylim([np.min(self.yaw_vec) - np.std(self.yaw_vec), np.max(self.yaw_vec) + np.std(self.yaw_vec)])


            self.roll_vec = np.append(self.roll_vec[1:], 0.0)
            self.pitch_vec = np.append(self.pitch_vec[1:], 0.0)
            self.yaw_vec = np.append(self.yaw_vec[1:], 0.0)

            self.hexapod1 = np.append(self.hexapod1[1:], 0.0)
            self.hexapod2 = np.append(self.hexapod2[1:], 0.0)
            self.hexapod3 = np.append(self.hexapod3[1:], 0.0)
            self.hexapod4 = np.append(self.hexapod4[1:], 0.0)
            self.hexapod5 = np.append(self.hexapod5[1:], 0.0)
            self.hexapod6 = np.append(self.hexapod6[1:], 0.0)

            self.draw()

        except Exception:
            traceback.print_exc()

