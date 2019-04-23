# Raster-GUI

This GUI is designed to remotely control the Newport CONEX TRA12-CC actuators that move the last mirror in our ablation laser setup.  The pattern is selected for the purpose of maximizing target utilization and minimizing bad signals from ablating off-target.

## Getting Started

First off, make sure that you have the ConexCC.py file in the same folder as the GUI program.  The only file you have to run is the RasterGUI.py file.  The ConexCC.py file is called from within the raster GUI, and the other files are all for reference in building GUIs.  Keep in mind that the scope of this implementation is running motors from a Windows 7 machine and communicating via that machine's COM6 and COM7 serial ports.  NOTE: is there is a connection problem, check to make sure that the correct COM ports are being used via the Windows Device Manager.

### Packages Used

* Python 3.7.2
* PyQt5 - Python package for creating GUIs, easier to use than tkinter
* numpy - Python package for handling more advanced mathematics

PyQt5 and numpy can be installed with

```
pip install PyQt5
pip install numpy
```

## ConexCC.py

This file is a python package that is used to communicate with the Newport motors over a serial connection.  Hence the
```
import serial
```
command.  This package should come default with your python 3 installation.

### Usage

The ConexCC package implements all the commands that the actuator controller can receive.  In essence, the class (when called) creates a "ConexCC" object.  The "__init__" function initializes the motor and makes it ready for use. The motor object has a fundamental "query" function on which all other functions rely.  Each individual function is named after its command, and uses the "query" function to send the command and receive a response (if any).  (See CONEX-CC_Controller_Documentation.pdf for full listing of commands and how they work and what they return.)

NOTE: It is very important to pay attention to the Controller State Diagram (see Page 5 of CONEX-CC_Controller_Documentation.pdf).  Some commands can only be received in certain states and as of now the package DOES NOT THROW AND ERROR IF THE STATE IS WRONG!  So be careful!

### Future Plans

It would be ideal if this package would allow direct communication with the motor via the command line when called on its own.  For example a change in the
```
if __name__ == '__main__':
```
section that allows for communication until a "quit" command is given.

## RasterGUI.py

This file is the actual control gui, as of now it is still under development, so this readme will be updated later.