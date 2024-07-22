import cv2
import numpy as np
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *
from pyzbar.pyzbar import decode
from PyQt5.QtCore import Qt
import pyautogui
import time

class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("UI.ui", self)
        self.show()

        self.setWindowIcon(QtGui.QIcon('icon.jpg'))
        self.currfile = ""
        self.actionLoad.triggered.connect(self.loadimg)
        self.fullsc.triggered.connect(self.screen)
        self.pushButton.clicked.connect(self.decoder)
        self.pushButton_2.clicked.connect(self.enhance)
        self.actionUser_Guide.triggered.connect(self.help)


    def screen(self):
        QMainWindow.setWindowState(self,Qt.WindowMinimized)
        time.sleep(2)
        screen = pyautogui.screenshot()
        screen.save("screen.jpg")
        QMainWindow.setWindowState(self, Qt.WindowNoState)
        self.currfile = "screen.jpg"
        pixmap = QtGui.QPixmap(self.currfile)
        self.label.setPixmap(pixmap.scaled(500,500))
        self.label.setScaledContents(True)
    def loadimg(self):
        options = QFileDialog.Options()
        filters = "Image Files (*.jpg *.jpeg *.png *.bmp);;All Files (*.*)"
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", filters, options=options
        )

        if filename != "":
            self.currfile = filename
            pixmap = QtGui.QPixmap(self.currfile)
            pixmap = pixmap.scaled(500, 500)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

    def help(self):
        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('icon.jpg'))
        msg.setWindowTitle("Help")
        msg.setTextFormat(Qt.RichText)
        msg.setText(
            "<a href='https://docs.google.com/document/d/1jc-33Kr6ikLMBKTKN0WCHr8kn6JOaMyRMkA2vK9jOmo/edit?usp"
            "=sharing'> nhấn vô để xem hướng dẫn sử dụng :v </a>")
        msg.exec_()

    def decoder(self):
        img = cv2.imread(self.currfile)
        bcode = decode(img)
        if len(bcode) == 0:
            self.textEdit.setText("Ảnh không có QR hãy thử lại hoặc enhance ảnh. ")
        else:
            for i in range(len(bcode)):
                self.textEdit.append('\n' + bcode[i].data.decode("utf-8"))
            for obj in bcode:
                bounding_box = obj.rect
                cv2.rectangle(img, (int(bounding_box[0]), int(bounding_box[1])),
                              (int(bounding_box[0] + bounding_box[2]), int(bounding_box[1] + bounding_box[3])),
                              (255, 0, 0), 5)
            height, width, channel = img.shape
            bytesPerLine = 3 * width
            qImg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped() # tạo QImg để nạp vào Qpixmap
            pixmap = QtGui.QPixmap.fromImage(qImg)
            pixmap = pixmap.scaled(500, 500)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

    def enhance(self):
        img = cv2.imread(self.currfile)
        if self.CheckBright(img) == 'dark':
            img2 = self.gamma(img, 0.5)
        if self.CheckBright(img) == 'bright':
            img2 = self.gamma(img, 2)
        if self.CheckBright(img) == 'ok':
            img2 = img.copy()
        img3 = cv2.blur(img2,ksize=(3,3))
        height, width, channel = img3.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(img3.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
        pixmap = QtGui.QPixmap.fromImage(qImg)
        pixmap = pixmap.scaled(500, 500)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        cv2.imwrite("725105073.jpg", img3)
        self.currfile = "725105073.jpg"

    def gamma(self, img, g):
        imggam = np.float32(img) / 255
        imggam = np.power(imggam, g) * 255
        return np.uint8(imggam)

    def CheckBright(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [2], None, [256], [0, 256])

        sum = np.sum(hist)
        dark = 0
        bright = 0

        for i in range(0, 65):
            dark += hist[i, 0]
        for i in range(230, 255):
            bright += hist[i, 0]
        bright_per = bright / sum
        dark_per = dark / sum
        if bright_per > 0.4:
            mean = 'bright'
        elif dark_per > 0.2:
            mean = 'dark'
        else:
            mean = 'ok'
        return mean


def main():
    app = QApplication([])
    window = MyGui()
    app.exec_()


if __name__ == "__main__":
    main()
