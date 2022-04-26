from re import T
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import math

class CircleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image = QImage(QSize(1000, 600), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.brushSize = 1
        self.brushColor = Qt.black

        # mode
        self.drawMode = "null"

        # click
        self.ctn = 0

        # click event
        self.startPoint = QPoint()
        self.endPoint = QPoint()

        self.initUI()

    # UI
    def initUI(self):
        # set basic UI
        self.setWindowTitle('بونوبونو')
        self.setGeometry(300, 300, 400, 400)
        self.setFixedSize(1000, 600)
        self.statusBar().showMessage('coordinates')
        self.show()

        # set Action
        menu = self.menuBar()
        menu.setNativeMenuBar(False)

        fileMenu = menu.addMenu('File')
        circleMenu = menu.addMenu('Circle')

        # clear
        clearAction = QAction('Clear', self)
        clearAction.triggered.connect(self.clear)

        # save
        saveAction = QAction('Save', self)
        saveAction.triggered.connect(self.save)

        # quit
        quitAction = QAction('Quit', self)
        quitAction.triggered.connect(QCoreApplication.instance().quit)

        # Bresenham Circle
        bhCircleAction = QAction('Bresenham Circle Algorithm', self)
        bhCircleAction.triggered.connect(self.bresenhamCircle)

        # Mid-point Circle
        mpCircleAction = QAction('Mid-point Circle Algorithm', self)
        mpCircleAction.triggered.connect(self.midpointCircle)

        # set file menu
        fileMenu.addAction(clearAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(quitAction)

        # set circle menu
        circleMenu.addAction(bhCircleAction)
        circleMenu.addAction(mpCircleAction)
    
    # paint event
    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())
    
    # clear
    def clear(self):
        self.ctn = 0
        self.image.fill(Qt.white)
        self.update()
    
    # 마우스 관련된 이벤트
    def mousePress(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.ctn += 1
        
        # 좌표를 얻어와서 point1, point2
        if self.ctn % 2 == 1:
            self.startPoint = e.pos()
        else:
            self.endPoint = e.pos()
    
    def mouseMove(self, e):
        if (e.buttons() & Qt.LeftButton):
            return
    
    def mouseRelease(self, e):
        if e.button() == Qt.LeftButton:
            if self.drawMode == "Bresenham Circle":
                if self.ctn % 2 != 1:
                    self.bresenhamCircle()
            
            if self.drawMode == "Mid-point Circle":
                if self.ctn % 2 != 1:
                    self.midpointCircle()
    
    def bresenhamCircleMode(self):
        self.drawMode = "Bresenham Circle"
        self.cnt = 0
    
    def bresenhamCircle(self):
        print("Bresenham Circle Algorithm")

        # set Painter
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap))

        # algorithm
        xc, yc = int(self.startPoint.x()), int(self.endPoint.y())
        xd, yd = int(self.endPoint.x()), int(self.endPoint.y())

        dx = math.pow(xd - xc, 2)
        dy = math.pow(yd - yc, 2)

        rad = int(math.sqrt(dx + dy))

        x = 0
        y = rad
        d = 3 - 2 * rad

        painter.drawPoint(xc, yc)

        while y >= x:
            x = x + 1

            if (d > 0):
                y = y - 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            
            painter.drawPoint(x, y)
        
        self.update()
    
    def midpointCircleMode(self):
        self.drawMode = "Mid-point Circle"
        self.cnt = 0
    
    def midpointCircle(self):
        print("Mid-point Circle Algorithm")

         # set Painter
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap))

        xc, yc = int(self.startPoint.x()), int(self.endPoint.y())
        
        rad = 20
        x, y = 0, rad
        p = 1 - rad

        painter.drawPoint(y + yc, x + xc)
        painter.drawPoint(-y + yc, x + xc)
        painter.drawPoint(x + yc, y + xc)
        painter.drawPoint(x + yc, -y + xc)

        x = 1
        while(x < y):
            if(p < 0):
                p = p + x + x + 1
            else:
                p = p + x + x + 1 - y - y
                y = y - 1

                i = 0
                for i in range(x):
                    painter.drawPoint(y + yc, i + xc)
                    painter.drawPoint(-y + yc, i + xc)
                    painter.drawPoint(y + yc, -i + xc)
                    painter.drawPoint(-y + yc, -i + xc)

                    painter.drawPoint(i + yc, y + xc)
                    painter.drawPoint(-i + yc, y + xc)
                    painter.drawPoint(i + yc, -y + xc)
                    painter.drawPoint(-i + yc, -y + xc)

                    x = x + 1
            
            painter.drawPoint(y + yc, x + xc)
            painter.drawPoint(-y + yc, x + xc)
            painter.drawPoint(y + yc, -x + xc)
            painter.drawPoint(-y + yc, -x + xc)

            painter.drawPoint(x + yc, y + xc)
            painter.drawPoint(-x + yc, y + xc)
            painter.drawPoint(x + yc, -y + xc)
            painter.drawPoint(-x + yc, -y + xc)

            x = x + 1
        
        self.update()

    def save(self):
        self.ctn = 0
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        
        if fpath:
            self.image.save(fpath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = CircleWindow()
    sys.exit(app.exec_())