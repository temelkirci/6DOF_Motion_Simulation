#!/usr/bin/env python3
import csv
import numpy as np
import threading
import math
import traceback

class StewartPlatform(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.surge = 0
        self.sway = 0
        self.heave = 0

        self.roll_limit = 15
        self.pitch_limit = 15
        self.yaw_limit = 15

        self.L = 99
        self.D = 23
        self.l = 76
        self.d = 23

        self.minimumAxisValue = 100

        self.maximumAxisValue = 100

        self.L1_Actutator = 0.0

        self.L2_Actutator = 0.0

        self.L3_Actutator = 0.0

        self.L4_Actutator = 0.0

        self.L5_Actutator = 0.0

        self.L6_Actutator = 0.0

        self.actuator = [0, 0, 0, 0, 0, 0]

        """
        # 3x1 matrix
        self.A1 = np.array([[-86.0], [-100.0], [50.0]])
        # 3x1 matrix
        self.A2 = np.array([[86.0], [-100.0], [50.0]])
        # 3x1 matrix
        self.A3 = np.array([[130.0], [-25.0], [50.0]])
        # 3x1 matrix
        self.A4 = np.array([[43.0], [125.0], [50.0]])
        # 3x1 matrix
        self.A5 = np.array([[-43.0], [125.0], [50.0]])
        # 3x1 matrix
        self.A6 = np.array([[-130.0], [-25.0], [50.0]])
   
        # 3x1 matrix
        self.B1 = np.array([[-43], [-125], [0]])
        # 3x1 matrix
        self.B2 = np.array([[43], [-125], [0]])
        # 3x1 matrix
        self.B3 = np.array([[130], [25], [0]])
        # 3x1 matrix
        self.B4 = np.array([[86], [100], [0]])
        # 3x1 matrix
        self.B5 = np.array([[-86], [100],[0]])
        # 3x1 matrix
        self.B6 = np.array([[-130], [25], [0]])
        """

        # 3x1 matrix
        self.P = np.array([[0.0], [41.81], [0.0]])

        # 3x1 matrix
        self.A1 = np.array([[-79.86], [41.81], [16.20]])
        # 3x1 matrix
        self.A2 = np.array([[27.76], [41.81], [77.94]])
        # 3x1 matrix
        self.A3 = np.array([[53.63], [41.81], [62.87]])
        # 3x1 matrix
        self.A4 = np.array([[53.63], [41.81], [-61.20]])
        # 3x1 matrix
        self.A5 = np.array([[27.30], [41.81], [-76.07]])
        # 3x1 matrix
        self.A6 = np.array([[-79.86], [41.81], [-13.70]])

        # 3x1 matrix
        self.B1 = np.array([[-42.92], [0.0], [56.46]])
        # 3x1 matrix
        self.B2 = np.array([[-26.41], [0.0], [66.29]])
        # 3x1 matrix
        self.B3 = np.array([[70.45], [0.0], [10.87]])
        # 3x1 matrix
        self.B4 = np.array([[71.83], [0.0], [-10.0]])
        # 3x1 matrix
        self.B5 = np.array([[-26.41], [0.0], [-66.30]])
        # 3x1 matrix
        self.B6 = np.array([[-41.92], [0.0], [-56.46]])


        self.Base = []
        self.Base.append(self.B1)
        self.Base.append(self.B2)
        self.Base.append(self.B3)
        self.Base.append(self.B4)
        self.Base.append(self.B5)
        self.Base.append(self.B6)

        self.Platform = []
        self.Platform.append(self.A1)
        self.Platform.append(self.A2)
        self.Platform.append(self.A3)
        self.Platform.append(self.A4)
        self.Platform.append(self.A5)
        self.Platform.append(self.A6)

        # 1x6 matrix
        self.actuator_lengths = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        open('temel.csv', 'w').close()

    def inverse_kinematics(self, roll, pitch, yaw):
        try:
            np.clip(float(self.roll), -15.0, 15.0)
            np.clip(float(self.pitch), -15.0, 15.0)
            np.clip(float(self.yaw), -15.0, 15.0)

            for i in range(6):
                self.temp = np.subtract(np.add(self.P, np.dot(self.eulerAnglesToRotationMatrix(roll, pitch, yaw), self.Platform[i])),self.Base[i])
                self.actuator_lengths[i] = np.linalg.norm(self.temp)
                self.actuator[i] = int(self.actuator_lengths[i])

            #self.saveCSVData(self.actuator[0], self.actuator[1], self.actuator[2], self.actuator[3], self.actuator[4],self.actuator[5])

            return self.actuator

        except Exception:
            traceback.print_exc()


    def saveCSVData(self, a1,a2,a3,a4,a5,a6):
        try:
            with open('temel.csv', mode='a') as csvFile:
                writer = csv.writer(csvFile)
                row = [str(a1), str(a2), str(a3), str(a4), str(a5), str(a6)]
                writer.writerow(row)

        except Exception:
            traceback.print_exc()


    # Calculates Rotation Matrix given euler angles.
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


