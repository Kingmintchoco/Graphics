"""
컴퓨터그래픽스 - My CG Program (my_cg_program.py)

작성자          : 20197125 김현민
최초 작성일     : 2022. 04. 04.
마지막 수정일   : 2022. 04. 06.
작성 환경       : python 3.9.4 + PyQt5(GUI)
작성 목적       : 컴퓨터그래픽스 알고리즘의 이해 및 실습
이력사항        : 2022. 04. 04. 최초작성
                 2022. 04. 05. GUI환경 구현 및 DDA 알고리즘 추가
                 2022. 04. 06. Bresenham's line 알고리즘 추가
"""

from re import T
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math

class MyApp(QMainWindow):

    # 프로그램 생성자
    def __init__(self):
        super().__init__()
        self.image = QImage(QSize(1000, 600), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brush_size = 1
        self.brush_color = Qt.black

        # 모드 설정에 따른 플래그
        self.draw_mode = "None"

        # 클릭횟수를 저장, mod연산을통해 point1, point2를 구별
        self.counter = 0

        # 클릭이벤트를 통해서 point1, point2를 저장
        self.x1y1_point = QPoint()
        self.x2y2_point = QPoint()

        self.initUI()
        

    # 프로그램 UI 설정
    def initUI(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('Commands')
        linemenu = menubar.addMenu('Line Drawing')
        circlemenu = menubar.addMenu('Circle Drawing')
        ellipsemenu = menubar.addMenu('Ellipse Drawing')
        
        clear_action = QAction('Clear All', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.clear)
        
        save_action = QAction('Save as File', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)

        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(QCoreApplication.instance().quit)
        
        dda_action = QAction('DDA Algorithm', self)
        dda_action.setShortcut('Ctrl+D')
        dda_action.triggered.connect(self.dda_mode)

        cartesian_action = QAction('Cartesian Algorithm', self)
        cartesian_action.setShortcut('Ctrl+A')
        cartesian_action.triggered.connect(self.cartesian_mode)

        polar_action = QAction('Polar Coordinate Algorithm', self)
        polar_action.setShortcut('Ctrl+B')
        polar_action.triggered.connect(self.polar_mode)

        bresenham_circle_action = QAction('Bresenham Algorithm', self)
        bresenham_circle_action.setShortcut('Ctrl+V')
        bresenham_circle_action.triggered.connect(self.bresenham_circle_mode)

        bresenham_action = QAction('Bresenham Algorithm', self)
        bresenham_action.setShortcut('Ctrl+B')
        bresenham_action.triggered.connect(self.bresenham_mode)

        polar_ellipse_action = QAction('Polar Coordinate Algorithm', self)
        polar_ellipse_action.setShortcut('Ctrl+N')
        polar_ellipse_action.triggered.connect(self.polar_ellipse_mode)

        bresenham_ellipse_action = QAction('Bresenham Algorithm', self)
        bresenham_ellipse_action.setShortcut('Ctrl+M')
        bresenham_ellipse_action.triggered.connect(self.bresenham_ellipse_mode)

        filemenu.addAction(clear_action)
        filemenu.addAction(save_action)
        filemenu.addAction(quit_action)
        linemenu.addAction(dda_action)
        linemenu.addAction(bresenham_action)
        circlemenu.addAction(cartesian_action)
        circlemenu.addAction(polar_action)
        circlemenu.addAction(bresenham_circle_action)
        ellipsemenu.addAction(polar_ellipse_action)
        ellipsemenu.addAction(bresenham_ellipse_action)
        
        self.setWindowTitle('My CG Program - 20197125 김현민')
        self.setGeometry(300, 300, 400, 400)
        self.setFixedSize(1000, 600)
        self.statusBar().showMessage('좌표가 여기에 출력됩니다.')
        self.show()

    # 점그리기, 선그리기를 위한 페인트 이벤트 설정
    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())
    
    #화면 지우기
    def clear(self):
        self.counter = 0
        self.image.fill(Qt.white)
        self.update()

    # 마우스 관련된 이벤트
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.counter += 1

            # 좌표를 얻어와서 point1, point2를 설정
            if self.counter%2 == 1:
                self.x1y1_point = e.pos()
            else:
                self.x2y2_point = e.pos()  

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            return

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

            # 마우스클릭(릴리즈)시에 설정된 모드에따라 function을 실행
            if self.draw_mode == "dda":
                if self.counter%2 != 1:
                    self.dda_function()
            
            if self.draw_mode == "bresenham":
                if self.counter%2 != 1:
                    self.bresenham_function()
            
            if self.draw_mode == "polar":
                if self.counter%2 != 1:
                    self.polar_function()

            if self.draw_mode == "cartesian":
                if self.counter%2 != 1:
                    self.cartesian_function()

            if self.draw_mode == "bresenham_circle":
                if self.counter%2 != 1:
                    self.bresenham_circle_function()

    # 파일로 저장
    def save(self):
        self.counter = 0
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if fpath:
            self.image.save(fpath)
    
    # DDA 알고리즘을 활용한 라인드로잉
    def dda_mode(self):
        self.draw_mode = "dda"
        self.counter = 0
        
    def dda_function(self):
        print("DDA 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # 알고리즘 START
        x1, y1 = self.x1y1_point.x(), self.x1y1_point.y()
        x2, y2 = self.x2y2_point.x(), self.x2y2_point.y()
        x, y = x1, y1

        painter.drawPoint(int(x), int(y))

        dx = x2 - x1
        dy = y2 - y1

        steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

        x_inc = float(dx / steps)
        y_inc = float(dy / steps)

        for i in range(0, int(steps + 1)):
            painter.drawPoint(int(x1), int(y1))
            x1 += x_inc
            y1 += y_inc

        # 스테이터스바에 출력, (left-top corner 형식이기때문에 보기좋게 값을 수정해주었음.)
        msg1 = "DDA 알고리즘 - (" + str(x) + ", " + str(-1*(y-600))+ ") -> (" + str(int(x1)) + ", " + str(int(-1*(y1-600))) + ")"
        msg2 = "  / 기울기 : " + str(round(((-1*(y1-600))-(-1*(y-600)))/(x1-x), 2))
        self.statusBar().showMessage(msg1 + msg2)
        self.update()

    # Bresenham 알고리즘을 활용한 라인드로잉
    def bresenham_mode(self):
        self.draw_mode = "bresenham"
        self.counter = 0

    def bresenham_function(self):
        print("Bresenham 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # 알고리즘 START
        x1, y1 = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x2, y2 = int(self.x2y2_point.x()), int(self.x2y2_point.y())
        gradient = (y2-y1) / (x2-x1)
        tmp_x, tmp_y = x1, y1

        x, y = x1, y1
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        slope = dy/float(dx)

        swap = False
        
        if slope > 1:
            dx, dy = dy, dx
            x, y = y, x
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            swap = True

        p = 2*dy - dx

        painter.drawPoint(x, y)

        for i in range(2, dx):
            if p > 0:
                y = y + 1 if y < y2 else y - 1
                p = p + 2*(dy - dx)
            else:
                p = p + 2*dy

            x = x + 1 if x < x2 else x -1

            if swap == False:
                painter.drawPoint(x, y)
                msg1 = "Bresenham 알고리즘 - (" + str(tmp_x) + ", " + str(-1*(tmp_y-600))+ ") -> (" + str(int(x)) + ", " + str(int(-1*(y-600))) + ")"
            else:
                painter.drawPoint(y, x)
                msg1 = "Bresenham 알고리즘 - (" + str(tmp_x) + ", " + str(-1*(tmp_y-600))+ ") -> (" + str(600-int(x)) + ", " + str(int(y)) + ")"

        # 스테이터스바에 출력
        msg2 = "  / 기울기 : " + str(round(-1*gradient, 2))
        self.statusBar().showMessage(msg1 + msg2)
        self.update()

    def cartesian_mode(self):
        self.draw_mode = "cartesian"
        self.counter = 0

    def cartesian_function(self):
        print("Cartesian circle 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # 알고리즘 START
        xc, yc = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x2, y2 = int(self.x2y2_point.x()), int(self.x2y2_point.y())

        delta_x = math.pow(x2 - xc, 2)
        delta_y = math.pow(y2 - yc , 2)
        radius = int(math.sqrt(delta_x + delta_y))

        for x in range(xc - radius, xc + radius):
            pow_r = math.pow(radius, 2)
            pow_xminc = math.pow(x-xc, 2)
            y = yc + math.sqrt(abs(pow_r - pow_xminc))
            painter.drawPoint(x, y)
            y = yc - math.sqrt(abs(pow_r - pow_xminc))
            painter.drawPoint(x, y)
            x = x + 1

        self.update()

    def polar_mode(self):
        self.draw_mode = "polar"
        self.counter = 0

    def polar_function(self):
        print("Polar circle 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # 알고리즘 START
        x2, y2 = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x1, y1 = int(self.x2y2_point.x()), int(self.x2y2_point.y())

        delta_x = math.pow((x2-x1), 2)
        delta_y = math.pow((y2-y1), 2)

        radius = math.sqrt(delta_x + delta_y)

        for i in range(0, 45):
            radian = i * math.pi / 180
            x = int(radius * math.cos(radian))
            y = int(radius * math.sin(radian))

            painter.drawPoint(x2+x, y2+y)
            painter.drawPoint(x2+y, y2+x)
            painter.drawPoint(x2+y, y2-x)
            painter.drawPoint(x2+x, y2-y)
            painter.drawPoint(x2-x, y2-y)
            painter.drawPoint(x2-y, y2-x)
            painter.drawPoint(x2-y, y2+x)
            painter.drawPoint(x2-x, y2+y)

        self.update()

    
    def bresenham_circle_mode(self):
        self.draw_mode = "bresenham_circle"
        self.counter = 0
    def bresenham_circle_function(self):
        print("Bresenham circle 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # 알고리즘 START
        xc, yc = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x2, y2 = int(self.x2y2_point.x()), int(self.x2y2_point.y())

        delta_x = math.pow(x2 - xc, 2)
        delta_y = math.pow(y2 - yc , 2)
        radius = int(math.sqrt(delta_x + delta_y))

        x = 0
        y = radius
        d = 3 - 2 * radius

        painter.drawPoint(xc, yc)

        while y >= x:
            x = x + 1
            if(d > 0): 
                y = y - 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            painter.drawPoint(x, y)
        
        self.update()

    def polar_ellipse_mode(self):
        self.draw_mode = "polar_ellipse"
        self.counter = 0
    
    def bresenham_ellipse_mode(self):
        self.draw_mode = "bresenham_ellipse"
        self.counter = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())