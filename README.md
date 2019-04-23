# Raster-GUI

This GUI is designed to remotely control the Newport CONEX TRA12-CC actuators that move the last mirror in our ablation laser setup.  The pattern is selected for the purpose of maximizing target utilization and minimizing bad signals from ablating off-target.

## Getting Started

First off, make sure that you have the ConexCC.py file in the same folder as the GUI program.  The only file you have to run is the RasterGUI.py file.  The ConexCC.py file is called from within the raster GUI, and the other files are all for reference in building GUIs.

### Packages Used

* Python 3.7.2
* PyQt5 - Python package for creating GUIs, easier to use than tkinter
* numpy - Python package for handling more advanced mathematics

PyQt5 and numpy can be installed with

```
pip install PyQt5
pip install numpy
```
