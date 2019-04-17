
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import numpy as np
import ConexCC as cc

print('-'*60)
print('-'*60)
print('STARTING RASTER GUI')
print('-'*60)

class RasterGUI(QDialog):
	def __init__(self,parent=None):
		super().__init__()
		self.title = 'Raster GUI'
		self.left = 50
		self.top = 50
		self.width = 1000
		self.height = 600
		self.laser = QPoint(500,300)
		self.inc = 10
		#defaults
		self.xvel = 0.4
		self.yvel = 0.4
		self.acc = .1
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)
		self.createJoystick()
		self.createCurrent()
		self.createConfig()

		self.spaceItem = QLabel('		'*5)

		self.ENGAGE = QPushButton('ENGAGE!')
		self.ENGAGE.setStyleSheet('background-color: green; font: 20px')

		err_lab = QLabel('ERROR:')
		self.err_box = QLineEdit('NONE')

		mainLayout = QGridLayout()
		mainLayout.addWidget(self.ConfBox,0,0)
		mainLayout.addWidget(self.ENGAGE,0,1,1,2)
		mainLayout.addWidget(self.spaceItem,1,1,1,2)
		mainLayout.addWidget(self.JoyBox,1,3)
		mainLayout.addWidget(self.CurBox,0,3)
		mainLayout.addWidget(err_lab,2,1)
		mainLayout.addWidget(self.err_box,2,2)
		self.JoyBox.move(500,500)
		self.setLayout(mainLayout)
		self.show()

	def createJoystick(self):
		Lbutt = QPushButton('\n\n<\n\n')
		Ubutt = QPushButton('\n\n^\n\n')
		Dbutt = QPushButton('\n\nv\n\n')
		Rbutt = QPushButton('\n\n>\n\n')
		inc_label = QLabel('Increment:')
		self.inc_box = QLineEdit(str(self.inc),self)
		set_inc = QPushButton('SET')

		Lbutt.clicked.connect(self.Lbutt_clicked)
		Rbutt.clicked.connect(self.Rbutt_clicked)
		Ubutt.clicked.connect(self.Ubutt_clicked)
		Dbutt.clicked.connect(self.Dbutt_clicked)
		set_inc.clicked.connect(self.set_inc_clicked)

		self.JoyBox = QGroupBox('Motor Control')
		layout = QGridLayout()
		layout.addWidget(Lbutt,2,0)
		layout.addWidget(Rbutt,2,2)
		layout.addWidget(Ubutt,1,1)
		layout.addWidget(Dbutt,3,1)
		layout.addWidget(inc_label,0,0)
		layout.addWidget(self.inc_box,0,1)
		layout.addWidget(set_inc,0,2)
		self.JoyBox.setLayout(layout)

	def Lbutt_clicked(self):
		self.laser = QPoint(self.laser.x()-self.inc,self.laser.y())
		if self.on_target():
			self.err_box.setText('NONE')
			self.Xcur.setText(str(self.laser.x()))
		else:
			self.err_box.setText('OFF TARGET')
			self.laser = QPoint(self.laser.x()+self.inc,self.laser.y())
		self.update()

	def Rbutt_clicked(self):
		self.laser = QPoint(self.laser.x()+self.inc,self.laser.y())
		if self.on_target():
			self.err_box.setText('NONE')
			self.Xcur.setText(str(self.laser.x()))
		else:
			self.err_box.setText('OFF TARGET')
			self.laser = QPoint(self.laser.x()-self.inc,self.laser.y())
		self.update()

	def Ubutt_clicked(self):
		self.laser = QPoint(self.laser.x(),self.laser.y()-self.inc)
		if self.on_target():
			self.err_box.setText('NONE')
			self.Ycur.setText(str(self.height-self.laser.y()))
		else:
			self.err_box.setText('OFF TARGET')
			self.laser = QPoint(self.laser.x(),self.laser.y()+self.inc)
		self.update()

	def Dbutt_clicked(self):
		self.laser = QPoint(self.laser.x(),self.laser.y()+self.inc)
		if self.on_target():
			self.err_box.setText('NONE')
			self.Ycur.setText(str(self.height-self.laser.y()))
		else:
			self.err_box.setText('OFF TARGET')
			self.laser = QPoint(self.laser.x(),self.laser.y()-self.inc)
		self.update()

	def set_inc_clicked(self):
		self.inc = float(self.inc_box.text())

	def createCurrent(self):
		Xcur_label = QLabel('X Position:')
		Ycur_label = QLabel('Y Position:')
		self.Xcur = QLineEdit(str(self.laser.x()),self)
		self.Ycur = QLineEdit(str(self.height-self.laser.y()),self)
		Xset = QPushButton('GO')
		Yset = QPushButton('GO')
		Sbutt = QPushButton('STOP')
		Sbutt.setStyleSheet('background-color: red')

		Xset.clicked.connect(self.Xset_clicked)
		Yset.clicked.connect(self.Yset_clicked)

		self.CurBox = QGroupBox('Absolute Positions')
		layout = QGridLayout()
		layout.addWidget(Xcur_label,0,0)
		layout.addWidget(self.Xcur,0,1)
		layout.addWidget(Ycur_label,1,0)
		layout.addWidget(self.Ycur,1,1)
		layout.addWidget(Xset,0,2)
		layout.addWidget(Yset,1,2)
		layout.addWidget(Sbutt,2,2)
		self.CurBox.setLayout(layout)

	def Xset_clicked(self):
		self.laser = QPoint(float(self.Xcur.text()),self.laser.y())
		self.update()

	def Yset_clicked(self):
		self.laser = QPoint(self.laser.x(),float(self.Ycur.text()))
		self.update()

	def createConfig(self):
		xvel_lab = QLabel('X Velocity:')
		self.xvel_box = QLineEdit(str(self.xvel),self)
		xvel_set = QPushButton('SET')
		yvel_lab = QLabel('Y Velocity:')
		self.yvel_box = QLineEdit(str(self.yvel),self)
		yvel_set = QPushButton('SET')

		xvel_set.clicked.connect(self.xvel_set_clicked)
		yvel_set.clicked.connect(self.yvel_set_clicked)

		self.ConfBox = QGroupBox('Configuration')
		layout = QGridLayout()
		layout.addWidget(xvel_lab,0,0)
		layout.addWidget(self.xvel_box,0,1,1,2)
		layout.addWidget(xvel_set,0,3)
		layout.addWidget(yvel_lab,1,0)
		layout.addWidget(self.yvel_box,1,1,1,2)
		layout.addWidget(yvel_set,1,3)
		self.ConfBox.setLayout(layout)

	def xvel_set_clicked(self):
		self.xvel = float(self.xvel_box.text())
		self.update()

	def yvel_set_clicked(self):
		self.yvel = float(self.yvel_box.text())
		self.update()

	def paintEvent(self,event):
		qp = QPainter(self)
		qp.setPen(Qt.black)
		qp.setBrush(Qt.black)
		qp.drawEllipse(296,100,404,400)
		qp.setPen(QColor(175,100,0))
		qp.setBrush(QColor(175,100,0))
		qp.drawEllipse(300,100,400,400)
		qp.setPen(Qt.black)
		qp.setBrush(Qt.green)
		qp.drawEllipse(self.laser,4,4)

	def on_target(self):
		r = np.sqrt((self.laser.x()-500)**2+(self.laser.y()-300)**2)
		#print(r)
		if r <= 200:
			return True
		else:
			return False



if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	dark_palette = QPalette()
	dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
	dark_palette.setColor(QPalette.WindowText, Qt.white)
	dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
	dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
	dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
	dark_palette.setColor(QPalette.ToolTipText, Qt.white)
	dark_palette.setColor(QPalette.Text, Qt.white)
	dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
	dark_palette.setColor(QPalette.ButtonText, Qt.white)
	dark_palette.setColor(QPalette.BrightText, Qt.red)
	dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
	dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
	dark_palette.setColor(QPalette.HighlightedText, Qt.black)
	app.setPalette(dark_palette)
	app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
	gui = RasterGUI()
	sys.exit(app.exec_())