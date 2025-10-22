import sys
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from Base.base_window import BaseWindow
from page.login import Ui_MainWindow as LoginWindow
import requests

# Thread sınıfı
class ApiThread(QtCore.QThread):
    finished_signal = QtCore.pyqtSignal()  # Bittiğinde sinyal gönderecek

    def run(self):
        try:
            requests.get("http://127.0.0.1:8000/checkFile")
        except Exception as e:
            print("API Hatası:", e)
        self.finished_signal.emit()  # GUI thread'de işaretlenecek

class MainWindow(QtWidgets.QDialog, BaseWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\animasyon.ui", self)

        # GIF setup
        self.loading_gif = QtGui.QMovie(r"./img/loading.gif")
        self.loadingLabel.setMovie(self.loading_gif)
        self.loadingLabel.hide()

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(600, 300)

        # Status label
        self.statusLabel = QtWidgets.QLabel("Veri yükleniyor...", self)
        self.statusLabel.setGeometry(100, 200, 400, 40)
        self.statusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.statusLabel.setStyleSheet("background-color: white; color: black; font-size: 16px;")

        # Start loading
        self.start_loading()

    def start_loading(self):
        self.loadingLabel.show()
        self.loading_gif.start()
        self.statusLabel.setText("Veri yükleniyor...")

        # Thread ile API çağrısı
        self.thread = ApiThread()
        self.thread.finished_signal.connect(self.go_to_login)  # GUI thread'de çağrılır
        self.thread.start()

    def go_to_login(self):
        self.loading_gif.stop()
        self.loadingLabel.hide()
        self.statusLabel.setText("Yükleme tamamlandı!")
        self.open_menu(LoginWindow)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
