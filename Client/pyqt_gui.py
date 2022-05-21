import ctypes
from multiprocessing import Process, Queue
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtWidgets

from recorder import record

SCALE_FACTOR = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100


class VoiceTranslatorMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        if not self.objectName():
            self.setObjectName('MainWindow')
        self.resize(270, 80)
        self.setMinimumSize(QSize(270, 80))
        self.setMaximumSize(QSize(270, 80))
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName('centralwidget')
        self.recordTimeLabel = QLabel(self.centralwidget)
        self.recordTimeLabel.setObjectName('recordTimeLabel')
        self.recordTimeLabel.setGeometry(QRect(70, 30, 90, 16))
        font = QFont()
        font.setPointSize(round(12 / SCALE_FACTOR))
        font.setBold(True)
        self.recordTimeLabel.setFont(font)
        self.recordTimeLabel.setCursor(Qt.CursorShape.ArrowCursor)
        self.recordTimeLabel.setStyleSheet('color: rgb(208, 69, 0);')
        self.recordTimeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.recordImagePushButton = QPushButton(self.centralwidget)
        self.recordImagePushButton.setObjectName('recordImagePushButton')
        self.recordImagePushButton.setGeometry(QRect(150, 20, 38, 35))
        self.recordImagePushButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.recordImagePushButton.clicked.connect(self.start_stop_recording)
        record_image_path = 'record.png'
        self.recordImagePushButton.setStyleSheet(f'border-image: url({record_image_path});')
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar()
        self.menubar.setObjectName('menubar')
        self.menubar.setGeometry(QRect(0, 0, 270, 22))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName('statusbar')
        self.setStatusBar(self.statusbar)

        self.threadTimer = QTimer(self)
        self.threadTimer.setInterval(1 * 1000)  # 1 second

        self.threadTimer.timeout.connect(self.update_timer)

        self.setWindowTitle(QCoreApplication.translate('MainWindow', 'Voice Translator', None))
        self.recordTimeLabel.setText(QCoreApplication.translate('MainWindow', '00:00', None))

        QMetaObject.connectSlotsByName(self)

    def start_stop_recording(self):
        if self.threadTimer.isActive():
            self.threadTimer.stop()
            self.recordTimeLabel.setText('00:00')
            self.recordQueue.put(False)
        else:
            self.recordQueue = Queue()
            self.recordingProcess = Process(target=record, args=(self.recordQueue,))
            self.threadTimer.start()
            self.recordingProcess.start()

    def update_timer(self):
        minutes, seconds = map(lambda x: int(x), self.recordTimeLabel.text().split(':'))
        minutes = minutes + (seconds + 1) // 60
        seconds = (seconds + 1) % 60
        self.recordTimeLabel.setText(f'{minutes:02}:{seconds:02}')


def main():
    app = QtWidgets.QApplication([])
    window = VoiceTranslatorMainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
