import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Painter(QMainWindow):
    def __init__(self):
        super().__init__()

        # canvas
        self.image = QImage(QSize(800, 500), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False

        # brush
        self.brushSize = 1
        self.brushColor = Qt.black

        # mode set
        self.mode = ""
    
        # point
        self.isFirst = 0
        self.firstPoint = QPoint()
        self.lastPoint = QPoint()

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        # menu - file
        fileMenu = menubar.addMenu('File')

        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)

        clearAction = QAction('Clear', self)
        clearAction.setShortcut('Ctrl+C')
        clearAction.triggered.connect(self.clear)

        # menu - figure
        createMenu = menubar.addMenu('Create')

        createPolygon = QAction('Polygon', self)
        createPolygon.triggered.connect(self.createPolygon)

        createCircle = QAction('Circle', self)
        createCircle.triggered.connect(self.createCircle)

        # menu - draw mode
        polygonMenu = menubar.addMenu('Polygon')

        floodFillAction = QAction('Flood Fill', self)
        floodFillAction.triggered.connect(self.modeFloodFill)

        seedFillAction = QAction('Seed Fill', self)
        seedFillAction.triggered.connect(self.modeSeedFill)

        boundaryFillAction = QAction('Boundary Fill', self)
        boundaryFillAction.triggered.connect(self.modeBoundaryFill)
        
        # push action
        fileMenu.addAction(saveAction)
        fileMenu.addAction(clearAction)

        createMenu.addAction(createPolygon)
        createMenu.addAction(createCircle)

        polygonMenu.addAction(floodFillAction)
        polygonMenu.addAction(seedFillAction)
        polygonMenu.addAction(boundaryFillAction)
        
        # window
        self.setWindowTitle('20197122 최서현 중간고사')
        self.setGeometry(300, 300, 800, 500)
        self.show()

    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.isFirst += 1

            # 좌표 설정
            if self.isFirst % 2 == 1:
                self.firstPoint = e.pos()
            else:
                self.lastPoint = e.pos()

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            return

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

            if self.mode == "create circle":
                if self.isFirst % 2 != 1:
                    self.drawCircle()

            if self.mode == "create polygon":
                self.drawPolygon()

    def save(self):
        # 횟수 초기화
        self.isFirst = 0

        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if fpath:
            self.image.save(fpath)

    def clear(self):
        self.isFirst = 0
        self.image.fill(Qt.white)
        self.update()
    
    def modeFloodFill(self):
        self.mode = "flood fill"
        self.isFirst = 0
    
    def modeSeedFill(self):
        self.mode = "seed fill"
        self.isFirst = 0

    def modeBoundaryFill(self):
        self.mode = "boundary fill"
        self.isFirst = 0
    
    def createCircle(self):
        self.mode = "create circle"
        self.isFirst = 0
    
    def createPolygon(self):
        self.mode = "create polygon"
        self.isFirst = 0
    
    def drawCircle(self):
        # bresenham circle drawing
        print("Circle Drawing")

        p = QPainter(self.image)
        p.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap))

        centerX, centerY = int(self.firstPoint.x()), int(self.firstPoint.y())
        elseX, elseY = int(self.lastPoint.x()), int(self.lastPoint.y())

        dX = math.pow(elseX - centerX, 2)
        dY = math.pow(elseY - centerY, 2)
        
        r = int(math.sqrt(dX + dY))

        x, y = 0, r
        d = 3 - 2 * r

        p.drawPoint(centerX + x, centerY + y)
        p.drawPoint(centerX - x, centerY + y)
        p.drawPoint(centerX + x, centerY - y)
        p.drawPoint(centerX - x, centerY - y)
        p.drawPoint(centerX + y, centerY + x)
        p.drawPoint(centerX - y, centerY + x)
        p.drawPoint(centerX + y, centerY - x)
        p.drawPoint(centerX - y, centerY - x)
        self.update()

        while y >= x:
            x += 1

            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            
            p.drawPoint(centerX + x, centerY + y)
            p.drawPoint(centerX - x, centerY + y)
            p.drawPoint(centerX + x, centerY - y)
            p.drawPoint(centerX - x, centerY - y)
            p.drawPoint(centerX + y, centerY + x)
            p.drawPoint(centerX - y, centerY + x)
            p.drawPoint(centerX + y, centerY - x)
            p.drawPoint(centerX - y, centerY - x)

            self.update()
        
        self.update()
    
    def drawPolygon(self):
        print("Polygon drawing")

        p = QPainter(self.image)
        p.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap))

        





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Painter()
    sys.exit(app.exec_())