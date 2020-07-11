
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ui = main()
    ui.show()
    sys.exit(app.exec_())