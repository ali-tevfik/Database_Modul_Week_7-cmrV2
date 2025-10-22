from PyQt6 import  QtWidgets
import sys


# from page.login import Ui_MainWindow
from page.animasyon import MainWindow 

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())
