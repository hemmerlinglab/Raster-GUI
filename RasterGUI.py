
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import numpy as np
import ConexCC as cc


class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setup()

	def setup(self):
		self.setGeometry(0,0,1100,600)
		self.setWindowTitle('Main Window')
		self.central_widget = RasterGUI(self)
		self.setCentralWidget(self.central_widget)

		exit_action = QAction('Quit',self)
		exit_action.triggered.connect(qApp.quit)

		menu_bar = self.menuBar()
		menu_bar.setNativeMenuBar(False)
		file_menu = menu_bar.addMenu('File')
		file_menu.addAction(exit_action)

		self.show()

	def closeEvent(self,event):
		reply = QuitMessage().exec_()
		if reply ==QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

class QuitMessage(QMessageBox):
	def __init__(self):
		QMessageBox.__init__(self)
		self.setText('Are you sure you want to quit?')
		self.addButton(self.No)
		self.addButton(self.Yes)

class RasterGUI(QWidget):
	def __init__(self,parent=None):
		super().__init__()
		self.title = 'Raster GUI'
		self.left = 50
		self.top = 50
		self.width = 1100
		self.height = 600
		self.laser = QPoint(self.width/2,self.height/2)
		self.inc = 0.01
		#defaults
		self.xvel = 0.4
		self.yvel = 0.4
		self.xmin = 3.6
		self.xmax = 4.8
		self.ymin = 3.6
		self.ymax = 4.8
		self.acc = .1
		self.pix = 400
		self.ulx = self.width/2-self.pix/2
		self.uly = self.height/2-self.pix/2
		self.initUI()

	def mmtpx(self,mm):
		print(mm)
		slp = self.pix/(self.xmax-self.xmin)
		px = int(mm*slp)
		print(px)
		return px

	def mmtpy(self,mm):
		slp = self.pix/(self.ymax-self.ymin)
		px = int(mm*slp)
		return px

	def ptmmx(self,px):
		slp = (self.xmax-self.xmin)/self.pix
		mm = px*slp
		return mm

	def ptmmy(self,px):
		slp = (self.ymax-self.ymin)/self.pix
		mm = px*slp
		return mm


	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)
		self.createJoystick()
		self.createCurrent()
		self.createConfig()
		self.createCalib()

		self.spaceItem = QLabel('	'*9)

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
		mainLayout.addWidget(self.CalBox,1,0)
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
		self.inc_box.returnPressed.connect(set_inc.click)

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
		self.laser = QPoint(self.laser.x()-(self.mmtpx(self.inc)-int(self.width/2-self.pix/2)),self.laser.y())
		if self.on_target():
			self.err_box.setText('NONE')
			self.Xcur.setText(str(self.ptmmx(self.laser.x())))
		else:
			self.err_box.setText('OFF TARGET')
			self.laser = QPoint(self.laser.x()+(self.mmtpx(self.inc)-int(self.width/2-self.pix/2)),self.laser.y())
		self.update()

	def Rbutt_clicked(self):
		self.laser = QPoint(self.laser.x()+(self.mmtpx(self.inc)-int(self.width/2-self.pix/2)),self.laser.y())
		if self.on_target():
			self.err_box.setText('NONE')
			self.Xcur.setText(str(self.ptmmx(self.laser.x())))
		else:
			self.err_box.setText('OFF TARGET')
			self.laser = QPoint(self.laser.x()-(self.mmtpx(self.inc)-int(self.width/2-self.pix/2)),self.laser.y())
		self.update()

	def Ubutt_clicked(self):
		self.laser = QPoint(self.laser.x(),self.laser.y()-(self.mmtpy(self.inc)-int(self.height/2-self.pix/2)))
		if self.on_target():
			self.err_box.setText('NONE')
			self.Ycur.setText(str(self.ptmmy(self.height-self.laser.y())))
		else:
			self.err_box.setText('OFF TARGET')
			self.laser = QPoint(self.laser.x(),self.laser.y()+(self.mmtpy(self.inc)-int(self.height/2-self.pix/2)))
		self.update()

	def Dbutt_clicked(self):
		self.laser = QPoint(self.laser.x(),self.laser.y()+(self.mmtpy(self.inc)-int(self.height/2-self.pix/2)))
		if self.on_target():
			self.err_box.setText('NONE')
			self.Ycur.setText(str(self.ptmmy(self.height-self.laser.y())))
		else:
			self.err_box.setText('OFF TARGET')
			self.laser = QPoint(self.laser.x(),self.laser.y()-(self.mmtpy(self.inc)-int(self.height/2-self.pix/2)))
		self.update()

	def set_inc_clicked(self):
		self.inc = float(self.inc_box.text())

	def createCalib(self):
		xmin_label = QLabel('X Min:')
		xmax_label = QLabel('X Max:')
		ymin_label = QLabel('Y Min:')
		ymax_label = QLabel('Y Max:')
		self.xmin_box = QLineEdit(str(self.xmin),self)
		self.xmax_box = QLineEdit(str(self.xmax),self)
		self.ymin_box = QLineEdit(str(self.ymin),self)
		self.ymax_box = QLineEdit(str(self.ymax),self)
		xmin_set = QPushButton('Set')
		xmax_set = QPushButton('Set')
		ymin_set = QPushButton('Set')
		ymax_set = QPushButton('Set')

		xmin_set.clicked.connect(self.xmin_set_clicked)
		xmax_set.clicked.connect(self.xmax_set_clicked)
		ymin_set.clicked.connect(self.ymin_set_clicked)
		ymax_set.clicked.connect(self.ymax_set_clicked)
		self.xmin_box.returnPressed.connect(xmin_set.click)
		self.xmax_box.returnPressed.connect(xmax_set.click)
		self.ymin_box.returnPressed.connect(ymin_set.click)
		self.ymax_box.returnPressed.connect(ymax_set.click)

		self.CalBox = QGroupBox('Calibration')
		layout = QGridLayout()
		layout.addWidget(xmin_label,0,0)
		layout.addWidget(xmax_label,1,0)
		layout.addWidget(ymin_label,2,0)
		layout.addWidget(ymax_label,3,0)
		layout.addWidget(self.xmin_box,0,1)
		layout.addWidget(self.xmax_box,1,1)
		layout.addWidget(self.ymin_box,2,1)
		layout.addWidget(self.ymax_box,3,1)
		layout.addWidget(xmin_set,0,2)
		layout.addWidget(xmax_set,1,2)
		layout.addWidget(ymin_set,2,2)
		layout.addWidget(ymax_set,3,2)
		self.CalBox.setLayout(layout)

	def xmin_set_clicked(self):
		self.xmin = float(self.xmin_box.text())
		self.update()

	def xmax_set_clicked(self):
		self.xmax = float(self.xmax_box.text())
		self.update()

	def ymin_set_clicked(self):
		self.ymin = float(self.ymin_box.text())
		self.update()

	def ymax_set_clicked(self):
		self.ymax = float(self.ymax_box.text())
		self.update()


	def createCurrent(self):
		Xcur_label = QLabel('X Position:')
		Ycur_label = QLabel('Y Position:')
		self.Xcur = QLineEdit(str(self.ptmmx(self.laser.x())),self)
		self.Ycur = QLineEdit(str(self.ptmmy(self.height-self.laser.y())),self)
		Xset = QPushButton('GO')
		Yset = QPushButton('GO')
		Sbutt = QPushButton('STOP')
		Sbutt.setStyleSheet('background-color: red')

		Xset.clicked.connect(self.Xset_clicked)
		Yset.clicked.connect(self.Yset_clicked)
		self.Xcur.returnPressed.connect(Xset.click)
		self.Ycur.returnPressed.connect(Yset.click)

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
		self.laser = QPoint(self.mmtpx(float(self.Xcur.text())),self.laser.y())
		self.update()

	def Yset_clicked(self):
		self.laser = QPoint(self.laser.x(),self.height-self.mmtpy(float(self.Ycur.text())))
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
		self.xvel_box.returnPressed.connect(xvel_set.click)
		self.yvel_box.returnPressed.connect(yvel_set.click)

		self.ConfBox = QGroupBox('Configuration')
		layout = QGridLayout()
		layout.addWidget(xvel_lab,0,0)
		layout.addWidget(self.xvel_box,0,1)
		layout.addWidget(xvel_set,0,2)
		layout.addWidget(yvel_lab,1,0)
		layout.addWidget(self.yvel_box,1,1)
		layout.addWidget(yvel_set,1,2)
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
		targ_vals = [(self.width/2)-(self.pix/2),(self.height/2)-(self.pix/2),self.pix,self.pix]
		qp.drawEllipse(targ_vals[0]-4,targ_vals[1],targ_vals[2]+4,targ_vals[3])
		qp.setPen(QColor(175,100,0))
		qp.setBrush(QColor(175,100,0))
		qp.drawEllipse(targ_vals[0],targ_vals[1],targ_vals[2],targ_vals[3])
		qp.setPen(Qt.black)
		qp.setBrush(Qt.green)
		qp.drawEllipse(self.laser,5,5)

	def on_target(self):
		r = np.sqrt((self.laser.x()-self.height/2)**2+(self.laser.y()-self.width/2)**2)
		print(r)
		if r <= self.pix/2:
			return True
		else:
			return False

	


def set_dark(app):
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




if __name__ == '__main__':
	#print('-'*60)
	#print('-'*60)
	#print('STARTING RASTER GUI')
	#print('-'*60)
	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	set_dark(app)
	gui = MainWindow()
	sys.exit(app.exec_())