#!/usr/bin/python2.5
#Author: RICHARD Georges-Emmanuel
#contact: joe@pec-corporation.com
#under license see COPYING

#Usage: python2.6 freeze_setup.py (-license)
import os,shutil,sys
MainScript='Main_BUPextractor'

PYQT_API = os.environ.get('QT_API')
if PYQT_API==None:
    print "No QT API defined, please set the environnement variable QT_API to pyside or pyqt"
    sys.exit(1)

os.popen2('rm -rf dist')[1].read()
execfile('pre_resui.py') # to generate ui->py

###################################################################
from distutils.sysconfig import get_python_lib
pytzzones = get_python_lib()+"/pytz/zoneinfo/"

if sys.version_info <= (2, 5, 0, 'final', 0):
    opt_inc=("pytz",)+tuple(zones)
else:
    opt_inc=()
from bbfreeze import Freezer
f = Freezer("dist",
           #includes=("matplotlib",
                     #"matplotlib.numerix.fft",
                     #"matplotlib.numerix.linear_algebra",
                     #"matplotlib.numerix.ma",
                     #"matplotlib.numerix.mlab",
                     #"matplotlib.numerix.random_array",
                     #)+opt_inc,
           includes=opt_inc,
           excludes=("myscript",
                     "_gtkagg",
                     "_tkagg",
                     "PyQt4.uic.port_v3")) #PyQt4.8 remove python3 module
f.addScript(MainScript+".py")
f()

print "app frozen!"

