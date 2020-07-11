
from PyQt5.QtCore import *
import pickle
import os
import math
from DataClass import *
import numpy as np
from itertools import groupby
from scipy.optimize import curve_fit
class readfilethread(QThread):
    statusBarMessageStr = pyqtSignal(str)
    progressBarValueInt = pyqtSignal(int)
    progressBarVisualBool = pyqtSignal(bool)
    endinglist = pyqtSignal(str,dict,dict)
    # sinOutinlinebool = pyqtSignal(bool)
    # sinOutoutlinebool = pyqtSignal(bool)
    # sinOutinlinetext = pyqtSignal(str)
    # sinOutoutlinetext = pyqtSignal(str)
    # sinOutoutpath = pyqtSignal(str)
    # sinOutoutData = pyqtSignal(dataclass)
    def __init__(self,path,groupnum=150):
        self.data=""
        self.groupnum=groupnum
        self.path=path
        self.filenames=[]
        self.datalist=dict()
        self.settinglist=dict()
        self.dRatio=180/math.pi
        super(readfilethread,self).__init__()

    def getIndexes(y_predict, y_data):
        y_predict = np.array(y_predict)
        y_data = np.array(y_data)
        n = y_data.size
        # SSE为和方差
        SSE = ((y_data - y_predict) ** 2).sum()
        # MSE为均方差
        MSE = SSE / n
        # RMSE为均方根,越接近0，拟合效果越好
        RMSE = np.sqrt(MSE)

        # 求R方，0<=R<=1，越靠近1,拟合效果越好
        u = y_data.mean()
        SST = ((y_data - u) ** 2).sum()
        SSR = SST - SSE
        R_square = SSR / SST
        return [R_square, SSE, MSE, RMSE]

    def formatTime(self,allTime):
        day = 24 * 60 * 60
        hour = 60 * 60
        min = 60

        if allTime < 60:
            return "%d 秒" % math.ceil(allTime)
        elif allTime > day:
            days = divmod(allTime, day)
            return "%d 天, %s" % (int(days[0]), self.formatTime(days[1]))
        elif allTime > hour:
            hours = divmod(allTime, hour)
            return '%d 小时, %s' % (int(hours[0]), self.formatTime(hours[1]))
        else:
            mins = divmod(allTime, min)
            return "%d 分, %d 秒" % (int(mins[0]), math.ceil(mins[1]))

    def readfile_noache(self,path,filelist):
        p = 1
        errornum=0
        # print(self.filenames)
        for f in filelist:
            self.statusBarMessageStr.emit("正在读取 " + str(p) + "/" + str(len(filelist)) + " " + f)
            data = dataclass()
            data.path = path
            name, _ = os.path.splitext(f)
            data.name=name
            data.filename=f

            datarow = open(path + '/' + f)  # 读取的整个原始文件数据
            datarowlines = datarow.readlines()  # 读取的整个原始文件的数据，按行分割
            datapar = []  # 真正的每行数据数组
            data.Total=int(datarowlines[0].strip().split()[1])
            if data.Total==0:
                errornum+=1
                continue
            data.StartTime=datarowlines[2].strip()[11:-2]
            duringtime_temp=0
            for line in datarowlines[4:]:
                linenew = line.strip().split()
                # print(linenew)
                if (len(linenew)!= 0):
                    in1=float(linenew[0])
                    in2=float(linenew[1])
                    data.in1.append(in1)
                    data.in2.append(in2)
                    if in2 ==0:
                        data.in1_2.append(0.0)
                    else:
                        data.in1_2.append(float(linenew[0])/float(linenew[1]))

                    if in1 ==0:
                        data.in2_1.append(0.0)
                    else:
                        data.in2_1.append(float(linenew[1])/float(linenew[0]))

                    data.out.append(float(linenew[2]))
                    dTotal = float(linenew[0]+linenew[1])
                    if (dTotal < 0.1):
                        data.dAngle.append(0.0)
                    else:
                        data.dAngle.append(self.dRatio * math.asin(math.sqrt(float(linenew[0])/ dTotal)) - 45.0)
                    data.x.append(float(linenew[3]))
                    data.duringtime.append(float(linenew[3])-duringtime_temp)
                    data.in1_partime.append(int(float(linenew[0])/(float(linenew[3])-duringtime_temp)))
                    data.in2_partime.append(int(float(linenew[1])/(float(linenew[3])-duringtime_temp)))
                    duringtime_temp=float(linenew[3])
            mean_in1=(np.sum(data.in1)/data.x[-1])
            mean_in2=(np.sum(data.in2)/data.x[-1])
            temp0=[data ** 2 for data in data.in1_partime]
            temp1=np.mean(temp0)
            data.in1_Q=(temp1-mean_in1**2)/mean_in1-1
            data.in2_Q=(np.mean([ data**2 for data in data.in2_partime ])-mean_in2**2)/mean_in2-1
            data.index1=0
            data.index2=len(data.x)-1
            data.duration = self.formatTime(data.x[-1]/1000)
            data.in1_mean=int(np.mean(data.in1)+0.5)
            data.in2_mean=int(np.mean(data.in2)+0.5)
            data.in1_variance=np.var(data.in1)
            data.in2_variance=np.var(data.in2)
            if data.Total>=self.groupnum*4:
                for i in range(0, len(data.in1), self.groupnum):
                    if i+self.groupnum<=len(data.in1):
                        data.in1_probability_dis_x.append(data.x[i])
                        data.in2_probability_dis_x.append(data.x[i])
                        data.in1_probability_dis.append(int(np.mean(data.in1[i:i + self.groupnum])+0.5))
                        data.in2_probability_dis.append(int(np.mean(data.in2[i:i + self.groupnum])+0.5))
                data.in1_group_mean=int(np.mean(data.in1_probability_dis)+0.5)
                data.in2_group_mean=int(np.mean(data.in2_probability_dis)+0.5)
                data.in1_group_variance=np.var(data.in1_probability_dis)
                data.in2_group_variance=np.var(data.in2_probability_dis)
            # inter=int(len(data.in1)/10)
            # for k, g in groupby(sorted(data.in1), key=lambda x: x // inter):
            #     print('{}-{}: {}'.format(k * inter, (k + 1) * inter - 1, len(list(g))))
            # inter=int(len(data.in1_probability_dis)/10)
            # for k, g in groupby(sorted(data.in1_probability_dis), key=lambda x: x // inter):
            #     print('{}-{}: {}'.format(k * inter, (k + 1) * inter - 1, len(list(g))))
            # def func(x, a, b):
            #     return data.in1_mean**x/factorial(x)
            # popt, pcov = curve_fit(func, x, y)
            tempsetting=settingclass()
            tempsetting.x2=len(data.x)-1
            tempsetting.path=path
            self.datalist[data.name]=data
            self.settinglist[data.name]=tempsetting
            self.progressBarValueInt.emit(int(p/len(filelist)*100))
            p+=1
        return errornum

    def saveache(self):
        self.statusBarMessageStr.emit("正在保存当前状态...")
        achefilename = self.path + "/" + os.path.basename(self.path) + ".data"
        settingfilename = self.path + "/" + os.path.basename(self.path) + "_setting.data"
        try:
            with open(achefilename, "wb") as file:
                pickle.dump(self.datalist, file, True)
            print("saveache",self.settinglist)
            with open(settingfilename, "wb") as file:
                pickle.dump(self.settinglist, file, True)
            # with open(achefilename, "rb") as file:
            #     data1 = pickle.load(file)
            # print(data1)
        except Exception as a:
            self.statusBarMessageStr.emit(str(a))

    def returndata(self):
        print(self.settinglist)
        self.endinglist.emit(self.path, self.datalist,self.settinglist)
        self.progressBarVisualBool.emit(False)
        errornum=len(self.filenames)-len(self.datalist)
        if errornum == 0:
            self.statusBarMessageStr.emit("读取完成！（已添加" + str(len(self.filenames)) + "个数据文件）")
        else:
            self.statusBarMessageStr.emit(
                "读取完成！（已添加" + str(len(self.datalist)) + "个数据文件,忽略" + str(errornum) + "个无效文件）")


    def run(self):
        self.progressBarValueInt.emit(0)
        self.progressBarVisualBool.emit(True)
        self.dRati = 180.0 / math.pi

        # 遍历目录
        try:
            files = os.listdir(self.path)
        except Exception as a:
            print(a)
            self.progressBarVisualBool.emit(False)
        # print(files)
        # 排除隐藏文件和文件夹
        self.dirList=[]
        for f in files:
            if (os.path.isdir(self.path + '/' + f)):
                # 排除隐藏文件夹。因为隐藏文件夹过多
                if (f[0] == '.'):
                    pass
                else:
                    # 添加非隐藏文件夹
                    self.dirList.append(f)
            if (os.path.isfile(self.path + '/' + f)):
                # 添加文件
                if (os.path.splitext(f)[1] == ".txt"):
                    self.filenames.append(f)

        achepath=self.path + "/" + os.path.basename(self.path) + ".data"
        settingpath=self.path + "/" + os.path.basename(self.path) + "_setting.data"
        if os.path.exists(achepath) and os.path.exists(settingpath):
            self.statusBarMessageStr.emit("正在从缓存中读取数据...")
            try:
                with open(achepath, "rb") as file:
                    self.datalist = pickle.load(file)
                with open(settingpath, "rb") as file:
                    self.settinglist = pickle.load(file)
                print(self.settinglist)
                pass
            except Exception as a:
                self.errorunm=self.readfile_noache(self.path,self.filenames)
                self.saveache()
                self.returndata()
            print(self.settinglist)
            self.returndata()
        else:
            # 读文件
            self.errorunm=self.readfile_noache(self.path,self.filenames)
            self.saveache()
            self.returndata()

class getcutdatathread(QThread):
    statusBarMessageStr = pyqtSignal(str)
    progressBarValueInt = pyqtSignal(int)
    progressBarVisualBool = pyqtSignal(bool)
    endingmulti = pyqtSignal(object,int,int)
    def __init__(self,data:dataclass,x1:int,x2:int):
        self.data=data
        self.x1=min(x1,x2)
        self.x2=max(x1,x2)
        super(getcutdatathread,self).__init__()
    def run(self):
        print(self.x1,self.x2)
        x1index=0
        x2index=len(self.data.x)-1
        for i in range(len(self.data.x)):
            if self.data.x[i]>=self.x1:
                x1index=i
                for j in range(i,len(self.data.x)):
                    if  self.data.x[j]>self.x2:
                        x2index=j-1
                        break
                break
        # print(x1index,x2index)
        self.data.index1=x1index
        self.data.index2=x2index
        self.endingmulti.emit(self.data,x1index,x2index)


class savesettingthread(QThread):
    statusBarMessageStr = pyqtSignal(str)
    progressBarValueInt = pyqtSignal(int)
    progressBarVisualBool = pyqtSignal(bool)
    endingmulti = pyqtSignal()
    def __init__(self,path,setting):
        self.path=path
        self.setting=setting
        super(savesettingthread,self).__init__()
    def run(self):
        self.statusBarMessageStr.emit("正在保存设置...")
        settingpath=self.path + "/" + os.path.basename(self.path) + "_setting.data"
        settingloacalpath=os.getcwd() + "/setting/" + os.path.basename(self.path) + "_setting.data"
        try:
            with open(settingpath, "wb") as file:
                pickle.dump(self.setting, file, True)
            # with open(achefilename, "rb") as file:
            #     data1 = pickle.load(file)
            # print(data1)
            with open(settingloacalpath, "wb") as file:
                pickle.dump(self.setting, file, True)
        except Exception as a:
            self.statusBarMessageStr.emit(str(a))
        self.statusBarMessageStr.emit("设置已保存！")
        self.endingmulti.emit()

class savelocalpathachethread(QThread):
    statusBarMessageStr = pyqtSignal(str)
    endingmulti = pyqtSignal()
    def __init__(self,path:str,datalist:dict,settinglist:dict):
        self.path=path
        self.datalist=datalist
        self.settinglist=settinglist
        super(savelocalpathachethread,self).__init__()
    def run(self):
        self.statusBarMessageStr.emit("正在保存数据...")
        self.dataname = os.path.basename(self.path)
        datapath=os.getcwd() + "/ache/" + self.dataname + ".data"
        settingpath=os.getcwd() + "/setting/" + self.dataname + "_setting.data"
        if not os.path.exists(os.getcwd() + "/ache/"):
            os.mkdir(os.getcwd() + "/ache/")
        if not os.path.exists(os.getcwd() + "/setting/"):
            os.mkdir(os.getcwd() + "/setting/")
        try:
            with open(datapath, "wb") as file:
                pickle.dump(self.datalist, file, True)
            with open(settingpath, "wb") as file:
                pickle.dump(self.settinglist, file, True)
        except Exception as a:
            self.statusBarMessageStr.emit(str(a))
        print("已保存：",self.dataname)
        # self.statusBarMessageStr.emit("数据已保存！")
        # self.endingmulti.emit()