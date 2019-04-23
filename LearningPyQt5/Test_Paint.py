from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os
import time

class Window(QMainWindow):

	Ts = [4,5,10,50,80]

	def __init__(self):
		super().__init__()
		self.title = 'Qt Drawing Test'
		self.top = 150
		self.left = 150
		self.width = 500
		self.height = 500
		self.InitWindow()

	def InitWindow(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.top,self.left,self.width,self.height)
		self.show()

	def TempToColor(self,T):
		tmax = 300
		val = int(816*T/tmax)
		col = QColor(51,51,51)
		if val <= 204:
			col = QColor(51,51+val,255)
		elif 204 < val <= 408:
			col = QColor(51,255,255-(val%204))
		elif 408 < val <= 612:
			col = QColor(51+(val%204),255,51)
		elif 612 < val <= 816:
			col = QColor(255,255-(val%204),51)
		return col

	def paintEvent(self,event):

		if self.Ts[0]>=4:
			oldTs = self.Ts
			newTs = [oldTs[0] - (1-3/oldTs[0]),
					oldTs[1] - (1-10/oldTs[1]),
					oldTs[2] - (1-4/oldTs[2]),
					oldTs[3] - (1-50/oldTs[3]),
					oldTs[4] - (1-80/oldTs[4])]
			self.Ts = newTs

		Thtop = self.Ts[3]
		Thbot = self.Ts[4]
		Tctop = self.Ts[1]
		Tcbot = self.Ts[2]
		Tcell = self.Ts[0]
		hottop = self.TempToColor(Thtop)
		hotbottom = self.TempToColor(Thbot)
		coldtop = self.TempToColor(Tctop)
		coldbottom = self.TempToColor(Tcbot)
		cell = self.TempToColor(Tcell)
		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(QPen(Qt.black,4,Qt.SolidLine))
		grad1 = QLinearGradient(100,50,100,400)
		grad1.setColorAt(0.0,hottop)
		grad1.setColorAt(1.0,hotbottom)
		painter.setBrush(grad1)
		painter.drawRect(100,50,300,400)
		grad2 = QLinearGradient(150,100,150,300)
		grad2.setColorAt(0.0,coldtop)
		grad2.setColorAt(1.0,coldbottom)
		painter.setBrush(grad2)
		painter.drawRect(150,100,200,300)
		painter.setBrush(cell)
		painter.drawRect(225,225,50,50)
		painter.end()

	



if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec_())
