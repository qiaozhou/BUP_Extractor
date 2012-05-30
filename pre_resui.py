#!/usr/bin/python2.5
#Author: RICHARD Georges-Emmanuel
#contact: joe@pec-corporation.com
#under license see COPYING
import popen2,os,time,sys

if __name__ == "__main__":

    if '-pyside' in sys.argv or os.environ.get('QT_API')=='pyside':
        pyuicpath = '/bin/'
        pyuic = 'pyside-uic'
        pyrcc = 'pyside-rcc'
    else: # pyqt4
        pyuicpath = '/usr/bin/'
        pyuic = 'pyuic4'
        pyrcc = 'pyrcc4'

    if os.name == 'nt':
        try:
            pyuicpath = os.path.dirname(sys.executable)+'\\'
            if not os.path.exists(pyuicpath+'pyuic4.bat'):
                raise Exception
        except:
            pyuicpath = ''
        ext = ".bat "
    else:
        try:
            if not os.path.exists(pyuicpath+pyuic):
                raise Exception
        except:
            pyuicpath = ''
        ext = " "

    ui_list = [ "_Help.ui","_Main.ui"]
    
    for uifile in ui_list:
        if os.path.exists(uifile):
            cmd = pyuicpath+pyuic+ext+uifile+" -o _ui"+uifile[:-2]+"py"
            print popen2.popen2(cmd)[0].read()
            #time.sleep(1)
            print cmd
        else:
            print uifile,"doesn't exist"

    if '-c' in sys.argv:
        import glob
        print 'compile script:'
        for e in glob.glob('*.py'):
            try:
                if e in ['freeze_setup.py','pre_resui.py']:
                    continue
                __import__(e[:-3])
                print e
            except:
                pass
