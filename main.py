import sys

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Thread import *
import pyqtgraph as pg
from MyWidget import *

class dragLineEdit(QLineEdit):
    def __init__(self, statusBar):
        super(dragLineEdit, self).__init__()
        self.statusBar = statusBar

    def dragEnterEvent(self, evn):
        evn.accept()

    def dropEvent(self, evn):
        filename = evn.mimeData().text().split("///")[1]
        print(filename)
        if (os.path.isdir(filename)):
            self.setText(filename)
        else:
            self.statusBar().showMessage("文件无效，请选择文件目录！")

    def dragMoveEvent(self, evn):
        self.statusBar().showMessage("正在进行拖入操作...")





class main(QMainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        self.setWindowTitle('旋光数据处理工具')
        self.setWindowIcon(QIcon('xyjk.png'))
        self.setFont(QFont("Microsoft YaHei", 12))
        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)
        self.statusBar().addPermanentWidget(self.progressBar)
        self.setAcceptDrops(True)
        self.resize(500, 600)
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.folderlist=dict()
        self.foldersettinglist=dict()
        self.datalist=dict()
        self.datasettinglist=dict()
        self.data = None
        self.setting = None
        self.currentpath=""
        self.grid = QGridLayout(self)

        # 文件读取
        self.inLineEdit = dragLineEdit(self.statusBar)
        self.inLineEdit.setPlaceholderText('可拖拽数据文件夹至此')
        self.inLineEdit.setReadOnly(True)
        self.inLineEdit.returnPressed.connect(lambda: self.inLineEditfinished())
        self.inLineEdit.textChanged.connect(lambda: self.inLineEditfinished())
        self.grid.addWidget(self.inLineEdit, 0, 0, 1, 3)

        self.readfileButton = QPushButton("添加文件夹")
        self.grid.addWidget(self.readfileButton, 0, 3, 1, 1)
        self.readfileButton.clicked.connect(self.selectfile)

        self.FolderTable = QListWidget()
        self.FolderTable.setFont(QFont("Microsoft YaHei", 12))
        self.FolderTable.clicked.connect(self.FolderTableclicked)
        self.grid.addWidget(self.FolderTable, 1, 0, 1, 2)


        self.showsettinggrid=QGridLayout()
        self.pw1showgroup = QGroupBox('预览图1')
        self.pw1showGrid = QGridLayout()
        self.pw1showcheckbox1 = QCheckBox("IN1")
        self.pw1showcheckbox2 = QCheckBox("IN2")
        self.pw1showcheckbox3 = QCheckBox("OUT")
        self.pw1showcheckbox4 = QCheckBox("IN1/IN2")
        self.pw1showcheckbox5 = QCheckBox("IN2/IN1")
        self.pw1showcheckbox6 = QCheckBox("dAngle")
        self.pw1showcheckbox1.stateChanged.connect(self.pw1showcheckbox1stateChanged)
        self.pw1showcheckbox2.stateChanged.connect(self.pw1showcheckbox2stateChanged)
        self.pw1showcheckbox3.stateChanged.connect(self.pw1showcheckbox3stateChanged)
        self.pw1showcheckbox4.stateChanged.connect(self.pw1showcheckbox4stateChanged)
        self.pw1showcheckbox5.stateChanged.connect(self.pw1showcheckbox5stateChanged)
        self.pw1showcheckbox6.stateChanged.connect(self.pw1showcheckbox6stateChanged)
        self.pw1showcheckbox1.setChecked(True)
        self.pw1showcheckbox2.setChecked(True)
        self.pw1showcheckbox3.setChecked(True)
        self.pw1showcheckbox4.setChecked(True)
        self.pw1showcheckbox5.setChecked(True)
        self.pw1showcheckbox6.setChecked(True)
        self.pw1showGrid.addWidget(self.pw1showcheckbox1, 0, 0, 1, 1)
        self.pw1showGrid.addWidget(self.pw1showcheckbox2, 0, 1, 1, 1)
        self.pw1showGrid.addWidget(self.pw1showcheckbox3, 0, 2, 1, 1)
        self.pw1showGrid.addWidget(self.pw1showcheckbox4, 0, 3, 1, 1)
        self.pw1showGrid.addWidget(self.pw1showcheckbox5, 0, 4, 1, 1)
        self.pw1showGrid.addWidget(self.pw1showcheckbox6, 0, 5, 1, 1)
        self.pw1showgroup.setLayout(self.pw1showGrid)
        # self.pw1showButtonGroup.buttonClicked[int].connect(self.showpicture)
        self.showsettinggrid.addWidget(self.pw1showgroup,0,0,1,1)

        self.pw2showgroup = QGroupBox('预览图2')
        self.pw2showGrid = QGridLayout()
        self.pw2showcheckbox1 = QCheckBox("IN1")
        self.pw2showcheckbox2 = QCheckBox("IN2")
        self.pw2showcheckbox3 = QCheckBox("OUT")
        self.pw2showcheckbox4 = QCheckBox("IN1/IN2")
        self.pw2showcheckbox5 = QCheckBox("IN2/IN1")
        self.pw2showcheckbox6 = QCheckBox("dAngle")
        self.pw2showcheckbox1.stateChanged.connect(self.pw2showcheckbox1stateChanged)
        self.pw2showcheckbox2.stateChanged.connect(self.pw2showcheckbox2stateChanged)
        self.pw2showcheckbox3.stateChanged.connect(self.pw2showcheckbox3stateChanged)
        self.pw2showcheckbox4.stateChanged.connect(self.pw2showcheckbox4stateChanged)
        self.pw2showcheckbox5.stateChanged.connect(self.pw2showcheckbox5stateChanged)
        self.pw2showcheckbox6.stateChanged.connect(self.pw2showcheckbox6stateChanged)
        self.pw2showcheckbox1.setChecked(True)
        self.pw2showcheckbox2.setChecked(True)
        self.pw2showcheckbox3.setChecked(True)
        self.pw2showcheckbox4.setChecked(True)
        self.pw2showcheckbox5.setChecked(True)
        self.pw2showcheckbox6.setChecked(True)
        self.pw2showGrid.addWidget(self.pw2showcheckbox1, 0, 0, 1, 1)
        self.pw2showGrid.addWidget(self.pw2showcheckbox2, 0, 1, 1, 1)
        self.pw2showGrid.addWidget(self.pw2showcheckbox3, 0, 2, 1, 1)
        self.pw2showGrid.addWidget(self.pw2showcheckbox4, 0, 3, 1, 1)
        self.pw2showGrid.addWidget(self.pw2showcheckbox5, 0, 4, 1, 1)
        self.pw2showGrid.addWidget(self.pw2showcheckbox6, 0, 5, 1, 1)
        self.pw2showgroup.setLayout(self.pw2showGrid)
        # self.pw2showButtonGroup.buttonClicked[int].connect(self.showpicture)
        self.showsettinggrid.addWidget(self.pw2showgroup, 1, 0, 1, 1)

        self.pw3showgroup = QGroupBox('预览图3')
        self.pw3showGrid = QGridLayout()
        self.pw3showcheckbox1 = QCheckBox("IN1")
        self.pw3showcheckbox2 = QCheckBox("IN2")
        self.pw3showcheckbox3 = QCheckBox("OUT")
        self.pw3showcheckbox4 = QCheckBox("IN1/IN2")
        self.pw3showcheckbox5 = QCheckBox("IN2/IN1")
        self.pw3showcheckbox6 = QCheckBox("dAngle")
        self.pw3showcheckbox1.stateChanged.connect(self.pw3showcheckbox1stateChanged)
        self.pw3showcheckbox2.stateChanged.connect(self.pw3showcheckbox2stateChanged)
        self.pw3showcheckbox3.stateChanged.connect(self.pw3showcheckbox3stateChanged)
        self.pw3showcheckbox4.stateChanged.connect(self.pw3showcheckbox4stateChanged)
        self.pw3showcheckbox5.stateChanged.connect(self.pw3showcheckbox5stateChanged)
        self.pw3showcheckbox6.stateChanged.connect(self.pw3showcheckbox6stateChanged)
        self.pw3showcheckbox1.setChecked(True)
        self.pw3showcheckbox2.setChecked(True)
        self.pw3showcheckbox3.setChecked(True)
        self.pw3showcheckbox4.setChecked(True)
        self.pw3showcheckbox5.setChecked(True)
        self.pw3showcheckbox6.setChecked(True)
        self.pw3showGrid.addWidget(self.pw3showcheckbox1, 0, 0, 1, 1)
        self.pw3showGrid.addWidget(self.pw3showcheckbox2, 0, 1, 1, 1)
        self.pw3showGrid.addWidget(self.pw3showcheckbox3, 0, 2, 1, 1)
        self.pw3showGrid.addWidget(self.pw3showcheckbox4, 0, 3, 1, 1)
        self.pw3showGrid.addWidget(self.pw3showcheckbox5, 0, 4, 1, 1)
        self.pw3showGrid.addWidget(self.pw3showcheckbox6, 0, 5, 1, 1)
        self.pw3showgroup.setLayout(self.pw3showGrid)
        # self.pw3showButtonGroup.buttonClicked[int].connect(self.showpicture)
        self.showsettinggrid.addWidget(self.pw3showgroup, 2, 0, 1, 1)

        self.FullScreengroup = QGroupBox('全屏预览')
        self.FullScreenGrid = QGridLayout()
        self.pw1FullScreen=QPushButton("图1全屏")
        self.FullScreenGrid.addWidget(self.pw1FullScreen,0,0,1,1)
        self.pw2FullScreen=QPushButton("图2全屏")
        self.FullScreenGrid.addWidget(self.pw2FullScreen,0,1,1,1)
        self.pw3FullScreen=QPushButton("图3全屏")
        self.pw3FullScreen.clicked.connect(self.pw3FullScreenclicked)
        self.FullScreenGrid.addWidget(self.pw3FullScreen,0,2,1,1)
        self.FullScreengroup.setLayout(self.FullScreenGrid)
        self.showsettinggrid.addWidget(self.FullScreengroup, 3, 0, 1, 1)

        self.showsettingwidget=QWidget()
        self.showsettingwidget.setLayout(self.showsettinggrid)


        self.imagelabel=Mydemo()

        self.tab = QTabWidget()
        self.tab.setFont(QFont("Microsoft YaHei", 12))
        self.tab1 = self.tab.addTab(self.showsettingwidget, "数据分析")
        self.tab2 = self.tab.addTab(self.imagelabel, "概率分布")
        self.grid.addWidget(self.showsettingwidget, 1, 2, 1, 2)

        # # 单选
        # self.pw3showgroup = QGroupBox('预览图2')
        # self.pw3showGrid = QGridLayout()
        # self.pw3showRadioButton1 = QRadioButton("IN1")
        # self.pw3showRadioButton2 = QRadioButton("IN2")
        # self.pw3showRadioButton3 = QRadioButton("OUT")
        # self.pw3showRadioButton1.setChecked(True)
        # self.pw3showRadioButton2.setChecked(True)
        # self.pw3showRadioButton3.setChecked(True)
        # self.pw3showGrid.addWidget(self.pw3showRadioButton1, 0, 0, 1, 1)
        # self.pw3showGrid.addWidget(self.pw3showRadioButton2, 0, 1, 1, 1)
        # self.pw3showGrid.addWidget(self.pw3showRadioButton3, 0, 2, 1, 1)
        # self.pw3showgroup.setLayout(self.pw3showGrid)
        # self.pw3showButtonGroup = QButtonGroup()
        # self.pw3showButtonGroup.addButton(self.pw3showRadioButton1)
        # self.pw3showButtonGroup.addButton(self.pw3showRadioButton2)
        # self.pw3showButtonGroup.addButton(self.pw3showRadioButton3)
        # self.pw3showButtonGroup.setId(self.pw3showRadioButton1, 1)  # 设定ID
        # self.pw3showButtonGroup.setId(self.pw3showRadioButton2, 2)  # 设定ID
        # self.pw3showButtonGroup.setId(self.pw3showRadioButton3, 3)  # 设定ID
        # # self.pw3showButtonGroup.buttonClicked[int].connect(self.showpicture)
        # self.showsettinggrid.addWidget(self.pw3showgroup, 1, 0, 1, 1)
        # self.showsettingwidget=QWidget()
        # self.showsettingwidget.setLayout(self.showsettinggrid)
        # self.grid.addWidget(self.showsettingwidget, 1, 2, 1, 2)



        

        self.filelistTable = QTableWidget()
        self.filelistTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.filelistTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.filelistTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.filelistTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.filelistTable.setFont(QFont("Microsoft YaHei", 12))
        self.filelistTable.setColumnCount(12)
        self.filelistTable.setHorizontalHeaderLabels(["文件名","创建时间","测试时长","总数据量","IN1均值","IN1方差","IN2均值","IN2方差","IN1聚合均值","IN1聚合方差","IN2聚合均值","IN2聚合方差"])
        # self.filelistTable.setHorizontalHeaderLabels(["显示","文件名","创建时间","测试时长","总数据量"])
        self.filelistTable.clicked.connect(self.filelistTableclicked)
        self.grid.addWidget(self.filelistTable, 2, 0, 3, 4)
        self.Graphgrid = pg.GraphicsLayoutWidget()

        pen1=pg.mkPen(color=(255, 0, 0))
        pen2=pg.mkPen(color=( 0,255, 0))
        pen3=pg.mkPen(color=(0, 0,255))
        pen4=pg.mkPen(color=(139,28,98))
        pen5=pg.mkPen(color=(255,246,143))
        pen6=pg.mkPen(color=(255,140,0))


        # 图像1
        # self.pw1 = pg.PlotWidget()  # 实例化一个绘图部件
        self.pw1 = self.Graphgrid.addPlot(row=0, col=0,rowspan = 1,colspan = 1)
        self.pw1.addLegend()
        # self.pw1 = self.Graphgrid.addViewBox(row=0, col=0)
        self.pw1.showGrid(x=True, y=True)
        # self.pw1.plot(self.data)
        # self.grid.addWidget(self.pw1,1,1,1,2)
        self.pw1dataline1=self.pw1.plot(pen=pen1,name='IN1')
        self.pw1dataline2=self.pw1.plot(pen=pen2,name='IN2')
        self.pw1dataline3=self.pw1.plot(pen=pen3,name='OUT')
        self.pw1dataline4=self.pw1.plot(pen=pen4,name='IN1/IN2')
        self.pw1dataline5=self.pw1.plot(pen=pen5,name='IN2/IN1')
        self.pw1dataline6=self.pw1.plot(pen=pen6,name='dAngle')

        # 图像2
        # self.pw2 = pg.PlotWidget()  # 实例化一个绘图部件
        self.pw2 = self.Graphgrid.addPlot(row=0, col=1,rowspan = 1,colspan = 1)
        self.pw2.addLegend()
        # self.pw2 = self.Graphgrid.addViewBox(row=1, col=0)
        self.pw2.showGrid(x=True, y=True)
        # self.grid.addWidget(self.pw2,2,1,1,2)
        self.pw2Line1 = pg.InfiniteLine(pos=QPointF(5.0, 5.0), angle=90, movable=True)
        self.pw2Line1.sigPositionChangeFinished.connect(self.pw2LinePositionChangeFinished)
        self.pw2Line2 = pg.InfiniteLine(pos=QPointF(10.0, 5.0), angle=90, movable=True)
        self.pw2Line2.sigPositionChangeFinished.connect(self.pw2LinePositionChangeFinished)
        self.pw2.addItem(self.pw2Line1, ignoreBounds=True)
        # self.pw2.addItem(self.pw2Line2, ignoreBounds=True)
        self.pw2.addItem(self.pw2Line2, ignoreBounds=True)
        self.pw2dataline1=self.pw2.plot(pen=pen1,name='IN1')
        self.pw2dataline2=self.pw2.plot(pen=pen2,name='IN2')
        self.pw2dataline3=self.pw2.plot(pen=pen3,name='out')
        self.pw2dataline4=self.pw2.plot(pen=pen4,name='IN1/IN2')
        self.pw2dataline5=self.pw2.plot(pen=pen5,name='IN2/IN1')
        self.pw2dataline6=self.pw2.plot(pen=pen6,name='dAngle')

        # self.pw3.plot(self.data)

        # 图像3
        # self.pw3 = pg.PlotWidget()  # 实例化一个绘图部件
        self.pw3 = self.Graphgrid.addPlot(row=1, col=0,rowspan = 2,colspan = 2)
        # self.pw3.scene().licked.connect(lambda:print("dddddddd****************"))
        print(type(self.pw3))
        # self.pw3.mouse_clicked.connect(lambda: print("dsfdsfsdfsdfdsfdsfsd"))
        self.pw3.addLegend()
        # self.pw3.enableAutoRange(axis='y')
        # self.pw3.setAutoVisible(y=True)
        # # self.pw3 = self.Graphgrid.addViewBox(row=2, col=0)
        self.pw3.showGrid(x=True, y=True)
        self.pw3dataline1 = self.pw3.plot(pen=pen1,name='IN2')
        self.pw3dataline2 = self.pw3.plot(pen=pen2,name='IN1')
        self.pw3dataline3 = self.pw3.plot(pen=pen3,name='out')
        self.pw3dataline4 = self.pw3.plot(pen=pen4,name='IN1/IN2')
        self.pw3dataline5 = self.pw3.plot(pen=pen5,name='IN2/IN1')
        self.pw3dataline6 = self.pw3.plot(pen=pen6,name='dAngle')
        self.pw3dataline6.curve.setClickable(True)
        # self.grid.addWidget(self.pw3,3,1,2,2)
        # self.Graphgrid.setRowStretch(0, 1)
        # self.Graphgrid.setRowStretch(1, 1)
        # self.Graphgrid.setRowStretch(2, 2)
        self.grid.addWidget(self.Graphgrid,0,4,5,8)

        # 全屏控件
        self.pw1fc = pg.PlotWidget()
        self.pw1fcexitbutton=QPushButton("退出全屏")
        self.pw1fcexitbutton.clicked.connect(self.pwfcexitbuttonclicked)
        self.pw2fc = pg.PlotWidget()
        self.pw2fcexitbutton = QPushButton("退出全屏")
        self.pw2fcexitbutton.clicked.connect(self.pwfcexitbuttonclicked)
        self.pw3fc = pg.PlotWidget()
        self.pw3fcexitbutton = QPushButton("退出全屏")
        self.pw3fcexitbutton.clicked.connect(self.pwfcexitbuttonclicked)
        self.pw1fc.addLegend()
        self.pw2fc.addLegend()
        self.pw3fc.addLegend()

        # 全屏控件3
        self.pw3fcdataline1 = self.pw3fc.plot(pen=pen1, name='IN2')
        self.pw3fcdataline2 = self.pw3fc.plot(pen=pen2, name='IN1')
        self.pw3fcdataline3 = self.pw3fc.plot(pen=pen3, name='out')
        self.pw3fcdataline4 = self.pw3fc.plot(pen=pen4, name='IN1/IN2')
        self.pw3fcdataline5 = self.pw3fc.plot(pen=pen5, name='IN2/IN1')
        self.pw3fcdataline6 = self.pw3fc.plot(pen=pen6, name='dAngle')


        # self.grid.setRowStretch(3, 2)
        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 1)
        self.grid.setRowStretch(2, 2)
        # self.grid.setColumnStretch(0, 1)
        # self.grid.setColumnStretch(1, 2)
        # self.grid.setColumnStretch(2, 1)
        self.widget=QWidget()
        self.widget.setLayout(self.grid)
        # self.setCentralWidget(self.widget)
        self.stackedWidget.addWidget(self.widget)

        self.pw3FullScreenwidget=QWidget()
        self.pw3FullScreengrid=QGridLayout()
        self.pw3FullScreengrid.addWidget(self.pw3fc,0,0,1,1)
        self.pw3FullScreengrid.addWidget(self.pw3fcexitbutton,1,0,1,1)
        self.pw3FullScreenwidget.setLayout(self.pw3FullScreengrid)
        self.stackedWidget.addWidget(self.pw3FullScreenwidget)

        self.loadache()
        # self.pw3.plot(data, )  # 在绘图部件中绘制折线图



    def loadache(self):
        if not (os.path.exists(os.getcwd() + "/ache/")and os.path.exists(os.getcwd() + "/setting/")):
            return

        datas = os.listdir(os.getcwd() + "/ache/")
        settings = os.listdir(os.getcwd() + "/setting/")
        if len(datas)==0 or len(settings)==0:
            return
        folderlist=dict()
        foldersettinglist=dict()
        for f in settings:
            settingpath=os.getcwd()+"/setting/"+f
            try:
                with open(settingpath, "rb") as file:
                    settinglist = pickle.load(file)

            except Exception as a:
                self.statusBar().showMessage(str(a))
            # filename,_ = os.path.splitext(f)
            path=list(settinglist.values())[0].path
            foldersettinglist[path]=settinglist

        for f in datas:
            datapath=os.getcwd()+"/ache/"+f
            try:
                with open(datapath, "rb") as file:
                    datalist=pickle.load(file)
            except Exception as a:
                self.statusBar().showMessage(str(a))
            path = list(datalist.values())[0].path
            folderlist[path] = datalist
        self.folderlist=folderlist
        self.foldersettinglist=foldersettinglist

        self.FolderTable.addItems(list(self.folderlist.keys()))
        self.statusBar().showMessage("已加载历史数据！")


    def inLineEditfinished(self):
        path = self.inLineEdit.text()
        if (not (os.path.exists(path))):
            self.statusBar().showMessage("文件夹不存在，请重新输入！")
        elif (path == self.currentpath):
            self.statusBar().showMessage("读取文件夹位置未改变！")
        else:
            self.readfile()

    def selectfile(self):
        self.statusBar().showMessage("正在选择文件夹...")
        path = QFileDialog.getExistingDirectory(self, "请选择数据文件的根目录")
        # path = "C:/Users/ENERGY/Desktop/工作文件/test"
        # path = "D:/工作文件2/lhy"
        if path == "":
            self.statusBar().showMessage("未选择文件夹！")
        # elif path in self.folderlist:
        #     self.statusBar().showMessage("当前文件夹在列表中！")
        else:
            self.inLineEdit.setText(path)
            self.readfile()

    def readfile(self):
        path=self.inLineEdit.text()
        self.readthread=readfilethread(path)
        self.readthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.readthread.progressBarValueInt.connect(self.progressBar.setValue)
        self.readthread.endinglist.connect(self.addData)
        self.readthread.progressBarVisualBool.connect(self.progressBar.setVisible)
        self.readthread.start()

    def addData(self,path,data,setting):
        # 文件夹内无文件
        if len(data)==0:
            self.statusBar().showMessage("此文件夹没有有效文件！")
            return

        # 保存本地数据
        self.savelocalpathachethread=savelocalpathachethread(path,data,setting)
        self.savelocalpathachethread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savelocalpathachethread.start()

        self.folderlist[path]=data
        # if(path in self.folderlist):
        #     self.folderlist.pop(path)
        self.foldersettinglist[path]=setting
        self.currentpath=path
        self.FolderTable.clear()
        self.FolderTable.addItems(list(self.folderlist.keys()))
        self.FolderTable.setCurrentRow(len(self.folderlist)-1)
        self.FolderTable.item(len(self.folderlist)-1).setSelected(True)


    def FolderTableclicked(self,index:QModelIndex):
        self.currentpath=str(index.data())
        self.datalist = self.folderlist[str(index.data())]
        self.datasettinglist = self.foldersettinglist[str(index.data())]
        print(self.datalist)
        # print(data)
        self.filelistTable.clearContents()
        # self.filelistTable.setColumnCount(1)
        self.filelistTable.setRowCount(len(self.datalist))
        for i,data in enumerate(self.datalist.values()):
            # ck = QCheckBox()
            # h = QHBoxLayout()
            # h.setAlignment(Qt.AlignCenter)
            # h.addWidget(ck)
            # w = QWidget()
            # w.setLayout(h)
            # self.filelistTable.setCellWidget(i, 0, w)
            # self.filelistTable.cellWidget(i, 0).
            self.filelistTable.setItem(i, 0, QTableWidgetItem(data.name))
            self.filelistTable.setItem(i, 1, QTableWidgetItem(data.StartTime))
            self.filelistTable.setItem(i, 2, QTableWidgetItem(data.duration))
            self.filelistTable.setItem(i, 3, QTableWidgetItem(str(data.Total)))
            self.filelistTable.setItem(i, 4, QTableWidgetItem(str(data.in1_mean)))
            self.filelistTable.setItem(i, 5, QTableWidgetItem(str(data.in1_variance)))
            self.filelistTable.setItem(i, 6, QTableWidgetItem(str(data.in2_mean)))
            self.filelistTable.setItem(i, 7, QTableWidgetItem(str(data.in2_variance)))
            self.filelistTable.setItem(i, 8, QTableWidgetItem(str(data.in1_group_mean)))
            self.filelistTable.setItem(i, 9, QTableWidgetItem(str(data.in1_group_variance)))
            self.filelistTable.setItem(i, 10, QTableWidgetItem(str(data.in2_group_mean)))
            self.filelistTable.setItem(i, 11, QTableWidgetItem(str(data.in2_group_variance)))

    def filelistTableclicked(self):
        selectrow=self.filelistTable.verticalHeader().selectionModel().selectedIndexes()[-1].row()
        text=self.filelistTable.item(selectrow,0).text()
        self.data=self.datalist[text]
        self.setting=self.datasettinglist[text]
        self.pw1showcheckbox1.blockSignals(True)
        self.pw1showcheckbox2.blockSignals(True)
        self.pw1showcheckbox3.blockSignals(True)
        self.pw1showcheckbox4.blockSignals(True)
        self.pw1showcheckbox5.blockSignals(True)
        self.pw1showcheckbox6.blockSignals(True)
        self.pw2showcheckbox1.blockSignals(True)
        self.pw2showcheckbox2.blockSignals(True)
        self.pw2showcheckbox3.blockSignals(True)
        self.pw2showcheckbox4.blockSignals(True)
        self.pw2showcheckbox5.blockSignals(True)
        self.pw2showcheckbox6.blockSignals(True)
        self.pw3showcheckbox1.blockSignals(True)
        self.pw3showcheckbox2.blockSignals(True)
        self.pw3showcheckbox3.blockSignals(True)
        self.pw3showcheckbox4.blockSignals(True)
        self.pw3showcheckbox5.blockSignals(True)
        self.pw3showcheckbox6.blockSignals(True)
        
        if self.setting.pw1in1:
            self.pw1showcheckbox1.setChecked(True)
            self.pw1dataline1.setData(self.data.x,self.data.in1)
        else:
            self.pw1showcheckbox1.setChecked(False)
            self.pw1dataline1.setData([],[])

        if self.setting.pw1in2:
            self.pw1showcheckbox2.setChecked(True)
            self.pw1dataline2.setData(self.data.x,self.data.in2)
        else:
            self.pw1showcheckbox2.setChecked(False)
            self.pw1dataline2.setData([],[])

        if self.setting.pw1out:
            self.pw1showcheckbox3.setChecked(True)
            self.pw1dataline3.setData(self.data.x,self.data.out)
        else:
            self.pw1showcheckbox3.setChecked(False)
            self.pw1dataline3.setData([],[])

        if self.setting.pw1in1_2:
            self.pw1showcheckbox4.setChecked(True)
            self.pw1dataline4.setData(self.data.x,self.data.in1_2)
        else:
            self.pw1showcheckbox4.setChecked(False)
            self.pw1dataline4.setData([],[])

        if self.setting.pw1in2_1:
            self.pw1showcheckbox5.setChecked(True)
            self.pw1dataline5.setData(self.data.x,self.data.in2_1)
        else:
            self.pw1showcheckbox5.setChecked(False)
            self.pw1dataline5.setData([],[])

        if self.setting.pw1dAngle:
            self.pw1showcheckbox6.setChecked(True)
            self.pw1dataline6.setData(self.data.x,self.data.dAngle)
        else:
            self.pw1showcheckbox6.setChecked(False)
            self.pw1dataline6.setData([],[])
        
        if self.setting.pw2in1:
            self.pw2showcheckbox1.setChecked(True)
            self.pw2dataline1.setData(self.data.x,self.data.in1)
        else:
            self.pw2showcheckbox1.setChecked(False)
            self.pw2dataline1.setData([],[])

        if self.setting.pw2in2:
            self.pw2showcheckbox2.setChecked(True)
            self.pw2dataline2.setData(self.data.x,self.data.in2)
        else:
            self.pw2showcheckbox2.setChecked(False)
            self.pw2dataline2.setData([],[])

        if self.setting.pw2out:
            self.pw2showcheckbox3.setChecked(True)
            self.pw2dataline3.setData(self.data.x,self.data.out)
        else:
            self.pw2showcheckbox3.setChecked(False)
            self.pw2dataline3.setData([],[])

        if self.setting.pw2in1_2:
            self.pw2showcheckbox4.setChecked(True)
            self.pw2dataline4.setData(self.data.x,self.data.in1_2)
        else:
            self.pw2showcheckbox4.setChecked(False)
            self.pw2dataline4.setData([],[])

        if self.setting.pw2in2_1:
            self.pw2showcheckbox5.setChecked(True)
            self.pw2dataline5.setData(self.data.x,self.data.in2_1)
        else:
            self.pw2showcheckbox5.setChecked(False)
            self.pw2dataline5.setData([],[])

        if self.setting.pw2dAngle:
            self.pw2showcheckbox6.setChecked(True)
            self.pw2dataline6.setData(self.data.x,self.data.dAngle)
        else:
            self.pw2showcheckbox6.setChecked(False)
            self.pw2dataline6.setData([],[])

        if self.setting.pw3in1:
            self.pw3showcheckbox1.setChecked(True)
            self.pw3dataline1.setData(self.data.x[self.setting.x1:self.setting.x2],self.data.in1[self.setting.x1:self.setting.x2])
        else:
            self.pw3showcheckbox1.setChecked(False)
            self.pw3dataline1.setData([],[])

        if self.setting.pw3in2:
            self.pw3showcheckbox2.setChecked(True)
            self.pw3dataline2.setData(self.data.x[self.setting.x1:self.setting.x2],self.data.in2[self.setting.x1:self.setting.x2])
        else:
            self.pw3showcheckbox2.setChecked(False)
            self.pw3dataline2.setData([],[])

        if self.setting.pw3out:
            self.pw3showcheckbox3.setChecked(True)
            self.pw3dataline3.setData(self.data.x[self.setting.x1:self.setting.x2],self.data.out[self.setting.x1:self.setting.x2])
        else:
            self.pw3showcheckbox3.setChecked(False)
            self.pw3dataline3.setData([],[])

        if self.setting.pw3in1_2:
            self.pw3showcheckbox4.setChecked(True)
            self.pw3dataline4.setData(self.data.x[self.setting.x1:self.setting.x2],self.data.in1_2[self.setting.x1:self.setting.x2])
        else:
            self.pw3showcheckbox4.setChecked(False)
            self.pw3dataline4.setData([],[])

        if self.setting.pw3in2_1:
            self.pw3showcheckbox5.setChecked(True)
            self.pw3dataline5.setData(self.data.x[self.setting.x1:self.setting.x2],self.data.in2_1[self.setting.x1:self.setting.x2])
        else:
            self.pw3showcheckbox5.setChecked(False)
            self.pw3dataline5.setData([],[])

        if self.setting.pw3dAngle:
            self.pw3showcheckbox6.setChecked(True)
            self.pw3dataline6.setData(self.data.x[self.setting.x1:self.setting.x2],self.data.dAngle[self.setting.x1:self.setting.x2])
        else:
            self.pw3showcheckbox6.setChecked(False)
            self.pw3dataline6.setData([],[])

        self.pw1showcheckbox1.blockSignals(False)
        self.pw1showcheckbox2.blockSignals(False)
        self.pw1showcheckbox3.blockSignals(False)
        self.pw1showcheckbox4.blockSignals(False)
        self.pw1showcheckbox5.blockSignals(False)
        self.pw1showcheckbox6.blockSignals(False)
        self.pw2showcheckbox1.blockSignals(False)
        self.pw2showcheckbox2.blockSignals(False)
        self.pw2showcheckbox3.blockSignals(False)
        self.pw2showcheckbox4.blockSignals(False)
        self.pw2showcheckbox5.blockSignals(False)
        self.pw2showcheckbox6.blockSignals(False)
        self.pw3showcheckbox1.blockSignals(False)
        self.pw3showcheckbox2.blockSignals(False)
        self.pw3showcheckbox3.blockSignals(False)
        self.pw3showcheckbox4.blockSignals(False)
        self.pw3showcheckbox5.blockSignals(False)
        self.pw3showcheckbox6.blockSignals(False)

        print(self.setting.x2)
        self.pw2Line1.setPos(QPointF(self.data.x[self.setting.x1],0))
        self.pw2Line2.setPos(QPointF(self.data.x[self.setting.x2],0))
        # self.pw3.getPlotItem().enableAutoRange()
        self.pw2.enableAutoRange()
        self.pw1.enableAutoRange()

        self.imagelabel.axes.plot(self.data.x)

    def pw2Line1PositionChangeFinished(self,pw3line1):
        print(pw3line1.getXPos())

    def pw3Line2PositionChangeFinished(self,pw3line2):
        print(pw3line2.getXPos())

    def pw2LinePositionChangeFinished(self):
        x1=round(self.pw2Line1.getXPos())
        x2=round(self.pw2Line2.getXPos())
        self.cutdatathread=getcutdatathread(self.data,x1,x2)
        self.cutdatathread.endingmulti.connect(self.plotcutdata)
        self.cutdatathread.run()

    def plotcutdata(self,data,index1,index2):
        self.setting.x1=index1
        self.setting.x2=index2
        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()
        if self.pw3showcheckbox1.isChecked():
            self.pw3dataline1.setData(data.x[index1:index2],data.in1[index1:index2])
        else:
            self.pw3dataline1.setData([],[])
        if self.pw3showcheckbox2.isChecked():
            self.pw3dataline2.setData(data.x[index1:index2],data.in2[index1:index2])
        else:
            self.pw3dataline2.setData([],[])

        if self.pw3showcheckbox3.isChecked():
            self.pw3dataline3.setData(data.x[index1:index2],data.out[index1:index2])
        else:
            self.pw3dataline3.setData([],[])

        if self.pw3showcheckbox4.isChecked():
            self.pw3dataline4.setData(data.x[index1:index2],data.in1_2[index1:index2])
        else:
            self.pw3dataline4.setData([],[])
        if self.pw3showcheckbox5.isChecked():
            self.pw3dataline5.setData(data.x[index1:index2],data.in2_1[index1:index2])
        else:
            self.pw3dataline5.setData([],[])    
        if self.pw3showcheckbox6.isChecked():
            self.pw3dataline6.setData(data.x[index1:index2],data.dAngle[index1:index2])
        else:
            self.pw3dataline6.setData([],[])
        # self.pw3dataline1.setData(datax,data,symbol="o")
        # self.pw3.getPlotItem().enableAutoRange()
        self.pw3.enableAutoRange()



    # 图像显示状态改变
    def pw1showcheckbox1stateChanged(self,index):
        if self.data==None:
            return
        if index==2:
            self.pw1dataline1.setData(self.data.x,self.data.in1)
            self.setting.pw1in1=True
        else:
            self.pw1dataline1.setData([],[])
            self.setting.pw1in1 = False
        self.pw1.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw1showcheckbox2stateChanged(self,index):
        if self.data == None:
            return
        if index == 2:
            self.pw1dataline2.setData(self.data.x, self.data.in2)
            self.setting.pw1in2 = True
        else:
            self.pw1dataline2.setData([], [])
            self.setting.pw1in2 = False
        self.pw1.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw1showcheckbox3stateChanged(self,index):
        if self.data == None:
            return
        if index == 2:
            self.pw1dataline3.setData(self.data.x, self.data.out)
            self.setting.pw1out = True
        else:
            self.pw1dataline3.setData([], [])
            self.setting.pw1out = False
        self.pw1.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw1showcheckbox4stateChanged(self,index):
        if self.data == None:
            return
        if index == 2:
            self.pw1dataline4.setData(self.data.x, self.data.in1_2)
            self.setting.pw1in1_2 = True
        else:
            self.pw1dataline4.setData([], [])
            self.setting.pw1in1_2 = False
        self.pw1.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw1showcheckbox5stateChanged(self,index):
        if self.data == None:
            return
        if index == 2:
            self.pw1dataline5.setData(self.data.x, self.data.in2_1)
            self.setting.pw1in2_1 = True
        else:
            self.pw1dataline5.setData([], [])
            self.setting.pw1in2_1 = False
        self.pw1.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()
        
    def pw1showcheckbox6stateChanged(self,index):
        if self.data == None:
            return
        if index == 2:
            self.pw1dataline6.setData(self.data.x, self.data.dAngle)
            self.setting.pw1dAngle = True
        else:
            self.pw1dataline6.setData([], [])
            self.setting.pw1dAngle = False
        self.pw1.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw2showcheckbox1stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw2dataline1.setData(self.data.x, self.data.in1)
            self.setting.pw2in1 = True
        else:
            self.pw2dataline1.setData([], [])
            self.setting.pw2in1 = False
        self.pw2.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()


    def pw2showcheckbox2stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw2dataline2.setData(self.data.x, self.data.in2)
            self.setting.pw2in2 = True
        else:
            self.pw2dataline2.setData([], [])
            self.setting.pw2in2 = False
        self.pw2.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw2showcheckbox3stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw2dataline3.setData(self.data.x, self.data.out)
            self.setting.pw2out = True
        else:
            self.pw2dataline3.setData([], [])
            self.setting.pw2out = False
        self.pw2.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw2showcheckbox4stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw2dataline4.setData(self.data.x, self.data.in1_2)
            self.setting.pw2in1_2 = True
        else:
            self.pw2dataline4.setData([], [])
            self.setting.pw2in1_2 = False
        self.pw2.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw2showcheckbox5stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw2dataline5.setData(self.data.x, self.data.in2_1)
            self.setting.pw2in2_1 = True
        else:
            self.pw2dataline5.setData([], [])
            self.setting.pw2in2_1 = False
        self.pw2.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()
        
    def pw2showcheckbox6stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw2dataline6.setData(self.data.x, self.data.dAngle)
            self.setting.pw2dAngle = True
        else:
            self.pw2dataline6.setData([], [])
            self.setting.pw2dAngle = False
        self.pw2.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw3showcheckbox1stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw3dataline1.setData(self.data.x, self.data.in1)
            self.setting.pw3in1 = True
        else:
            self.pw3dataline1.setData([], [])
            self.setting.pw3in1 = False
        self.pw3.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw3showcheckbox2stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw3dataline2.setData(self.data.x, self.data.in2)
            self.setting.pw3in2 = True
        else:
            self.pw3dataline2.setData([], [])
            self.setting.pw3in2 = False
        self.pw3.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw3showcheckbox3stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw3dataline3.setData(self.data.x, self.data.out)
            self.setting.pw3out = True
        else:
            self.pw3dataline3.setData([], [])
            self.setting.pw3out = False
        self.pw3.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw3showcheckbox4stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw3dataline4.setData(self.data.x, self.data.in1_2)
            self.setting.pw3in1_2 = True
        else:
            self.pw3dataline4.setData([], [])
            self.setting.pw3in1_2 = False
        self.pw3.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw3showcheckbox5stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw3dataline5.setData(self.data.x, self.data.in2_1)
            self.setting.pw3in2_1 = True

        else:
            self.pw3dataline5.setData([], [])
            self.setting.pw3in2_1 = False
            self.savesettingthread=savesettingthread(self.currentpath, self.datasettinglist)
            self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
            self.savesettingthread.run()

        self.pw3.enableAutoRange()
        self.savesettingthread = savesettingthread(self.currentpath, self.setting)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw3showcheckbox6stateChanged(self, index):
        if self.data == None:
            return
        if index == 2:
            self.pw3dataline6.setData(self.data.x, self.data.dAngle)
            self.setting.pw3dAngle = True
            self.savesettingthread=savesettingthread(self.currentpath, self.datasettinglist)
            self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
            self.savesettingthread.run()
        else:
            self.pw3dataline6.setData([], [])
            self.setting.pw3dAngle = False
        self.pw3.enableAutoRange()

        self.savesettingthread = savesettingthread(self.currentpath, self.datasettinglist)
        self.savesettingthread.statusBarMessageStr.connect(self.statusBar().showMessage)
        self.savesettingthread.run()

    def pw3FullScreenclicked(self):
        if self.data==None:
            self.statusBar().showMessage("请先选择图片！")
            return
        self.statusBar().showMessage("正在加载全屏视图...")
        print("self.data:",self.data.x)
        if self.pw3showcheckbox1.isChecked():
            self.pw3fcdataline1.setData(self.data.x[self.setting.x1:self.setting.x2], self.data.in1[self.setting.x1:self.setting.x2])
        else:
            self.pw3fcdataline1.setData([], [])
        if self.pw3showcheckbox2.isChecked():
            self.pw3fcdataline2.setData(self.data.x[self.setting.x1:self.setting.x2], self.data.in2[self.setting.x1:self.setting.x2])
        else:
            self.pw3fcdataline2.setData([], [])

        if self.pw3showcheckbox3.isChecked():
            self.pw3fcdataline3.setData(self.data.x[self.setting.x1:self.setting.x2], self.data.out[self.setting.x1:self.setting.x2])
        else:
            self.pw3fcdataline3.setData([], [])

        if self.pw3showcheckbox4.isChecked():
            self.pw3fcdataline4.setData(self.data.x[self.setting.x1:self.setting.x2], self.data.in1_2[self.setting.x1:self.setting.x2])
        else:
            self.pw3fcdataline4.setData([], [])
        if self.pw3showcheckbox5.isChecked():
            self.pw3fcdataline5.setData(self.data.x[self.setting.x1:self.setting.x2], self.data.in2_1[self.setting.x1:self.setting.x2])
        else:
            self.pw3fcdataline5.setData([], [])
        if self.pw3showcheckbox6.isChecked():
            self.pw3fcdataline6.setData(self.data.x[self.setting.x1:self.setting.x2], self.data.dAngle[self.setting.x1:self.setting.x2])
        else:
            self.pw3fcdataline6.setData([], [])
        # self.pw3dataline1.setData(datax,data,symbol="o")
        # self.pw3.getPlotItem().enableAutoRange()
        self.pw3fc.enableAutoRange()
        self.stackedWidget.setCurrentIndex(1)
        self.statusBar().showMessage("已加载全屏视图！")


    def pwfcexitbuttonclicked(self):
        self.stackedWidget.setCurrentIndex(0)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ui = main()
    ui.show()
    sys.exit(app.exec_())