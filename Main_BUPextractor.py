#!/usr/bin/env python
#############################################################################
##
## Copyright (C) 2012 Georges-Emmanuel RICHARD.
## All rights reserved.
##
##
## You may use this file under the terms of the GPL v3 license
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
#############################################################################

## This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

#from myconfig import *

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic  # PySide.QtUiTools.QUiLoader

SRCFILE,SRCDATE,SRCSIZE,NBRFILES,VIRUSNAME,DATE,NAME0 = range(7)
#SUBJECT, SENDER, DATE = range(3)

class SortFilterProxyModel(QtGui.QSortFilterProxyModel):
# Work around the fact that QSortFilterProxyModel always filters datetime
# values in QtCore.Qt.ISODate format, but the tree views display using
# QtCore.Qt.DefaultLocaleShortDate format.
    def filterAcceptsRow(self, sourceRow, sourceParent):
        # Do we filter for the date column?
        if self.filterKeyColumn() == DATE:
            # Fetch datetime value.
            index = self.sourceModel().index(sourceRow, DATE, sourceParent)
            data = self.sourceModel().data(index)

            # Return, if regExp match in displayed format.
            return (self.filterRegExp().indexIn(data.toString(QtCore.Qt.DefaultLocaleShortDate)) >= 0)

        # Not our business.
        return super(SortFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

def exec_cmd(cmd):
    subres = []
    cmdlist = cmd.strip().split('|')
    limit = len(cmdlist)-1
    for i,subcmd in enumerate(cmdlist):
        subres.append(QProcess())
        if i!=0:
            subres[i-1].setStandardOutputProcess(subres[i])

    for i,subcmd in enumerate(cmdlist):
        subres[i].setProcessChannelMode(QProcess.MergedChannels) # latest modification to merge Stder with Stdout
        subres[i].start(subcmd.strip())
    subres[-1].waitForStarted()
    subres[-1].waitForFinished() #30second avant un timeout
    subres[-1].waitForReadyRead() #30seconds avant un timeout
    res = str(subres[-1].readAll())
    return res

def QAPP_NEW():
    global app
    try:
        app
    except NameError,e:
        app = QApplication(sys.argv)
    return app

def QAPP_END():
    try:
        ipmagic #we are under ipython (works with 0.11)
    except NameError:
        sys.exit(app.exec_())

import os,datetime
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

try:
    Ui_Form, base_class = uic.loadUiType("_Main.ui")
    exec_cmd("pyuic4 _Main.ui -o _Main.py")
except:
    import _ui_Main
    Ui_Form = _ui_Main.Ui_MainWindow
try:
    Ui_Dlg, base_class = uic.loadUiType("_Help.ui")
    exec_cmd("pyuic4 _Help.ui -o _Help.py")
except:
    import _ui_Help
    Ui_Dlg = _ui_Help.Ui_Dialog

class Help(QDialog,  Ui_Dlg):
    def __init__(self, parent = None):
        super(Help, self).__init__(parent)
        self.setupUi(self)

def BUPextract(BUPfile,filetoextract='Details',newfilename='Details.txt',targetfolder='.'):
    if 'Error' in os.popen('7z.exe x '+BUPfile+' '+filetoextract+' -yo"'+targetfolder+'"').read():
        print "Error on ",filetoextract
    b = bytearray(open(os.path.join(targetfolder,filetoextract), 'rb').read())
    for i in range(len(b)):
        b[i] ^= 0x6A
    open(os.path.join(targetfolder,newfilename), 'wb').write(b)
    os.remove(os.path.join(targetfolder,filetoextract))
    
class Window(QMainWindow,  Ui_Form):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setupUi(self)

        self._Folder = ''
        
        self.actionOpen_folder.triggered.connect(self.OpenFolder)
        self.actionDelete.triggered.connect(self.Remove)
        self.Help = Help()
        self.actionAbout.triggered.connect(self.Help.exec_)
        self.pbBrowseDest.clicked.connect(self.SelectDestination)

        self.pbRestore.clicked.connect(self.Restore)

        self.pbTickAll.clicked.connect(self.TickFiles)
        self.pbUnTickAll.clicked.connect(self.UnTickFiles)
        
        self.pb = QProgressBar(self.statusBar())
        self.pb.setFormat("%v/%m")
        self.statusBar().addPermanentWidget(self.pb)

        self.proxyModel = SortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)
        
        self.proxyGroupBox = QtGui.QGroupBox("Sorted/Filtered Model")
        #proxyModel.setData(0,QtCore.Qt.Checked,QtCore.Qt.CheckStateRole)

        self.proxyView.setModel(self.proxyModel)

        self.filterSyntaxComboBox.addItem("Regular expression",
                QtCore.QRegExp.RegExp)
        self.filterSyntaxComboBox.addItem("Wildcard",
                QtCore.QRegExp.Wildcard)
        self.filterSyntaxComboBox.addItem("Fixed string",
                QtCore.QRegExp.FixedString)

        self.filterColumnComboBox.addItem("SRCFILE")
        self.filterColumnComboBox.addItem("SRCDATE")
        self.filterColumnComboBox.addItem("SRCSIZE")
        self.filterColumnComboBox.addItem("NBRFILES")
        self.filterColumnComboBox.addItem("VIRUSNAME")
        self.filterColumnComboBox.addItem("DATE")
        self.filterColumnComboBox.addItem("NAME0")

        self.filterPatternLineEdit.textChanged.connect(self.filterRegExpChanged)
        self.filterSyntaxComboBox.currentIndexChanged.connect(self.filterRegExpChanged)
        self.filterColumnComboBox.currentIndexChanged.connect(self.filterColumnChanged)
        self.filterCaseSensitivityCheckBox.toggled.connect(self.filterRegExpChanged)
        self.sortCaseSensitivityCheckBox.toggled.connect(self.sortChanged)

        self.setWindowTitle("Basic Sort/Filter Model")
        self.resize(500, 450)

        self.proxyView.sortByColumn(SRCFILE, QtCore.Qt.AscendingOrder)
        self.filterColumnComboBox.setCurrentIndex(SRCFILE)

        self.filterPatternLineEdit.setText("")
        self.filterPatternLineEdit.setToolTip("RegExp separated with |")

        self.show()
        QtGui.qApp.processEvents()
        self.updateModel(".")

    def UnTickFiles(self):
        self.setCheckStateFiles(Qt.Unchecked)
        
    def TickFiles(self):
        self.setCheckStateFiles(Qt.Checked)
        
    def setCheckStateFiles(self, state):
        for a in self.proxyView.selectedIndexes():
            if a.column() == 0:
                chkboxline = self.model.findItems(a.data())
                chkboxline[0].setCheckState(state)
        
    def OpenFolder(self):
        ret = str(QFileDialog.getExistingDirectory(directory=self._Folder, options=QFileDialog.ReadOnly))
        if ret != '':
            self._Folder = ret
            self._SrcFolder = ret
            self.model.clear()
            self.updateModel(ret)

    def SelectDestination(self):
        ret = str(QFileDialog.getExistingDirectory(directory=self._Folder, options=QFileDialog.DontResolveSymlinks))
        if ret != '':
            self._Folder = ret
            self.leDestFolder.setText(ret)

    def Restore(self):
        if self.leDestFolder.text() == '':
            QMessageBox.warning(self,'No Destination Folder','You must select a destination folder')
            self.SelectDestination()
            self.Restore()
            return
        dest = str(self.leDestFolder.text())
        ticked = []
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if item.checkState() ==  Qt.Checked:
                ticked.append(item)

        self.pb.setRange(0,max(1,len(ticked)))
        for i,item in enumerate(ticked):
            BUPfile=os.path.join(os.path.realpath(self._SrcFolder),str(self.model.data(self.model.index(item.row(),SRCFILE))))
            
            to_restore = str(self.model.data(self.model.index(item.row(),NAME0)))
            
            self.statusBar().showMessage(self.tr(to_restore))
            self.pb.setValue(i+1)
            QtGui.qApp.processEvents()
            
            folders = os.path.dirname(to_restore).replace(":","")
            filename = os.path.basename(to_restore)
            # extract File_0, xor with 0x6A, create folder into destination folder, and rename File_0 to real name
            BUPextract(BUPfile,filetoextract='File_0',newfilename=filename,targetfolder=os.path.join(dest,folders))
        self.pb.reset()
        self.statusBar().showMessage('')
        
    def Remove(self):
        ticked = []
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if item.checkState() ==  Qt.Checked:
                ticked.append(item)

        if QMessageBox.No == QMessageBox.question(self,'Confirmation','You will delete files from disk, are you sure?',QMessageBox.Yes|QMessageBox.No):
            QMessageBox.information(self,'Operation Cancelled','Operation Cancelled')
            return
            
        self.pb.setRange(0,max(1,len(ticked)))
        for i,item in enumerate(ticked):
            BUPfile=os.path.join(os.path.realpath(self._SrcFolder),str(self.model.data(self.model.index(item.row(),SRCFILE))))
            
            self.pb.setValue(i+1)
            QtGui.qApp.processEvents()
            
            os.remove(BUPfile)
            item.setCheckable(False)
            item.setCheckState(Qt.Unchecked)
            self.model.takeRow(item.row())
            
        self.pb.reset()
        self.statusBar().showMessage('')

    def setSourceModel(self, model):
        self.proxyModel.setSourceModel(model)

    def filterRegExpChanged(self):
        syntax_nr = self.filterSyntaxComboBox.itemData(self.filterSyntaxComboBox.currentIndex())
        syntax = QtCore.QRegExp.PatternSyntax(syntax_nr)

        if self.filterCaseSensitivityCheckBox.isChecked():
            caseSensitivity = QtCore.Qt.CaseSensitive
        else:
            caseSensitivity = QtCore.Qt.CaseInsensitive

        regExp = QtCore.QRegExp(self.filterPatternLineEdit.text(),
                caseSensitivity, syntax)
        self.proxyModel.setFilterRegExp(regExp)

    def filterColumnChanged(self):
        self.proxyModel.setFilterKeyColumn(self.filterColumnComboBox.currentIndex())

    def sortChanged(self):
        if self.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = QtCore.Qt.CaseSensitive
        else:
            caseSensitivity = QtCore.Qt.CaseInsensitive

        self.proxyModel.setSortCaseSensitivity(caseSensitivity)

    def updateModel(self,folder='C:\Joe\Mcafee_Quarantine\BUP_browser\FFF'):
        self.model = QtGui.QStandardItemModel(0, 7, self)
        self.proxyModel.setSourceModel(self.model)
        model = self.model
        model.setHeaderData(SRCFILE, QtCore.Qt.Horizontal, "Src File")
        model.setHeaderData(SRCDATE, QtCore.Qt.Horizontal, "Src Date")
        model.setHeaderData(SRCSIZE, QtCore.Qt.Horizontal, "Src Size")
        model.setHeaderData(NBRFILES, QtCore.Qt.Horizontal, "NumberOfFiles")
        model.setHeaderData(VIRUSNAME, QtCore.Qt.Horizontal, "DetectionName")
        model.setHeaderData(DATE, QtCore.Qt.Horizontal, "Date")
        model.setHeaderData(NAME0, QtCore.Qt.Horizontal, "OriginalName")

        #List folder's files with BUP extension
        import glob
        BUPList = glob.glob(folder+'\*.bup')
        
        self.pb.setRange(0,max(1,len(BUPList)))
        for i,f in enumerate(BUPList):
            if os.path.isdir(f):
                continue
            # extract 7z, xor 0x6A
            srcfile = os.path.basename(f)
            self.statusBar().showMessage(self.tr(srcfile))
            self.pb.setValue(i+1)
            QtGui.qApp.processEvents()
            BUPextract(f,'Details','Details.txt')
            
            # parse Details
            import ConfigParser
            config = ConfigParser.ConfigParser()
            config.readfp(open('Details.txt'))

            srcdate = QtCore.QDateTime(modification_date(f))
            srcsize = os.path.getsize(f)
            nbrfiles = config.getint('Details','NumberOfFiles')
            virusname = config.get('Details','DetectionName')
            date = QtCore.QDateTime(QtCore.QDate(config.getint('Details','CreationYear'), config.getint('Details','CreationMonth'), config.getint('Details','CreationDay')), QtCore.QTime(config.getint('Details','CreationHour'),config.getint('Details','CreationMinute'),config.getint('Details','CreationSecond')))
            if nbrfiles == 0:
                print "NoFile",virusname
                continue
            elif nbrfiles > 1:
                print "TooManyFiles"
                for i in range(nbrfiles):
                    print '\t' + config.get('File_'+str(i),'OriginalName')
            name0 = config.get('File_0','OriginalName')
            name0 = name0.strip('\\\\?\\')

            self.addFileEntry(model, srcfile,srcdate,srcsize,nbrfiles,virusname,date,name0)

        self.pb.reset()
        self.statusBar().showMessage('')

    def addFileEntry(self,model, srcfile,srcdate,srcsize,nbrfiles,virusname,date,name0):
        model.insertRow(0)
        model.setData(model.index(0, SRCFILE), srcfile)
        model.setData(model.index(0, SRCDATE), srcdate)
        model.setData(model.index(0, SRCSIZE), srcsize)
        model.setData(model.index(0, NBRFILES), nbrfiles)
        model.setData(model.index(0, VIRUSNAME), virusname)
        model.setData(model.index(0, DATE), date)
        model.setData(model.index(0, NAME0), name0)
        model.item(0).setCheckState(QtCore.Qt.Unchecked)
        model.item(0).setCheckable(True)

if __name__ == '__main__':

    import sys
    app = QAPP_NEW()#see myconfig

    window = Window()
    window.show()

    QAPP_END()#see myconfig    
