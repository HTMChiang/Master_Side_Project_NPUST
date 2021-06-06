from PyQt5 import QtWidgets
from STFTUI import Ui_MainWindow
import sys
import data
import ch1SFT
import ch2SFT
import ch3SFT
import ch4SFT

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.start.clicked.connect(self.startprocess)

    def startprocess(self):

        if self.ui.TimeFrequency.isChecked():
            TimeFrequency=1
        else:
            TimeFrequency=0

        if self.ui.dataharvest.isChecked():
            dataharvest=1
        else:
            dataharvest=0

        if self.ui.complexdiag.isChecked():
            complexdiag=1
        else:
            complexdiag=0

        if self.ui.Timedomain.isChecked():
            Timedomain=1
        else:
            Timedomain=0

        fs=self.ui.fs.text()
        fs=float(fs)
        N=self.ui.N.text()
        N=int(N)
        fmin=self.ui.fmin.text()
        fmin=float(fmin)
        fmax=self.ui.fmax.text()
        fmax=float(fmax)
        tmin = self.ui.tmin.text()
        tmin = float(tmin)
        tmax =self.ui.tmax.text()
        tmax = float(tmax)
        dBvalve=self.ui.dBvalve.text()
        dBvalve=float(dBvalve)
        plotres = self.ui.plotres.text()
        plotres=float(plotres)
        vm = self.ui.vm.text()
        vm = float(vm)
        ch0instru = self.ui.ch0instru.text()
        ch1instru = self.ui.ch1instru.text()
        ch2instru = self.ui.ch2instru.text()
        ch3instru = self.ui.ch3instru.text()
        numberofchannel = self.ui.numberofchannel.text()
        numberofchannel=int(numberofchannel)
        microphonechannel = self.ui.microphonechannel.text()
        microphonechannel=int(microphonechannel)
        limtxset1 = self.ui.limtxset1.text()
        limtxset1=float(limtxset1)
        limtxset2=self.ui.limtxset2.text()
        limtxset2=float(limtxset2)
        limtxset3=self.ui.limtxset3.text()
        limtxset3=float(limtxset3)
        limtxset4=self.ui.limtxset4.text()
        limtxset4=float(limtxset4)
        filepath=self.ui.filepath.text()
        plotpath=self.ui.plotpath.text()
        wf=self.ui.wf.text()
        filetype=self.ui.filetype.text()
        float(fs)
        dt=1/fs
        path = plotpath
        data.mkdir(path)
        del path
        plotpath = plotpath + '/valve=' + str(dBvalve)  # 圖表存放路徑
        path = plotpath
        data.mkdir(path)
        del path
        if numberofchannel == 1:
            ch1SFT.ch1(fs, dt, N, fmin, fmax,tmax ,tmin ,wf , vm, dBvalve, plotres, TimeFrequency, dataharvest, complexdiag, Timedomain,
                       ch0instru, limtxset1, microphonechannel, filepath, plotpath,filetype)
        elif numberofchannel == 2:
            ch2SFT.ch2(fs, dt, N, fmin, fmax,tmax ,tmin ,wf , vm, dBvalve, plotres, TimeFrequency, dataharvest, complexdiag, Timedomain,
                       ch0instru, ch1instru, limtxset1, limtxset2, microphonechannel, filepath, plotpath,filetype)
        elif numberofchannel == 3:
            ch3SFT.ch3(fs, dt, N, fmin, fmax,tmax ,tmin ,wf , vm, dBvalve, plotres, TimeFrequency, dataharvest, complexdiag, Timedomain,
                       ch0instru, ch1instru, ch2instru, limtxset1, limtxset2, limtxset3, microphonechannel, filepath,
                       plotpath,filetype)
        elif numberofchannel == 4:
            ch4SFT.ch4(fs, dt, N, fmin, fmax,tmax ,tmin ,wf , vm, dBvalve, plotres, TimeFrequency, dataharvest, complexdiag, Timedomain,
                       ch0instru, ch1instru, ch2instru, ch3instru, limtxset1, limtxset2, limtxset3, limtxset4,
                       microphonechannel, filepath, plotpath,filetype)
        else:
            print('please check the number of input channel')

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
