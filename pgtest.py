from PyQt5 import QtCore
from PyQt5 import QtWidgets
import pyqtgraph as pg

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pickle
import pymysql
import socket
import time
import requests
import getpass
from pymongo import MongoClient
# import os
# from DataClass import *
#
# path="H:/PATData"
# try:
#     files = os.listdir(path)
# except Exception as a:
#     print(a)
# # print(files)
# # 排除隐藏文件和文件夹
# dirList=[]
# filenames=[]
# for f in files:
#     if (os.path.isdir(path + '/' + f)):
#         # 排除隐藏文件夹。因为隐藏文件夹过多
#         if (f[0] == '.'):
#             pass
#         else:
#             # 添加非隐藏文件夹
#             dirList.append(f)
#     if (os.path.isfile(path + '/' + f)):
#         # 添加文件
#         if (os.path.splitext(f)[1] == ".txt"):
#             filenames.append(f)
# p = 1
# # print(self.filenames)
#
# for f in filenames:
#     data = dataclass()
#     data.filepath = path
#     datarow = open(path + '/' + f)  # 读取的整个原始文件数据
#     datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
#     datapar = []  # 真正的每行数据数组
#     temp = datarowlines[0].strip().split()
#     StartTime = datarowlines[2].strip()[11:-2]
#     print(temp)
#     for line in datarowlines[4:]:
#         linenew = line.strip().split()
#         print(linenew)
#         if (linenew != ""):
#             data1 = float(linenew[0])
#             data2 = float(linenew[1])
#             data3 = float(linenew[2])
#             x = float(linenew[3])
#             pass
#             datapar.append(linenew)


#
# import pyqtgraph as pg
# from pyqtgraph.Qt import QtCore, QtGui
#
# app = QtGui.QApplication([])
#
# view = pg.GraphicsView()
# layout = pg.GraphicsLayout()
# view.setCentralItem(layout)
#
# view.showMaximized()
#
# import sys
# if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#     QtGui.QApplication.instance().exec_()

#
# from PyQt5 import QtCore, QtGui, QtWidgets
#
#
# class Ui_StartForm(object):
#     def setupUi(self, StartForm):
#         StartForm.setObjectName("StartForm")
#         StartForm.resize(400, 300)
#         self.verticalLayout = QtWidgets.QVBoxLayout(StartForm)
#         self.verticalLayout.setObjectName("verticalLayout")
#         self.graphicsView = PlotWidget(StartForm)
#         self.graphicsView.setObjectName("graphicsView")
#         self.verticalLayout.addWidget(self.graphicsView)
#
#         self.retranslateUi(StartForm)
#         QtCore.QMetaObject.connectSlotsByName(StartForm)
#
#     def retranslateUi(self, StartForm):
#         _translate = QtCore.QCoreApplication.translate
#         StartForm.setWindowTitle(_translate("StartForm", "Form"))
#
# from pyqtgraph import PlotWidget
# from PyQt5 import QtWidgets
# # import StartForm
#
# class AppWindow(QtWidgets.QWidget, Ui_StartForm):
#     def __init__(self):
#         super(AppWindow, self).__init__()
#         self.setupUi(self)
#
#         line1 = ([1, 3, 2, 4, 6, 5, 3])
#         pl = self.graphicsView.plot(line1)
#
# if __name__ == '__main__':
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     w = AppWindow()
#     w.show()
#     sys.exit(app.exec_())


# obj1 = qtg.PlotWidget()
# # obj2 = qtg.PlotWidget()
# # obj3 = qtg.PlotWidget()
# #
# # layout = QGridLayout()
# #
# # layout.addWidget(obj1, 0, 0, 1, 2)
# # layout.addWidget(obj2, 0, 2, 1, 1)
# # layout.addWidget(obj3, 0, 3, 1, 1)
# # layout.setColumnStretch(0, 2)
# # layout.setColumnStretch(2, 1)
# # layout.setColumnStretch(3, 1)
# #
# # box = QGroupBox(self)
# # box.setLayout(layout)
# # self.setCentralWidget(box)

# w = pg.GraphicsLayoutWidget()
# p1 = w.addPlot(row=0, col=0)
# p2 = w.addPlot(row=0, col=1)
# print(min(0.5,0.4))
import numpy as np
from scipy.stats import kstest
from scipy.stats import anderson
import scipy
import random
walk = []
for _ in range(1000):
    walk.append(random.normalvariate(5, 1))
import matplotlib.pyplot as plt  # 导入模块

# plt.hist(walk, bins=30)  # bins直方图的柱数
# plt.show()
# print(walk)

# x = np.linspace(-15, 15, 9)
# kstest(walk, scipy.stats.norm.cdf, args=(5,1))
# print(kstest(walk, 'norm',args=(5,1)))
print(kstest(walk, 'poisson',args=(np.mean(walk),)))
# print(anderson(walk, 'norm'))