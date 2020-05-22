from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
import sys
import gui
import SerialRead as sr


class MainClass(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer()
        # threading interval set to 500ms
        self.timer.setInterval(500)
        # defining which function to call
        self.timer.timeout.connect(self.update_labels)
        self.timer.start()

    def update_labels(self):
        # updates labels with fresh data from SerialRead
        self.voltsOutput.setText(str(sr.volts))
        self.ampsOutput.setText(str(sr.amps))
        self.packCurrentOutput.setText(str(sr.packCurrent))
        self.packVoltageOutput.setText(str(sr.packVoltage))
        self.socOutput.setText(str(sr.packSoc))
        self.relayOutput.setText(str(sr.packRelay))
        self.mphOutput.setText(str(sr.speed))
        self.rpmOutput.setText(str(sr.rpm))
        self.odometerOutput.setText(str(sr.odometer))
        self.powerTrackersOutput.setText(str(sr.trackers))
        self.acAmpsOutput.setText(str(sr.commandAcAmps))
        self.dcAmpsOutput.setText(str(sr.commandDcAmps))
        self.rpmDcOutput.setText(str(sr.commandRpm))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainClass()
    window.show()
    app.exec_()
