import ctypes
import logging
from multiprocessing import Process, Queue
from PyQt6 import QtWidgets, QtGui, QtCore

from handlers import recording_ended_handler
from logger_config import config_client_logger
from recorder import record

config_client_logger()
logger = logging.getLogger(__name__)

SCALE_FACTOR = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100


class VoiceTranslatorMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        if not self.objectName():
            self.setObjectName('MainWindow')
        WIDTH = 400
        HEIGHT = 120
        self.resize(WIDTH, HEIGHT)
        self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))
        self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName('centralwidget')
        self.recordTimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.recordTimeLabel.setObjectName('recordTimeLabel')
        self.recordTimeLabel.setGeometry(QtCore.QRect(120, 30, 90, 16))
        font = QtGui.QFont()
        font.setPointSize(round(12 / SCALE_FACTOR))
        font.setBold(True)
        self.recordTimeLabel.setFont(font)
        self.recordTimeLabel.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        self.recordTimeLabel.setStyleSheet('color: rgb(208, 69, 0);')
        self.recordTimeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.recordImagePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.recordImagePushButton.setObjectName('recordImagePushButton')
        self.recordImagePushButton.setGeometry(QtCore.QRect(200, 20, 38, 35))
        self.recordImagePushButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.recordImagePushButton.clicked.connect(self.start_stop_recording)
        record_image_path = 'record.png'
        self.recordImagePushButton.setStyleSheet(f'border-image: url({record_image_path});')
        self.messageLabel = QtWidgets.QLabel(self.centralwidget)
        self.messageLabel.setObjectName('recordTimeLabel')
        self.messageLabel.setGeometry(QtCore.QRect(0, 65, WIDTH, 35))
        font = QtGui.QFont()
        font.setPointSize(round(12 / SCALE_FACTOR))
        font.setBold(True)
        self.messageLabel.setFont(font)
        self.messageLabel.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        self.messageLabel.setStyleSheet('color: rgb(208, 69, 0);')
        self.messageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setObjectName('menubar')
        self.menubar.setGeometry(QtCore.QRect(0, 0, WIDTH, 22))
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName('statusbar')
        self.setStatusBar(self.statusbar)

        self.threadTimer = QtCore.QTimer(self)
        self.threadTimer.setInterval(1 * 1000)  # 1 second

        self.threadTimer.timeout.connect(self.update_timer)

        self.setWindowTitle(QtCore.QCoreApplication.translate('MainWindow', 'Voice Translator', None))
        self.recordTimeLabel.setText(QtCore.QCoreApplication.translate('MainWindow', '00:00', None))

        QtCore.QMetaObject.connectSlotsByName(self)

    def start_stop_recording(self):
        if self.threadTimer.isActive():
            self.threadTimer.stop()
            self.recordTimeLabel.setText('00:00')
            self.recordQueue.put(False)
            self.recordingProcess.join()
            self.recordingProcess.terminate()
            if not self.recordQueue.empty():
                recording_content = recording_ended_handler(self.recordQueue.get())
                self.messageLabel.setText(recording_content)

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

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if hasattr(self, 'recordingProcess') and self.recordingProcess:
            self.recordingProcess.terminate()


def main():
    app = QtWidgets.QApplication([])
    window = VoiceTranslatorMainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
