import socket
import time
import traceback

import numpy as np
from threading import Thread

class Server(Thread):
    def __init__(self, stewartOBJ, myPlot, myHexa):
        Thread.__init__(self)

        # Can setup other things before the thread starts
        self.stewart_obj = stewartOBJ
        self.myDrawing = myPlot
        self.myHexapod = myHexa

        self.TCP_IP = "127.0.0.1"
        self.TCP_PORT = 2021

        self.elapsed = 0
        self.lastTime = 0

        try:
            # Create a TCP/IP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind the socket to the port
            self.server_address = (self.TCP_IP, self.TCP_PORT)
            print('started up on {} port {}'.format(*self.server_address))
            self.sock.bind(self.server_address)

            # Listen for incoming connections
            self.sock.listen(1)

        except Exception:
            traceback.print_exc()

        self.thread_active = True
        self.client_thread = True

        # PLC Connection
        self.PLC_IP = "192.168.1.20"
        self.PLC_PORT = 10001

        try:
            self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.clientsocket.connect((self.PLC_IP, self.PLC_PORT))
        except Exception:
            traceback.print_exc()


        #myResult = self.stewart_obj.inverse_kinematics(float(0.0), float(0.0), float(0.0))

        #self.myDrawing.myPlot(0.0, 0.0, 0.0 , myResult)


    def sendDataToPLC(self , myData):
        self.temel = str(myData[0]) + '~' + str(myData[1]) + '~' + str(myData[2]) + '~' + str(myData[3]) + '~' + str(myData[4]) + '~' + str(myData[5]) + '~' + str(0) + '~' + str(0) + '~' + str(0) + '~'
        #print(self.temel)
        try:
            #self.start = int(round(time.time() * 1000))

            self.clientsocket.send(str.encode(self.temel))

            self.finish = int(round(time.time() * 1000))

            self.elapsed = self.finish - self.lastTime
            self.lastTime = self.finish

            time.sleep(0.05) #50 ms

            #print(self.elapsed)

        except Exception:
            traceback.print_exc()

    def manuel_plc(self, manual_roll, manual_pitch, manual_yaw):
        myResult = self.stewart_obj.inverse_kinematics(float(manual_roll), float(manual_pitch), float(manual_yaw))

        self.myDrawing.myPlot(float(manual_roll), float(manual_pitch), float(manual_yaw), myResult)
        self.myHexapod.update_stewart_platform(float(manual_roll), float(manual_pitch), float(manual_yaw))

        self.sendDataToPLC(myResult)
        print(myResult)

    def listenTCP(self):
        while self.thread_active:
            # Wait for a connection
            print('waiting for a connection')
            self.connection, self.client_address = self.sock.accept()

            try:
                print('connection from', self.client_address)

                # Receive the data in small chunks and retransmit it
                while self.client_thread:
                    self.msg = self.connection.recv(1024)
                    self.data = str(self.msg)
                    #print(self.data)

                    if self.data:
                        self.startPitch = self.data.index("P")
                        self.pitch = self.data[self.startPitch + 2 : self.startPitch + 8]

                        self.startRoll = self.data.index("R")
                        self.roll = self.data[self.startRoll + 2 : self.startRoll + 8]

                        self.startYaw = self.data.index("Y")
                        self.yaw = self.data[self.startYaw + 2 : self.startYaw + 8]

                        myResult = self.stewart_obj.inverse_kinematics(float(self.roll), float(self.pitch),float(self.yaw))
                        self.sendDataToPLC ( myResult)
                        #self.connection.sendall(self.data)
                        self.myDrawing.myPlot(np.clip(float(self.roll), -15.0, 15.0),
                                              np.clip(float(self.pitch), -15.0, 15.0),
                                              np.clip(float(self.yaw), -15.0, 15.0) , myResult)
                    else:
                        print('no data from', self.client_address)
                        break

            except Exception:
                traceback.print_exc()
            finally:
                # Clean up the connection
                self.connection.close()