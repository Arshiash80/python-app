from PyQt5.QtCore import QTime, QTimer,Qt
from PyQt5.QtWidgets import QApplication, QLCDNumber ,QVBoxLayout,QWidget ,QLabel
import sys
from MainWindow import Ui_MainWindow

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        v_box = QVBoxLayout()
        self.lbl = QLabel()
        self.lbl.setAlignment(Qt.AlignCenter)
        v_box.addWidget(self.lbl)
        self.setLayout(v_box)
        timer = QTimer(self)
        timer.timeout.connect(self.displaytime)
        timer.start(1000)

    def displaytime(self):
        currentTime = QTime.currentTime()
        displayText = currentTime.toString('hh:mm:ss')
        print(displayText)
        self.lbl.setText(displayText)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())